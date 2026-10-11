# Trilha original "brincadeira" (Dia das Crianças): tom maior, xilofone/sino, palmas, 120 BPM
import numpy as np, wave
sr=44100; bpm=120; beat=60/bpm; bars=8; dur=bars*4*beat
N=int(sr*dur); out=np.zeros(N+sr)
def add(i0,w,amp): seg=out[i0:i0+len(w)]; seg+=amp*w[:len(seg)]
def hz(m): return 440*2**((m-69)/12)
rng=np.random.default_rng(7)
chords=[[60,64,67],[65,69,72],[67,71,74],[60,64,67]]  # C F G C
mel=[72,74,76,79,76,74,72,74, 77,76,74,72,74,76,77,79, 79,77,76,74,76,77,79,81, 79,76,74,72,74,76,72,72]
for b in range(bars):
    ch=chords[b%4]; s=b*4*beat
    # baixo saltitante
    for k in range(4):
        n=int(beat*0.45*sr); tt=np.arange(n)/sr; m=ch[0]-24+(7 if k%2 else 0)
        add(int((s+k*beat)*sr),np.sin(2*np.pi*hz(m)*tt)*np.exp(-tt*7),0.30)
    # acordes pizzicato no contratempo
    for k in range(4):
        n=int(0.15*sr); tt=np.arange(n)/sr
        w=sum(np.sin(2*np.pi*hz(c+12)*tt) for c in ch)/3*np.exp(-tt*18)
        add(int((s+k*beat+beat/2)*sr),w,0.18)
    # melodia de xilofone (colcheias)
    for k in range(8):
        m=mel[(b*8+k)%len(mel)] if b>=1 else None
        if m is None or (k in (3,7) and b%2): continue
        n=int(0.35*sr); tt=np.arange(n)/sr
        w=(np.sin(2*np.pi*hz(m)*tt)+0.45*np.sin(2*np.pi*hz(m)*4*tt)*np.exp(-tt*30))*np.exp(-tt*9)
        add(int((s+k*beat/2)*sr),w,0.16)
    # bumbo
    for k in (0,2):
        n=int(0.2*sr); tt=np.arange(n)/sr; f=50+120*np.exp(-tt*35)
        add(int((s+k*beat)*sr),np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-tt*12),0.5)
    # palmas
    for k in (1,3):
        for d in (0,0.008,0.016):
            n=int(0.06*sr); add(int((s+k*beat+d)*sr),rng.standard_normal(n)*np.exp(-np.arange(n)/sr*60),0.10)
    # chocalho
    for k in range(8):
        n=int(0.05*sr); add(int((s+k*beat/2)*sr),rng.standard_normal(n)*np.exp(-np.arange(n)/sr*80),0.04)
out=out[:N]; out=out/np.max(np.abs(out))*0.9
f=int(sr*1.2); out[-f:]*=np.linspace(1,0,f)
d=(np.stack([out,out],1)*32767).astype(np.int16)
w=wave.open('trilha_insolar_03_criancas.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(d.tobytes()); w.close()
