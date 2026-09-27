# Voix off féminine (Kokoro TTS, licence Apache 2.0), calée sur les scènes de video.html.
# Modèle : kokoro-v1.0.onnx + voices-v1.0.bin (github.com/thewh1teagle/kokoro-onnx), chemin via KOKORO_DIR.
import os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

D = os.environ.get('KOKORO_DIR', '.')
k = Kokoro(os.path.join(D, 'kokoro-v1.0.onnx'), os.path.join(D, 'voices-v1.0.bin'))
SR = 24000; TOTAL = 28.5

# (début en s, durée max en s, texte)
LINES = [
    (0.15, 3.0, "Achetez-en un… le deuxième est offert !"),
    (3.35, 3.2, "Voici La Goutte d'Émeraude. Un cristal vert, taillé en goutte."),
    (6.75, 2.6, "Élégante le jour… inoubliable le soir."),
    (9.55, 2.6, "Livré dans son écrin, prêt à offrir."),
    (12.35, 3.1, "Un pour vous… un à offrir."),
    (15.75, 2.5, "Pour commander, allez sur maison l'émeraude point f r."),
    (18.35, 2.6, "Ajoutez le collier au panier."),
    (21.1, 2.8, "Validez… et vous recevez deux colliers."),
    (24.25, 4.0, "Offre limitée. Commandez maintenant !"),
]
track = np.zeros(int(TOTAL * SR), dtype=np.float32)
for start, room, text in LINES:
    speed = 1.0
    while True:
        s, sr = k.create(text, voice='ff_siwis', speed=speed, lang='fr-fr')
        nz = np.nonzero(np.abs(s) > 0.01)[0]
        s = s[max(0, nz[0] - 240): nz[-1] + 1200]  # coupe les silences
        if len(s) / sr <= room or speed >= 1.3: break
        speed = round(speed + 0.05, 2)
    print(f"{start:5.2f}s  {len(s)/sr:4.2f}/{room}s  x{speed}  {text}")
    i = int(start * SR); track[i:i + len(s)] += s[:len(track) - i]
sf.write('voix.wav', track / max(1e-6, np.abs(track).max()) * 0.95, SR)
