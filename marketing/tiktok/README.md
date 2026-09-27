# Vidéo publicitaire TikTok / Reels / Meta: 9:16

| Fichier | Accroche (0 à 3 s) |
|---|---|
| `out/maison-lemeraude-tiktok-A.mp4` | « Achetez-en un. Le 2e est offert. » (offre en premier) |
| `out/maison-lemeraude-tiktok-B.mp4` | « Le cadeau qu'elle va adorer. » (émotion / cadeau) |
| `out/maison-lemeraude-tiktok-A-voix-off.mp4` | Version A + voix off féminine (`voix.py`, Kokoro TTS, licence Apache 2.0), son normalisé à −14 LUFS |

1080×1920 · 30 i/s · 28,5 s · H.264 + AAC · musique générée, libre de droits.

## Déroulé
1. 0–3 s: accroche sur photo portée + pastille « 1+1 offert »
2. 3–7 s: zoom sur le pendentif, caractéristiques
3. 7–9 s: porté (« Élégante le jour. Inoubliable le soir. »)
4. 9–12 s: l'écrin, prêt à offrir
5. 12–16 s: 1 acheté = 1 offert
6. 16–24 s: commander en 3 étapes (site → panier → commande), sur un téléphone
7. 24–28,5 s: appel à l'action + réassurance (paiement sécurisé, livraison suivie, retours 30 jours)

Textes placés dans la zone sûre TikTok/Reels (rien sous les boutons ni sous la légende).

## Texte de la publicité (suggestion)
**Texte principal :** Offre de lancement 🎁 Pour un collier La Goutte d'Émeraude acheté, le 2e est offert. Un pour vous, un à offrir. Chacun dans son écrin. Offre limitée.
**Titre :** 1 acheté = 1 offert
**Bouton :** Acheter

## Modifier / régénérer
`video.html` contient la composition (textes et minutage dans le `<script>`). Rendu :
```
pip install imageio-ffmpeg numpy
python3 music.py   # régénère la musique (convertir music.wav en music.m4a avec ffmpeg)
FFMPEG=$(python3 -c "import imageio_ffmpeg as i; print(i.get_ffmpeg_exe())") node render.js A
```
