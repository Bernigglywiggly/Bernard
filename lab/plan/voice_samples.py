"""George pacing samples for the plan page: the same passage at the old pace and two faster ones."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "voice"))
import audio_fx as fx  # noqa: E402
import voice_lab as vl  # noqa: E402

TEXT = ("Eighteen forty-eight. San Francisco. A shopkeeper called Sam Brannan walks down the street holding up a bottle of gold, "
        "like he's just won the bloody Champions League. The whole city loses its mind. And Sam? Sam had already bought up the pans. "
        "And the shovels. Nine weeks later, he'd made thirty-six thousand dollars. He never dug for gold. Not once. Not one fucking scoop.")

if __name__ == "__main__":
    k = vl.engine()
    room = fx.cinema_ir(rt60=1.6, predelay=0.02, seed=5, dark=0.6)
    for tag, speed, pause in (("george_old_092", 0.92, 0.36), ("george_fast_102", 1.02, 0.24), ("george_faster_110", 1.10, 0.18)):
        y = vl.say(k, TEXT, "bm_george", speed=speed, pause=pause)
        wet = fx.chain_voice(y, exo_amt=0.0, room=room, room_wet=-13.0, target=-16.0)
        fx.save(os.path.join(HERE, "media", tag + ".wav"), wet, mp3=True)
        print(tag, round(len(y) / fx.SR, 1), "s")
