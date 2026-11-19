"""Instagram kit v4 — static posts rendered from the updated local site pages.
Output: /home/claude/ig/v4/*.jpg (1080x1350).  Run with the repo at /home/claude/1294962213sh.github.io."""
import os, sys, time, json, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image

R = "/home/claude/1294962213sh.github.io"
OUT = "/home/claude/ig/v4"; TMP = "/home/claude/ig/tools/kit/tmp"
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)

FOOT = "Invite as Art · Custom animated invitations · No app for your guests"
BASE_CSS = """
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Jost:wght@400;500&display=swap">
<style>
:root{--wine:#4A1221;--gold:#A8873F;--foot:#A28D56;--ink:#2B2420;--soft:#6B5E55;--green:#26302A}
*{box-sizing:border-box;margin:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{background:radial-gradient(130% 70% at 50% 0%, #F6EFE3 0%, #EFE6D6 55%, #ECE1CF 100%);font-family:Jost,sans-serif;color:var(--ink);position:relative}
.eye{font:500 15px/1 Jost;letter-spacing:.32em;text-transform:uppercase;color:var(--gold);text-align:center}
h1{font:italic 500 78px/1.08 "Cormorant Garamond",serif;color:var(--wine);text-align:center;letter-spacing:-.005em}
h1.green{color:var(--green)}
.foot{position:absolute;left:0;right:0;bottom:46px;text-align:center;font:500 14px/1 Jost;letter-spacing:.3em;text-transform:uppercase;color:var(--foot)}
.phone{position:absolute;border-radius:54px;padding:8px;background:linear-gradient(160deg,#3a322f,#241f1d);box-shadow:0 34px 70px rgba(90,60,40,.28),0 0 0 1px rgba(255,255,255,.06) inset}
.screen{border-radius:46px;overflow:hidden;background:#3a0f1b;position:relative}
.screen iframe{position:absolute;top:0;left:0;width:390px;height:1000px;border:0;transform-origin:top left}
.card{box-shadow:0 22px 46px rgba(90,60,40,.2);border-radius:6px}
.pal{font:500 13px/1 Jost;letter-spacing:.28em;text-transform:uppercase;color:var(--soft);text-align:center}
.cap{font:italic 400 30px/1.35 "Cormorant Garamond",serif;color:var(--soft);text-align:center}
</style>"""

def page(html):  # full document
    return "<!doctype html><html><head><meta charset='utf-8'>" + BASE_CSS + "</head><body>" + html + f"<p class='foot'>{FOOT}</p></body></html>"

def phone(left, top, w, h, src, scale, cls=""):
    inner = w - 16
    return (f"<div class='phone {cls}' style='left:{left}px;top:{top}px;width:{w}px'>"
            f"<div class='screen' style='width:{inner}px;height:{h}px'>"
            f"<iframe src='{src}' style='transform:scale({scale});width:{inner/scale:.1f}px;height:{(h)/scale:.1f}px'></iframe></div></div>")

def render(name, html, b, wait=7500, pre=None):
    p = f"{TMP}/{name}.html"; open(p, "w").write(page(html))
    pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
    pg.goto("file://" + p); pg.wait_for_timeout(1200)
    if pre: pre(pg)
    pg.wait_for_timeout(wait)
    pg.screenshot(path=f"{TMP}/{name}.png"); pg.close()
    Image.open(f"{TMP}/{name}.png").convert("RGB").save(f"{OUT}/{name}.jpg", quality=93, subsampling=0)
    print("rendered", name)

def shoot_cards(b):
    """Each storefront card at 3x as an image, plus the RSVP panel in two states."""
    pg = b.new_page(viewport={"width": 1366, "height": 900}, device_scale_factor=3)
    pg.goto(f"file://{R}/invites/index.html"); pg.wait_for_timeout(7500)
    for n in ("holiday", "friends", "brunch", "nye"):
        pg.query_selector(f".swatch.s-{n} .sframe").screenshot(path=f"{TMP}/card-{n}.png")
    pg.close()
    pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=3)
    pg.goto(f"file://{R}/demo/index.html"); pg.wait_for_timeout(4000)
    pg.fill("#name", "Claire Morgan"); pg.click("#att-yes"); pg.click("#plus")
    pg.wait_for_timeout(300)
    if pg.is_visible("#diet"): pg.fill("#diet", "Vegetarian")
    pg.click("#dinner"); pg.wait_for_timeout(600)
    pg.query_selector(".rsvp").screenshot(path=f"{TMP}/rsvp-form.png")
    pg.click("#submit"); pg.wait_for_timeout(1600)
    pg.query_selector(".rsvp").screenshot(path=f"{TMP}/rsvp-thanks.png")
    pg.close()
    print("cards + rsvp shot")

def main(only=None):
    with sync_playwright() as p:
        b = p.chromium.launch()
        if not only: shoot_cards(b)
        demo = f"file://{R}/demo/index.html"; ws = f"file://{R}/demo-workshop/index.html"
        # ---- Post 1: hero
        cards = "".join(f"<img class='card' src='{TMP}/card-{n}.png' style='position:absolute;left:{x}px;top:{y}px;width:236px'>"
                        for n, x, y in (("holiday", 560, 438), ("friends", 816, 438), ("brunch", 560, 800), ("nye", 816, 800)))
        render("post-1-hero", f"""
          <p class='eye' style='position:absolute;top:118px;left:0;right:0'>Invite as Art · Holiday invitations</p>
          <h1 style='position:absolute;top:160px;left:0;right:0'>Made for your party.<br>Live in 24 hours.</h1>
          {phone(110, 438, 390, 740, demo, 0.96)}
          {cards}""", b)
        # ---- Post 4: four cards
        for n, eye, head, pal in (("holiday", "Holiday party", "For the holiday party, designed to your theme", "Burgundy · Gold"),
                                  ("friends", "Friendsgiving", "For Friendsgiving, designed to your theme", "Terracotta · Olive"),
                                  ("nye", "New Year's Eve", "For New Year's Eve, designed to your theme", "Nocturne · Gold"),
                                  ("brunch", "Family brunch", "For New Year's Day, designed to your theme", "Ivory · Apricot · Gold")):
            idx = {"holiday": 1, "friends": 2, "nye": 3, "brunch": 4}[n]
            render(f"post-4-{idx}-{ {1:'holiday',2:'friends',3:'nye',4:'brunch'}[idx] }", f"""
              <p class='eye' style='position:absolute;top:150px;left:0;right:0'>{eye}</p>
              <h1 style='position:absolute;top:186px;left:0;right:0;font-size:54px'>{head}</h1>
              <img class='card' src='{TMP}/card-{n}.png' style='position:absolute;left:300px;top:318px;width:480px'>
              <p class='pal' style='position:absolute;top:1078px;left:0;right:0'>{pal}</p>""", b, wait=1500)
        # ---- Post 5: save a seat (workshop booking panel, shifted up so the panel leads)
        def to_panel(pg):
            fr = pg.frames[1]
            y = fr.evaluate("document.querySelector('.rsvp').getBoundingClientRect().top + window.scrollY - 10")
            pg.evaluate("""(y)=>{const f=document.querySelector('iframe');const sc=1.035;f.style.height=(y+1100)+'px';f.style.top=(-y*sc)+'px';}""", y)
            pg.add_style_tag(content=".foot{display:none}")
        render("post-5-booking", f"""
          <p class='eye' style='position:absolute;top:120px;left:0;right:0'>For studios &amp; workshops</p>
          <h1 class='green' style='position:absolute;top:160px;left:0;right:0'>Guests save a seat<br>in one tap.</h1>
          {phone(330, 420, 420, 980, ws, 1.035)}""", b, pre=to_panel)
        # ---- Post 6: opens from WhatsApp
        render("post-6-phone", f"""
          <div style='position:absolute;left:88px;top:300px;width:420px'>
            <p class='eye' style='text-align:left;margin-bottom:26px'>One link · Nothing to install</p>
            <h1 style='text-align:left;font-size:68px;line-height:1.1'>Guests open it from WhatsApp or iMessage.</h1>
            <div style='width:150px;height:1px;background:var(--gold);margin:34px 0 30px;position:relative'><span style='position:absolute;left:64px;top:-9px;color:var(--gold);font-size:14px'>✦</span></div>
            <p class='cap' style='text-align:left;font-size:27px;color:#5a4f47'>No app, no account, no phone number. They tap, reply, and add it to their calendar.</p>
            <p class='cap' style='text-align:left;font-size:27px;color:#5a4f47;margin-top:22px'>Calendar and map buttons built in. It moves: bells swing, wine sways, sparkles twinkle.</p>
          </div>
          {phone(576, 150, 400, 1020, demo, 0.985)}""", b)
        # ---- Post 7: RSVP form + thanks card
        render("post-7-rsvp", f"""
          <p class='eye' style='position:absolute;top:118px;left:0;right:0'>RSVPs done for you</p>
          <h1 style='position:absolute;top:156px;left:0;right:0;font-size:56px'>Headcount, dietary notes,<br>one extra question.</h1>
          <img class='card' src='{TMP}/rsvp-form.png' style='position:absolute;left:92px;top:330px;width:470px;border-radius:12px'>
          <img class='card' src='{TMP}/rsvp-thanks.png' style='position:absolute;left:600px;top:470px;width:400px;border-radius:12px'>
          <p class='cap' style='position:absolute;left:600px;top:{470+330}px;width:400px;font-size:26px'>Guests see how many are coming, never who. You get a private guest list that updates itself.</p>""", b, wait=1500)
        b.close()

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
