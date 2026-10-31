import json,glob,subprocess,numpy as np
d=json.load(open('flow/lines.json'))['lines']
for l in d:
    f=glob.glob(f"flow/takes/{l['i']:03d}_{l['id']}/*.mp3")[0]
    a=subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    x=np.frombuffer(a,np.float32); dur=len(x)/16000
    db=lambda s: 20*np.log10(np.sqrt(np.mean(s**2))+1e-9)
    # find last frame above -40 dB
    fr=400; e=[db(x[i:i+fr]) for i in range(0,len(x)-fr,fr)]
    last=max([i for i,v in enumerate(e) if v>-40] or [0])*fr/16000
    print(f"{l['i']:3d} {l['id']:12s} take={dur:6.2f} slot={l['end']-l['start']:6.2f} lastsound={last:6.2f} tail60ms={db(x[-960:]):6.1f} head={db(x[:960]):6.1f}")
