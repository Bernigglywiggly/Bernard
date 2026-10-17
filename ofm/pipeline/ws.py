#!/usr/bin/env python3
"""WaveSpeed AI client: submit -> poll -> download, with a spend ledger and hard caps.

Key handling
  * Reads WAVESPEED_API_KEY from the environment, else from ~/Bernard/ofm/.env
    (a line `WAVESPEED_API_KEY=...`). The owner creates that file himself.
  * The key is never printed, logged, written to the ledger, or put in a URL.

Money handling
  * Every paid call is estimated first (PRICES below, taken from wavespeed.ai model
    pages on 12 Oct 2026, +10% safety margin) and refused if it would push this run
    past --run-cap (default $2) or this calendar month past --month-cap (default $100).
  * Every call is written to out/spend.csv. When the key can read the balance,
    the real balance before/after each run is logged too, so estimates can be checked.
  * --dry-run prints the exact request JSON + estimate and makes NO network call.

CLI
  python ws.py balance                 # real account balance (needs key)
  python ws.py ledger                  # month-to-date spend from out/spend.csv
  python ws.py estimate MODEL '{json}' # cost estimate for one request
  python ws.py run MODEL '{json}' [--dry-run]   # one raw call (images may be local paths)
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import mimetypes
import os
import sys
import time
import uuid
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
OFM = HERE.parent
OUT = HERE / "out"
CACHE = HERE / "cache"
LEDGER = OUT / "spend.csv"
ENV_FILE = OFM / ".env"

API = "https://api.wavespeed.ai/api/v3"
SAFETY_MARGIN = 1.10          # estimates are multiplied by this before cap checks
DEFAULT_RUN_CAP = float(os.environ.get("WS_RUN_CAP", "2.0"))
DEFAULT_MONTH_CAP = float(os.environ.get("WS_MONTH_CAP", "100.0"))
TERMINAL_BAD = {"failed", "cancelled", "timeout", "deleted"}

# ----------------------------------------------------------------------------------
# Prices (USD) from each model's wavespeed.ai page, read 12 Oct 2026. Pages warn that
# "documentation prices may be outdated; the final task charge prevails" -> we keep a
# margin and log the real balance delta.
# ----------------------------------------------------------------------------------

def _res(p, default="1k"):
    return str(p.get("resolution", default)).lower()


def _n_images(p):
    imgs = p.get("images") or []
    return len(imgs) if isinstance(imgs, list) else 1


def _dur(p, default=5):
    return float(p.get("duration", default))


PRICES = {
    # --- identity-locked edit / multi-reference ---
    "bytedance/seedream-v5.0-flash/edit": lambda p: 0.027,
    "bytedance/seedream-v5.0-flash": lambda p: 0.027,
    "bytedance/seedream-v5.0-pro/edit": lambda p: (0.09 if _res(p) == "2k" else 0.045)
        + 0.003 * max(0, _n_images(p) - 1),
    "bytedance/seedream-v5.0-pro": lambda p: 0.09 if _res(p) == "2k" else 0.045,
    "google/nano-banana-2.1/edit": lambda p: {"1k": 0.04, "2k": 0.06, "4k": 0.135}[_res(p)]
        + 0.002 * _n_images(p),
    "google/nano-banana-2.1/text-to-image": lambda p: {"1k": 0.04, "2k": 0.06, "4k": 0.135}[_res(p)],
    "google/nano-banana-pro/edit": lambda p: {"1k": 0.14, "2k": 0.14, "4k": 0.24}[_res(p)],
    "openai/gpt-image-2/edit": lambda p: {
        ("low", "1k"): 0.02, ("low", "2k"): 0.03, ("low", "4k"): 0.04,
        ("medium", "1k"): 0.07, ("medium", "2k"): 0.11, ("medium", "4k"): 0.19,
        ("high", "1k"): 0.23, ("high", "2k"): 0.41, ("high", "4k"): 0.73,
    }[(p.get("quality", "medium"), _res(p))] + 0.012 * max(0, _n_images(p) - 1),
    "kwaivgi/kling-image-o1": lambda p: 0.028 * int(p.get("num_images", 1)),
    "wavespeed-ai/qwen-image/edit-2511": lambda p: 0.03,
    # --- LoRA route ---
    "wavespeed-ai/z-image-lora-trainer": lambda p: 1.25 * float(p.get("steps", 1000)) / 1000,
    "wavespeed-ai/qwen-image-2512-lora-trainer": lambda p: 1.00 * float(p.get("steps", 1000)) / 1000,
    "wavespeed-ai/flux-dev-lora-trainer": lambda p: 1.00 * float(p.get("steps", 1000)) / 1000,
    "wavespeed-ai/z-image/turbo-lora": lambda p: 0.01,
    "wavespeed-ai/z-image-turbo/image-to-image-lora": lambda p: 0.01,   # page not read: assumed = turbo-lora
    "wavespeed-ai/qwen-image/edit-2511-lora": lambda p: 0.025,
    "wavespeed-ai/qwen-image/text-to-image-2512-lora": lambda p: 0.03,  # page not read: assumed
    # --- image-to-video (Reels) ---
    "kwaivgi/kling-v2.6-std/image-to-video": lambda p: 0.21 if _dur(p) <= 5 else 0.42,
    "kwaivgi/kling-v3.0-std/image-to-video": lambda p: 0.084 * _dur(p) * (1.5 if p.get("sound") else 1),
    "kwaivgi/kling-v3.0-pro/image-to-video": lambda p: 0.112 * _dur(p) * (1.5 if p.get("sound") else 1),
    "wavespeed-ai/minimax-h3/image-to-video": lambda p: {"480p": 0.04, "540p": 0.06, "768p": 0.08,
                                                         "1080p": 0.16}[_res(p, "480p")] * _dur(p),
    "alibaba/wan-3.0/image-to-video": lambda p: {"480p": 0.05, "720p": 0.10, "1080p": 0.20}[_res(p, "720p")]
        * math.ceil(_dur(p)),
    "bytedance/seedance-2.0/image-to-video": lambda p: {"480p": 0.12, "720p": 0.24, "1080p": 0.60,
                                                        "4k": 1.20}[_res(p, "720p")] * _dur(p),
    "google/veo3.1-fast/image-to-video": lambda p: (0.15 if p.get("generate_audio", True) else 0.10) * _dur(p, 8),
    # --- upscalers ---
    "wavespeed-ai/seedvr2/image": lambda p: 0.01,
    "wavespeed-ai/image-upscaler": lambda p: 0.01,
    "wavespeed-ai/ultimate-image-upscaler": lambda p: 0.06,
    "clarity-ai/crystal-upscaler": lambda p: 0.05 if float(p.get("target_megapixels", 4)) <= 4 else 0.20,
}


def estimate(model: str, payload: dict) -> float:
    if model not in PRICES:
        raise SystemExit(f"[ws] no price on file for {model!r}: add it to PRICES in ws.py first "
                         "(refusing to spend blind).")
    return round(PRICES[model](payload), 4)


# ----------------------------------------------------------------------------------
# Key
# ----------------------------------------------------------------------------------

def load_key(required: bool = True) -> str | None:
    key = os.environ.get("WAVESPEED_API_KEY", "").strip()
    if not key and ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line.startswith("WAVESPEED_API_KEY") and "=" in line:
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    if not key and required:
        raise SystemExit(f"[ws] No API key. Owner: create {ENV_FILE} containing one line "
                         "WAVESPEED_API_KEY=... (never paste the key in chat).")
    return key or None


def have_key() -> bool:
    return load_key(required=False) is not None


# ----------------------------------------------------------------------------------
# Ledger
# ----------------------------------------------------------------------------------
FIELDS = ["ts", "run_id", "job", "model", "task_id", "est_usd", "status", "note"]


def month_spent(month: str | None = None) -> float:
    month = month or dt.date.today().strftime("%Y-%m")
    if not LEDGER.exists():
        return 0.0
    total = 0.0
    with LEDGER.open() as f:
        for row in csv.DictReader(f):
            # count everything that was submitted (a failed task may still be billed)
            if row["ts"].startswith(month) and row["status"] not in ("dry-run", "refused"):
                try:
                    total += float(row["est_usd"] or 0)
                except ValueError:
                    pass
    return round(total, 4)


def log(row: dict):
    OUT.mkdir(parents=True, exist_ok=True)
    new = not LEDGER.exists()
    with LEDGER.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in FIELDS})


class CapExceeded(RuntimeError):
    pass


# ----------------------------------------------------------------------------------
# Client
# ----------------------------------------------------------------------------------

class WaveSpeed:
    """One instance = one "run" (one CLI invocation) with its own cap."""

    def __init__(self, dry_run: bool = False, run_cap: float = DEFAULT_RUN_CAP,
                 month_cap: float = DEFAULT_MONTH_CAP, job: str = ""):
        self.dry_run = dry_run
        self.run_cap = run_cap
        self.month_cap = month_cap
        self.job = job
        self.run_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:4]
        self.run_est = 0.0          # committed (submitted) estimate this run
        self._key = None if dry_run else load_key(required=True)
        self._balance_start = None
        if not dry_run:
            self._balance_start = self.balance(quiet=True)
            if self._balance_start is not None:
                log({"ts": _now(), "run_id": self.run_id, "job": job, "model": "-",
                     "status": "balance-start", "note": f"{self._balance_start:.4f}"})

    # -- http helpers (key only ever goes in the Authorization header) --
    def _h(self, json_body=True):
        h = {"Authorization": f"Bearer {self._key}"}
        if json_body:
            h["Content-Type"] = "application/json"
        return h

    def balance(self, quiet=False) -> float | None:
        if self.dry_run:
            return None
        try:
            r = requests.get(f"{API}/balance", headers=self._h(False), timeout=20)
            r.raise_for_status()
            return float(r.json()["data"]["balance"])
        except Exception as e:  # never echo the request (headers)
            if not quiet:
                print(f"[ws] balance unavailable: {type(e).__name__}")
            return None

    # -- uploads --
    def upload(self, path: str | Path) -> str:
        """Local file -> WaveSpeed download_url (kept 7 days). Cached by content hash."""
        path = Path(path)
        if self.dry_run:
            return f"<upload:{path.name}>"
        import hashlib
        digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
        CACHE.mkdir(parents=True, exist_ok=True)
        cache_f = CACHE / "uploads.json"
        cache = json.loads(cache_f.read_text()) if cache_f.exists() else {}
        hit = cache.get(digest)
        if hit and time.time() - hit["t"] < 6 * 86400:      # files live 7 days
            return hit["url"]
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        with path.open("rb") as f:
            r = requests.post(f"{API}/media/upload/binary", headers=self._h(False),
                              files={"file": (path.name, f, mime)}, timeout=300)
        r.raise_for_status()
        url = r.json()["data"]["download_url"]
        cache[digest] = {"url": url, "t": time.time(), "name": path.name}
        cache_f.write_text(json.dumps(cache, indent=1))
        return url

    def resolve_media(self, payload: dict) -> dict:
        """Replace local file paths in image/images/last_image/end_image/data with uploaded URLs."""
        out = dict(payload)
        for k in ("image", "last_image", "end_image", "data"):
            v = out.get(k)
            if isinstance(v, str) and not v.startswith(("http://", "https://", "<")) and Path(v).exists():
                out[k] = self.upload(v)
        if isinstance(out.get("images"), list):
            out["images"] = [self.upload(v) if isinstance(v, str) and not v.startswith(("http", "<"))
                             and Path(v).exists() else v for v in out["images"]]
        return out

    # -- the one paid entry point --
    def run(self, model: str, payload: dict, dest: str | Path | None = None,
            note: str = "", timeout_s: float = 1800) -> dict:
        """Estimate, cap-check, submit, poll, download. Returns {'outputs': [...], 'files': [...]}."""
        est = estimate(model, payload)
        guarded = est * SAFETY_MARGIN
        spent_month = month_spent()
        print(f"[ws] {model}  est ${est:.4f}  (run so far ${self.run_est:.3f} / cap ${self.run_cap:.2f}; "
              f"month ${spent_month:.2f} / cap ${self.month_cap:.2f})")

        if self.dry_run:
            print("[ws] DRY RUN request:")
            print(f"POST {API}/{model}")
            print(json.dumps(payload, indent=2))
            log({"ts": _now(), "run_id": self.run_id, "job": self.job, "model": model,
                 "est_usd": est, "status": "dry-run", "note": note})
            self.run_est += est
            return {"outputs": [], "files": [], "est": est, "dry_run": True}

        if self.run_est + guarded > self.run_cap:
            log({"ts": _now(), "run_id": self.run_id, "job": self.job, "model": model,
                 "est_usd": est, "status": "refused", "note": "run cap"})
            raise CapExceeded(f"run cap ${self.run_cap:.2f} would be exceeded "
                              f"(${self.run_est:.3f} + ${guarded:.3f}). Raise --run-cap deliberately.")
        if spent_month + guarded > self.month_cap:
            log({"ts": _now(), "run_id": self.run_id, "job": self.job, "model": model,
                 "est_usd": est, "status": "refused", "note": "month cap"})
            raise CapExceeded(f"month cap ${self.month_cap:.2f} would be exceeded "
                              f"(${spent_month:.2f} + ${guarded:.3f}).")

        body = self.resolve_media(payload)
        r = requests.post(f"{API}/{model}", headers=self._h(), json=body, timeout=120)
        if r.status_code >= 400:
            log({"ts": _now(), "run_id": self.run_id, "job": self.job, "model": model,
                 "est_usd": 0, "status": f"http-{r.status_code}", "note": _safe_err(r)})
            raise RuntimeError(f"[ws] submit failed HTTP {r.status_code}: {_safe_err(r)}")
        data = r.json().get("data", {})
        task_id = data.get("id", "")
        self.run_est += est
        log({"ts": _now(), "run_id": self.run_id, "job": self.job, "model": model, "task_id": task_id,
             "est_usd": est, "status": "submitted", "note": note})

        result = self.poll(task_id, timeout_s=timeout_s)
        status = result.get("status")
        log({"ts": _now(), "run_id": self.run_id, "job": self.job, "model": model, "task_id": task_id,
             "est_usd": 0, "status": status, "note": (result.get("error") or "")[:200]})
        if status != "completed":
            raise RuntimeError(f"[ws] task {task_id} ended {status}: {result.get('error')}")
        outputs = result.get("outputs") or []
        files = []
        if dest:
            files = self.download(outputs, dest)
        return {"outputs": outputs, "files": files, "est": est, "task_id": task_id,
                "nsfw": result.get("has_nsfw_contents")}

    def poll(self, task_id: str, timeout_s: float = 1800) -> dict:
        url = f"{API}/predictions/{task_id}/result"
        t0, wait = time.time(), 2.0
        while time.time() - t0 < timeout_s:
            try:
                r = requests.get(url, headers=self._h(False), timeout=30)
                if r.status_code == 200:
                    d = r.json().get("data", {})
                    st = d.get("status")
                    if st == "completed" or st in TERMINAL_BAD:
                        return d
            except requests.RequestException:
                pass
            time.sleep(wait)
            wait = min(wait * 1.3, 10.0)       # >= 2 s between polls, as the docs ask
        return {"status": "timeout", "error": f"local poll timeout after {timeout_s}s"}

    @staticmethod
    def download(outputs: list, dest: str | Path) -> list[Path]:
        dest = Path(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        files = []
        for i, u in enumerate(outputs):
            if not isinstance(u, str) or not u.startswith("http"):
                continue
            ext = Path(u.split("?")[0]).suffix or ".bin"
            p = dest.with_suffix(ext) if len(outputs) == 1 else dest.parent / f"{dest.stem}_{i}{ext}"
            with requests.get(u, stream=True, timeout=300) as r:   # output URLs are public, no key sent
                r.raise_for_status()
                with p.open("wb") as f:
                    for chunk in r.iter_content(1 << 16):
                        f.write(chunk)
            files.append(p)
        return files

    def close(self):
        """Log the real balance delta for this run (truth check on the estimates)."""
        if self.dry_run:
            print(f"[ws] DRY RUN total estimate this run: ${self.run_est:.3f}")
            return
        end = self.balance(quiet=True)
        if end is not None:
            note = f"{end:.4f}"
            if self._balance_start is not None:
                note += f" (real spend this run ${self._balance_start - end:.4f} vs est ${self.run_est:.4f})"
            log({"ts": _now(), "run_id": self.run_id, "job": self.job, "model": "-",
                 "status": "balance-end", "note": note})
            print(f"[ws] balance now ${end:.2f}; {note}")
        print(f"[ws] estimated spend this run: ${self.run_est:.3f}")


def _now():
    return dt.datetime.now().isoformat(timespec="seconds")


def _safe_err(r) -> str:
    try:
        j = r.json()
        return str(j.get("message") or j.get("error") or j)[:300]
    except Exception:
        return r.text[:300]


def add_common_args(ap: argparse.ArgumentParser):
    ap.add_argument("--dry-run", action="store_true", help="print request JSON + cost, call nothing")
    ap.add_argument("--run-cap", type=float, default=DEFAULT_RUN_CAP, help="hard $ cap for this run (default 2)")
    ap.add_argument("--month-cap", type=float, default=DEFAULT_MONTH_CAP, help="hard $ cap per month (default 100)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("balance")
    sub.add_parser("ledger")
    e = sub.add_parser("estimate"); e.add_argument("model"); e.add_argument("payload")
    r = sub.add_parser("run"); r.add_argument("model"); r.add_argument("payload")
    r.add_argument("--out", default=None); add_common_args(r)
    a = ap.parse_args()
    if a.cmd == "balance":
        ws = WaveSpeed(job="balance")
        b = ws.balance()
        print(f"balance: ${b:.2f}" if b is not None else "balance: unavailable")
    elif a.cmd == "ledger":
        print(f"month-to-date estimated spend: ${month_spent():.2f} (cap ${DEFAULT_MONTH_CAP:.0f}); file {LEDGER}")
    elif a.cmd == "estimate":
        print(f"${estimate(a.model, json.loads(a.payload)):.4f}")
    elif a.cmd == "run":
        ws = WaveSpeed(dry_run=a.dry_run, run_cap=a.run_cap, month_cap=a.month_cap, job="raw")
        res = ws.run(a.model, json.loads(a.payload), dest=a.out or OUT / "raw" / ws.run_id)
        print(json.dumps({k: v for k, v in res.items() if k != "files"}, indent=1, default=str))
        ws.close()


if __name__ == "__main__":
    main()
