import numpy as np, wave
sr=44100; bpm=126; beat=60/bpm; bars=8; dur=bars*4*beat
N=int(sr*dur); out=np.zeros(N)
def add(i0,w,amp):
    seg=out[i0:i0+len(w)]; seg+=amp*w[:len(seg)]
def hz(m): return 440*2**((m-69)/12)
def saw(f,tt): return 2*(tt*f-np.floor(0.5+tt*f))
chords=[[57,60,64],[53,57,60],[60,64,67],[55,59,62]]
rng=np.random.default_rng(1)
for b in range(bars):
    ch=chords[b%4]; s=b*4*beat
    for k in range(4):
        t0=s+k*beat+beat/2; n=int(0.18*sr); tt=np.arange(n)/sr
        w=sum(saw(hz(c+12),tt) for c in ch)/3*np.exp(-tt*14); add(int(t0*sr),w,0.16)
    for k in range(8):
        n=int(beat/2*0.9*sr); tt=np.arange(n)/sr; m=ch[0]-24+(12 if k%2 else 0)
        add(int((s+k*beat/2)*sr),np.sin(2*np.pi*hz(m)*tt)*np.exp(-tt*6),0.32)
    scale=[69,72,74,76,79,81]
    for k in range(8):
        if k in (1,5): continue
        m=scale[(b*3+k*2)%len(scale)]; n=int(beat/2*sr); tt=np.arange(n)/sr
        w=(np.sin(2*np.pi*hz(m)*tt)+0.3*np.sin(4*np.pi*hz(m)*tt))*np.exp(-tt*7)
        add(int((s+k*beat/2)*sr),w,0.10 if b>=2 else 0.0)
    for k in range(4):
        n=int(0.22*sr); tt=np.arange(n)/sr; f=55+110*np.exp(-tt*35)
        add(int((s+k*beat)*sr),np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-tt*10),0.55)
    for k in (1,3):
        n=int(0.12*sr); add(int((s+k*beat)*sr),rng.standard_normal(n)*np.exp(-np.arange(n)/sr*30),0.12)
    for k in range(4):
        n=int(0.08*sr); add(int((s+k*beat+beat/2)*sr),rng.standard_normal(n)*np.exp(-np.arange(n)/sr*45),0.06)
out=out/np.max(np.abs(out))*0.9
f=int(sr*1.2); out[-f:]*=np.linspace(1,0,f)
d=(np.stack([out,out],1)*32767).astype(np.int16)
w=wave.open('trilha_insolar_02_animada.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(d.tobytes()); w.close()
