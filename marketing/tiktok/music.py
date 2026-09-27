# Nappe musicale douce (libre de droits, générée) : accords + arpège cristallin.
import numpy as np, wave
SR = 44100; DUR = 28.5
t = np.arange(int(SR * DUR)) / SR
out = np.zeros_like(t)
n = lambda m: 440 * 2 ** ((m - 69) / 12)
BAR = 2.0  # ~120 bpm, 4 temps par mesure
prog = [[57, 64, 69, 72], [53, 60, 65, 69], [48, 55, 60, 64], [55, 62, 67, 71]]  # Am F C G
bars = int(np.ceil(DUR / BAR))
for b in range(bars):
    ch = prog[b % 4]; t0 = b * BAR
    seg = (t >= t0) & (t < t0 + BAR + 1.0)
    tt = t[seg] - t0
    env = np.minimum(1, tt / .35) * np.exp(-np.maximum(0, tt - BAR) * 3)
    for m in ch:
        f = n(m)
        out[seg] += .05 * env * (np.sin(2*np.pi*f*tt) + .3*np.sin(2*np.pi*2*f*tt + .5)) * (1 + .15*np.sin(2*np.pi*.5*tt))
    out[seg] += .08 * env * np.sin(2*np.pi*n(ch[0]-12)*tt)
    arp = [ch[1]+12, ch[2]+12, ch[3]+12, ch[2]+12] * 2
    for k, m in enumerate(arp):
        s0 = t0 + k * BAR / 8
        sg = (t >= s0) & (t < s0 + 1.2); tt = t[sg] - s0
        f = n(m)
        out[sg] += .06 * np.exp(-tt * 4.5) * np.minimum(1, tt/.005) * (np.sin(2*np.pi*f*tt) + .25*np.sin(2*np.pi*3*f*tt))
# réverbération simple
rev = out.copy()
for d, g in [(.043, .35), (.071, .3), (.113, .25), (.167, .2), (.251, .15)]:
    k = int(d * SR); rev[k:] += g * out[:-k]
out = rev
out *= np.minimum(1, t / .3) * np.minimum(1, (DUR - t) / 1.5)
out = out / np.abs(out).max() * .7
data = (np.stack([out, np.roll(out, 300)], 1) * 32767).astype('<i2')
with wave.open('music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())
