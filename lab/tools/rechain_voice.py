"""Re-run the voice chain on an episode's saved dry voice (no new TTS): build/voice_dry.wav -> build/voice.wav.
Use after changing audio_fx (EQ, de-ess, compression, room, limiter).

    python3 tools/rechain_voice.py ep03
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import audio_fx as fx  # noqa: E402

if __name__ == "__main__":
    ep = sys.argv[1]
    build = os.path.join(HERE, "..", ep, "build")
    dry = fx.load(os.path.join(build, "voice_dry.wav"), mono=True)
    room = fx.cinema_ir(rt60=1.6, predelay=0.02, seed=5, dark=0.6)
    wet = fx.chain_voice(dry, exo_amt=0.0, room=room, room_wet=-13.0, target=-16.0)
    fx.save(os.path.join(build, "voice.wav"), wet, mp3=False)
    print(ep, "voice.wav", round(fx.lufs(wet), 2), "LUFS")
