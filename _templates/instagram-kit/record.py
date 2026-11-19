"""Record post 2 (workshop opening, 1080x1350, ~8 s) and post 3 (Reel 1080x1920, ~16 s) + reel cover."""
import os, sys, time, glob, shutil, subprocess
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np

R = "/home/claude/1294962213sh.github.io"; OUT = "/home/claude/ig/v4"; TMP = "/home/claude/ig/tools/kit/tmp"
os.makedirs(TMP, exist_ok=True)

REEL_HTML = f"""<!doctype html><html><head><meta charset="utf-8">
<style>
*{{box-sizing:border-box;margin:0}} html,body{{width:1080px;height:1920px;overflow:hidden}}
body{{background:radial-gradient(130% 60% at 50% 0%, #F6EFE3 0%, #EFE6D6 55%, #ECE1CF 100%);font-family:Jost,sans-serif;position:relative}}
.cap{{position:absolute;top:118px;left:60px;right:60px;text-align:center;font:italic 400 56px/1.25 "Cormorant Garamond",serif;color:#4A1221;transition:opacity .5s}}
.phone{{position:absolute;left:152px;top:300px;width:776px;border-radius:66px;padding:8px;background:linear-gradient(160deg,#3a322f,#241f1d);box-shadow:0 40px 90px rgba(90,60,40,.3),0 0 0 1px rgba(255,255,255,.06) inset}}
.screen{{width:760px;height:1500px;border-radius:58px;overflow:hidden;background:#3a0f1b;position:relative}}
.screen iframe{{position:absolute;top:0;left:0;width:390px;height:770px;border:0;transform:scale(1.9487);transform-origin:top left}}
.foot{{position:absolute;left:0;right:0;bottom:52px;text-align:center;font:500 16px/1 Jost;letter-spacing:.3em;text-transform:uppercase;color:#A28D56}}
</style></head><body>
<p class="cap" id="cap">I describe the party.</p>
<div class="phone"><div class="screen"><iframe id="f" src="file://{R}/demo/index.html"></iframe></div></div>
<p class="foot">Invite as Art · Custom animated invitations · No app for your guests</p>
</body></html>"""

def first_live_frame(path):
    """index of the first frame that isn't blank/white (recording starts before paint)."""
    os.makedirs(f"{TMP}/scan", exist_ok=True)
    for f in glob.glob(f"{TMP}/scan/*.png"): os.remove(f)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-t", "2", "-vf", "fps=25,scale=108:-1", f"{TMP}/scan/%03d.png"], check=True)
    for k, f in enumerate(sorted(glob.glob(f"{TMP}/scan/*.png"))):
        a = np.asarray(Image.open(f).convert("L")).astype(int)
        if a.std() > 6 and a.mean() < 245: return k / 25.0
    return 0.0

def encode(webm, out, size, start, dur):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.2f}", "-i", webm, "-t", f"{dur}", "-vf", f"scale={size},fps=30,format=yuv420p",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-movflags", "+faststart", "-an", out], check=True)

def record_post2(p):
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1080, "height": 1350}, record_video_dir=f"{TMP}/vid2", record_video_size={"width": 1080, "height": 1350})
    pg = ctx.new_page()
    pg.add_init_script("(()=>{const z=()=>{if(document.documentElement){document.documentElement.style.zoom='2.5'}};z();document.addEventListener('DOMContentLoaded',z)})()")
    pg.goto(f"file://{R}/demo-workshop/index.html")
    pg.wait_for_timeout(11800)
    pg.screenshot(path=f"{TMP}/p2-last.png")
    ctx.close(); b.close()
    webm = glob.glob(f"{TMP}/vid2/*.webm")[-1]
    t0 = first_live_frame(webm); print("post2 first live frame at", t0)
    encode(webm, f"{OUT}/post-2-workshop.mp4", "1080:1350", t0 + 0.3, 10.0)
    # cover / still fallback: full bloom
    Image.open(f"{TMP}/p2-last.png").convert("RGB").save(f"{OUT}/post-2-workshop.jpg", quality=93, subsampling=0)

def record_post3(p):
    open(f"{TMP}/reel.html", "w").write(REEL_HTML)
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1080, "height": 1920}, record_video_dir=f"{TMP}/vid3", record_video_size={"width": 1080, "height": 1920})
    pg = ctx.new_page(); pg.goto(f"file://{TMP}/reel.html")
    fr = pg.frame(name=None, url=lambda u: "demo/index.html" in u) if False else pg.frames[1]
    t = time.time()
    def at(sec):
        while time.time() - t < sec: time.sleep(0.02)
    at(2.0); pg.screenshot(path=f"{TMP}/reel-cover.png")
    at(3.2); pg.evaluate("document.getElementById('cap').innerHTML='I describe the party.<br>24h later: a live invite with RSVPs.'")
    y = fr.evaluate("document.querySelector('.rsvp').getBoundingClientRect().top + window.scrollY - 12")
    fr.evaluate("(y)=>window.scrollTo({top:y,behavior:'smooth'})", y)
    at(5.2); fr.click("#name"); fr.type("#name", "Claire", delay=110)
    at(7.2); fr.click("#att-yes")
    at(8.4); fr.click("#dinner")
    at(9.8); fr.click("#submit")
    at(11.6); pg.evaluate("document.getElementById('cap').innerHTML='No app for your guests.<br>Holiday party, Friendsgiving, New Year&rsquo;s Eve.'")
    at(12.8); fr.evaluate("window.scrollTo({top:0,behavior:'smooth'})")
    at(17.0)
    ctx.close(); b.close()
    webm = glob.glob(f"{TMP}/vid3/*.webm")[-1]
    t0 = first_live_frame(webm); print("post3 first live frame at", t0)
    encode(webm, f"{OUT}/post-3-reel.mp4", "1080:1920", t0 + 0.3, 16.2)
    Image.open(f"{TMP}/reel-cover.png").convert("RGB").save(f"{OUT}/post-3-reel-cover.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        which = sys.argv[1] if len(sys.argv) > 1 else "both"
        if which in ("2", "both"): record_post2(p)
        if which in ("3", "both"): record_post3(p)
