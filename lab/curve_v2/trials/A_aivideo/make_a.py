"""Style trial A: hyper-real "Unreal Engine" look via AI (Seedream still -> Kling 2.6 image-to-video).

    ~/youtube/.venv/bin/python make_a.py            # ~ $0.71 on WaveSpeed
Generic hypercar only: no Tesla logo or exact design (style test, not a depiction of the real car).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / "ofm" / "pipeline"))
from ws import WaveSpeed  # noqa: E402

NEG = ("logos, badges, text, watermark, warped wheels, melting metal, extra wheels, flicker, low detail, "
       "cartoon, blurry")
CAR = ("a sleek two-door electric hypercar in candy-apple red, low wedge nose, wraparound glass canopy, "
       "no logos or badges")
SHOTS = [
    ("a1_hero", "16:9",
     f"Ultra-crisp Unreal Engine 5 cinematic render, low three-quarter front view of {CAR}, on a mirror-glossy "
     "black studio floor. Small white frosty cold-gas jets burst from nozzles behind the rear wheels. Hot magenta "
     "key light from the left, electric cyan rim light from the right, warm orange strip light overhead, light "
     "haze. Sharp ray-traced reflections, 35mm lens, shallow depth of field, vibrant saturated colour.",
     "The car's rear thrusters fire bright white frosty cold-gas jets, the car lifts off the floor, rolls a quick "
     "half barrel roll in the air and lands back on all four wheels with a small bounce. The camera orbits slowly "
     "left around the car. Magenta and cyan reflections slide across the paint. Ends with the car settled, "
     "three-quarter front view."),
    ("a2_xray", "16:9",
     f"Unreal Engine 5 technical cutaway render, side view of {CAR}, its body rendered as translucent tinted "
     "glass revealing a glowing carbon-wrapped cylindrical high-pressure tank behind the seats and thin glowing "
     "pipes running to eight small thruster nozzles at the corners. Nozzles glow electric cyan, battery pack deep "
     "blue, black studio, magenta rim light, crisp detail, vibrant colour.",
     "Slow camera push-in along the side of the translucent car. The high-pressure tank pulses with light, then "
     "glowing streaks travel through the pipes to each thruster nozzle one after another, each nozzle flashing "
     "cyan as it fills. Ends close on the rear nozzle cluster."),
    ("a3_ceiling", "9:16",
     f"Unreal Engine 5 cinematic render, vertical frame: {CAR} driving upside down along the ceiling of a long "
     "neon tunnel, wheels on the ceiling, tunnel lined with magenta and cyan light strips, motion streaks, camera "
     "low looking up the tunnel, glossy surfaces, vibrant saturated colour.",
     "The car speeds along the tunnel ceiling towards the camera, light strips streaking past. The camera rolls "
     "slowly 180 degrees until the car appears right side up. Ends with the car rushing past the lens."),
]


def main():
    ws = WaveSpeed(run_cap=1.0, job="curve_v2_trialA")
    for sid, aspect, still_prompt, motion in SHOTS:
        out = HERE / sid
        res = ws.run("bytedance/seedream-v5.0-flash",
                     {"prompt": still_prompt, "aspect_ratio": aspect, "resolution": "2k",
                      "output_format": "jpeg", "enable_safety_checker": True},
                     dest=out, note=f"{sid} still")
        still = res["files"][0]
        url = ws.upload(still)
        ws.run("kwaivgi/kling-v2.6-std/image-to-video",
               {"image": url, "prompt": motion, "negative_prompt": NEG, "duration": 5},
               dest=out, note=f"{sid} video")
        print(f"[A] {sid} done -> {out}")
    ws.close()


if __name__ == "__main__":
    main()
