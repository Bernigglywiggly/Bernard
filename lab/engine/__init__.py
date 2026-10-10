"""The Curve's episode engine: everything an episode needs except its script and its scenes, so a new episode (or a
new channel) is two files, not a new pipeline. Pulled out of EP03 (lab/ep03s), which stays as it was shipped.

    lab/<ep>/script.py   LINES (id, text, say, card, air, cut, floor), FLOORS, SOURCES
    lab/<ep>/scenes.py   frame(c, t): the line art, keyed to line ids through engine.tl (and optional TRAILS, GLINTS)
    lab/<ep>/film.py     the settings (title, music marks, shorts) and engine.film.main(...)

    python3 film.py voice          # George from the ElevenLabs cache (or the API) -> build/lines.json, voice.wav
    python3 film.py lines 3 9.5    # quick line-art stills (no characters)
    python3 film.py still 3 9.5    # stills in the finished look + a contact sheet
    python3 film.py render 4       # the caption-free picture in 4 parallel slices (the feed for the shorts too)
    python3 film.py parts 8 0 4    # or in resumable waves (each its own job, under the cloud's ~30-minute limit):
    python3 film.py parts 8 4 8    #   slices 0-3, then 4-7 (finished slices are kept), then
    python3 film.py join 8         #   join them into the feed
    python3 film.py sound          # sound events, the score, the mix
    python3 film.py master         # captions over the picture + the mix -> build/<ep>.mp4
    python3 film.py shorts         # the vertical cuts -> build/shorts/*.mp4 + kit.json
    python3 film.py all 4          # voice (if needed), render, sound, master, shorts

  tl        the timeline (lines.json by id, word times), sound events, the label queue
  draw      line-art primitives: formations, morphs, chrome numbers, Big Macs, coins, figures
  look      the ASCII look: lines -> characters with true strokes, one focus, a soft glow, crisp typed labels
  captions  the 16:9 captions, word by word from George's timings
  voice     the voice build for any episode directory
  score     Mainframe (or any bed) re-cut to the film's sections
  mix       voice on top, music ducked under it, the picture's detail sounds, mastered to -14 LUFS
  shorts    9:16 cuts with hooks and big captions
  film      the command line above
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.abspath(os.path.join(HERE, ".."))
V6 = os.path.abspath(os.path.join(LAB, "..", "a01_v6"))
for _p in (os.path.join(LAB, "voice"), os.path.join(LAB, "tools"), os.path.join(LAB, "sfx"), os.path.join(LAB, "music"), LAB, V6):
    if _p not in sys.path:
        sys.path.insert(0, _p)
os.environ.setdefault("A01V6_FONTS", os.path.join(V6, "fonts"))
