"""Benchmark Candidato B: Deterministic HTML5/CSS/SVG + Playwright -> FFmpeg (h264_videotoolbox) on Intel Mac."""

from __future__ import annotations

import math
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
RIG_DIR = REPO_ROOT / "assets" / "personagem" / "rig"
OUT_DIR = REPO_ROOT / "video-engine" / "_bench_out"
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1080px; height: 1920px; overflow: hidden;
    background: radial-gradient(circle at 50% 28%, #1e3a2f 0%, #0f1f1c 52%, #080d0e 100%);
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", sans-serif;
    color: #f8fafc;
  }
  .safe {
    position: absolute; left: 65px; top: 296px; width: 822px; height: 945px;
    display: flex; flex-direction: column; justify-content: space-between;
  }
  .pill {
    display: inline-flex; align-items: center; gap: 14px; align-self: flex-start;
    background: rgba(15, 23, 42, 0.86); border: 2px solid rgba(52, 211, 153, 0.55);
    border-radius: 999px; padding: 12px 26px; box-shadow: 0 14px 34px rgba(0,0,0,0.42);
  }
  .dot { width: 14px; height: 14px; border-radius: 99px; background: #34d399; box-shadow: 0 0 14px #34d399; }
  .card {
    margin-top: 22px; background: rgba(15, 23, 42, 0.82);
    border: 1.5px solid rgba(255,255,255,0.14); border-radius: 32px;
    padding: 32px 34px; box-shadow: 0 28px 60px rgba(0,0,0,0.5);
  }
  .nodes { display: flex; justify-content: space-between; gap: 14px; margin: 20px 0 32px; }
  .node { flex: 1; background: rgba(30, 41, 59, 0.88); border-radius: 22px; padding: 18px 16px; border: 2px solid #38bdf8; }
  .bar-bg { height: 22px; background: rgba(255,255,255,0.09); border-radius: 99px; overflow: hidden; margin-top: 6px; }
  .bottom { position: relative; height: 280px; display: flex; align-items: flex-end; }
  .rig { position: relative; width: 230px; height: 308px; flex-shrink: 0; }
  .rig img { position: absolute; inset: 0; width: 100%; height: 100%; }
  .cap {
    flex: 1; margin-left: 12px; margin-bottom: 34px;
    background: rgba(9, 13, 22, 0.90); border: 2px solid rgba(250, 204, 21, 0.45);
    border-radius: 24px; padding: 20px 24px; display: flex; justify-content: center; gap: 14px;
  }
</style>
</head>
<body>
  <svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;inset:0;opacity:0.26">
    <defs>
      <linearGradient id="mtGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#34d399" stop-opacity="0.35" />
        <stop offset="100%" stop-color="#080d0e" stop-opacity="0" />
      </linearGradient>
    </defs>
    <path id="mtPath" d="M0,980 L220,780 L460,910 L740,710 L1080,890 L1080,1500 L0,1500 Z" fill="url(#mtGrad)" />
  </svg>
  <div class="safe">
    <div class="pill" id="pill">
      <div class="dot"></div>
      <span style="font-size:27px;font-weight:800;color:#ecfdf5">TRILHA LEVE: 90% MENOS PESO NA MOCHILA</span>
    </div>
    <div class="card" id="card">
      <div style="font-size:24px;font-weight:700;color:#fbbf24;text-transform:uppercase;letter-spacing:1.2px">Como a Liofilização Funciona</div>
      <div class="nodes">
        <div class="node" id="n1" style="border-color:#38bdf8"><div style="font-size:25px;font-weight:800;color:#38bdf8">1. Gelo Rápido</div><div style="font-size:20px;color:#cbd5e1;margin-top:6px;font-weight:600">-40 °C preserva células</div></div>
        <div class="node" id="n2" style="border-color:#a78bfa"><div style="font-size:25px;font-weight:800;color:#a78bfa">2. Alto Vácuo</div><div style="font-size:20px;color:#cbd5e1;margin-top:6px;font-weight:600">Gelo vira vapor direto</div></div>
        <div class="node" id="n3" style="border-color:#34d399"><div style="font-size:25px;font-weight:800;color:#34d399">3. Crocante</div><div style="font-size:20px;color:#cbd5e1;margin-top:6px;font-weight:600">100% fruta · 0 água</div></div>
      </div>
      <div style="display:flex;flex-direction:column;gap:18px">
        <div>
          <div style="display:flex;justify-content:space-between;font-size:23px;font-weight:700"><span>Fruta In Natura (água pura)</span><span style="color:#f87171">500 g</span></div>
          <div class="bar-bg"><div id="bFresh" style="height:100%;width:0%;background:linear-gradient(90deg,#ef4444,#f97316);border-radius:99px"></div></div>
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;font-size:23px;font-weight:700"><span>Equivalente Liofilizado</span><span style="color:#34d399">50 g (-90%)</span></div>
          <div class="bar-bg"><div id="bFreeze" style="height:100%;width:0%;background:linear-gradient(90deg,#10b981,#34d399);border-radius:99px"></div></div>
        </div>
      </div>
    </div>
    <div class="bottom">
      <div class="rig" id="rig">
        <img src="__RIG__/torso_apontar.png" />
        <img src="__RIG__/cabeca_base.png" />
        <img src="__RIG__/antena_esq.png" />
        <img src="__RIG__/antena_dir.png" />
        <img id="lupa" src="__RIG__/haste_lupa.png" style="transform-origin:63.8% 15%" />
        <img src="__RIG__/sobrancelha_esq.png" />
        <img src="__RIG__/sobrancelha_dir.png" />
        <img id="visema" src="__RIG__/visemas/visema_X.png" />
      </div>
      <div class="cap" id="cap"></div>
    </div>
  </div>
<script>
const visemas = ["X", "A", "OU", "EI", "BMP", "FV", "SORRISO"];
const rigBase = "__RIG__";
const caps = [
  { s: 0, e: 29, w: ["Por", "que", "levar"], a: 1 },
  { s: 30, e: 59, w: ["90%", "menos", "peso"], a: 0 },
  { s: 60, e: 89, w: ["na", "sua", "mochila?"], a: 2 },
  { s: 90, e: 120, w: ["Sublimação", "a", "vácuo!"], a: 0 }
];
function springApprox(f) {
  if (f <= 0) return 0;
  const t = f / 24;
  return 1 - Math.exp(-8.5 * t) * Math.cos(10 * t);
}
window.__setFrame = function(frame) {
  const t = frame / 24;
  const cIn = Math.min(1.05, springApprox(frame));
  const s2 = Math.min(1.05, springApprox(frame - 24));
  const s3 = Math.min(1.05, springApprox(frame - 52));
  document.getElementById("pill").style.transform = `translateY(${(1-cIn)*-28}px) scale(${0.92+0.08*cIn})`;
  document.getElementById("pill").style.opacity = Math.min(1, cIn);
  document.getElementById("card").style.transform = `scale(${0.94+0.06*cIn})`;
  document.getElementById("card").style.opacity = Math.min(1, cIn);
  document.getElementById("n2").style.opacity = Math.min(1, s2);
  document.getElementById("n2").style.transform = `translateY(${(1-s2)*20}px)`;
  document.getElementById("n3").style.opacity = Math.min(1, s3);
  document.getElementById("n3").style.transform = `translateY(${(1-s3)*20}px)`;
  const bf = Math.max(0, Math.min(100, ((frame - 10) / 35) * 100));
  const bfr = Math.max(0, Math.min(12, ((frame - 28) / 37) * 12));
  document.getElementById("bFresh").style.width = bf + "%";
  document.getElementById("bFreeze").style.width = bfr + "%";
  document.getElementById("rig").style.transform = `translateY(${Math.sin(t*2.6)*4}px)`;
  document.getElementById("lupa").style.transform = `rotate(${-8 + Math.sin(t*2.1)*6}deg)`;
  const v = visemas[Math.floor(frame / 4) % visemas.length];
  document.getElementById("visema").src = rigBase + "/visemas/visema_" + v + ".png";
  const c = caps.find(x => frame >= x.s && frame <= x.e) || caps[0];
  document.getElementById("cap").innerHTML = c.w.map((word, i) => {
    const act = i === c.a;
    return `<span style="font-size:44px;font-weight:900;color:${act?'#facc15':'#fff'};text-decoration:${act?'underline':'none'};text-underline-offset:8px;transform:scale(${act?1.07:1});display:inline-block">${word}</span>`;
  }).join("");
};
</script>
</body>
</html>
"""


def _render_chunk(html_path: Path, start_f: int, end_f: int) -> list[bytes]:
    frames: list[bytes] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        page.goto(f"file://{html_path}", wait_until="load")
        for f in range(start_f, end_f):
            page.evaluate(f"window.__setFrame({f})")
            frames.append(page.screenshot(type="jpeg", quality=94))
        browser.close()
    return frames


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html_file = OUT_DIR / "bench_scene.html"
    html_file.write_text(HTML_TEMPLATE.replace("__RIG__", RIG_DIR.as_uri()), encoding="utf-8")
    out_mp4 = OUT_DIR / "playwright_bench.mp4"

    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=2) as ex:
        fut1 = ex.submit(_render_chunk, html_file, 0, 60)
        fut2 = ex.submit(_render_chunk, html_file, 60, 120)
        all_frames = fut1.result() + fut2.result()

    proc = subprocess.Popen(
        [
            "ffmpeg",
            "-y",
            "-f",
            "image2pipe",
            "-vcodec",
            "mjpeg",
            "-r",
            "24",
            "-i",
            "-",
            "-c:v",
            "h264_videotoolbox",
            "-b:v",
            "6M",
            "-pix_fmt",
            "yuv420p",
            str(out_mp4),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    assert proc.stdin is not None
    for buf in all_frames:
        proc.stdin.write(buf)
    proc.stdin.close()
    proc.wait()
    elapsed = time.perf_counter() - t0
    print(f"PLAYWRIGHT_ELAPSED={elapsed:.3f}")


if __name__ == "__main__":
    main()
