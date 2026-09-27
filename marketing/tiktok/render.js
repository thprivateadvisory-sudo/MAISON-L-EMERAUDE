// Rendu image par image de video.html puis encodage MP4 (1080x1920, 30 i/s).
// Usage : node render.js [A|B]           -> video complète
//         node render.js A --stills      -> quelques images de contrôle
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const variant = process.argv[2] || 'A';
const stills = process.argv.includes('--stills');
const FPS = 30;
const FFMPEG = process.env.FFMPEG || 'ffmpeg';
const out = path.join(__dirname, 'out');
fs.mkdirSync(out, { recursive: true });

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.join(__dirname, 'video.html') + '?v=' + variant);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForLoadState('networkidle');
  const duration = await page.evaluate(() => window.DURATION);

  if (stills) {
    for (const t of [0.2, 2.5, 5.5, 8.5, 11.5, 14.8, 17.2, 19.5, 20.2, 22.5, 23.5, 27]) {
      await page.evaluate(t => window.seek(t), t);
      await page.screenshot({ path: path.join(out, `still-${variant}-${t}.jpg`), type: 'jpeg', quality: 80 });
    }
    await browser.close();
    return;
  }

  const file = path.join(out, `maison-lemeraude-tiktok-${variant}.mp4`);
  const audio = path.join(__dirname, 'music.m4a');
  const args = ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-'];
  if (fs.existsSync(audio)) args.push('-i', audio, '-c:a', 'aac', '-b:a', '160k', '-shortest');
  args.push('-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-movflags', '+faststart', file);
  const ff = spawn(FFMPEG, args, { stdio: ['pipe', 'inherit', 'inherit'] });

  const frames = Math.round(duration * FPS);
  for (let i = 0; i < frames; i++) {
    await page.evaluate(t => window.seek(t), i / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 60 === 0) process.stdout.write(`\r${variant} ${i}/${frames}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log('\n' + file);
})();
