"""Post 8 footer, profile ring, highlight covers."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright
sys.path.insert(0, "/home/claude/ig/tools")
OUT = "/home/claude/ig/v4"; F = "/home/claude/ig/fonts"

def font(name, size, wght):
    f = ImageFont.truetype(f"{F}/{name}", size)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f

def tracked(d, xy, text, f, fill, tracking):
    widths = [d.textlength(ch, font=f) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x, y = xy[0] - total / 2, xy[1]
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=f, fill=fill); x += w + tracking

def post8_footer():
    p = f"{OUT}/post-8-not-a-template.jpg"
    im = Image.open(p).convert("RGB"); d = ImageDraw.Draw(im)
    y = 931 + 135
    d.rectangle((300, y - 16, 780, y + 16), fill=(250, 246, 235))
    tracked(d, (540, y - 7), "ONE LINK  ·  NO APP FOR YOUR GUESTS", font("Jost[wght].ttf", 14, 500), (162, 141, 86), 4.2)
    im.save(p, quality=93, subsampling=0); print("post 8 footer")

def profile_ring():
    im = Image.open(f"{OUT}/profile-picture.jpg").convert("RGB"); d = ImageDraw.Draw(im)
    W = im.width; r = int(W * .455)
    d.ellipse((W/2 - r, W/2 - r, W/2 + r, W/2 + r), outline=(168, 135, 63), width=9)
    r2 = r - 22
    d.ellipse((W/2 - r2, W/2 - r2, W/2 + r2, W/2 + r2), outline=(168, 135, 63, 120), width=3)
    im.save(f"{OUT}/profile-picture.jpg", quality=94, subsampling=0); print("profile ring")

ICONS = {
 "holiday": """<path d="M53 100 A 30 30 0 1 1 93 101" fill="none" stroke="#A8873F" stroke-width="1.3" stroke-linecap="round"/>
   <path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(54.1 94.3) rotate(180)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(48.9 100.9) rotate(256)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M51.5 97.6 l-2.2 2.8" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(49.7 89.9) rotate(194)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(43.1 95.1) rotate(270)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M46.4 92.5 l-2.8 2.2" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(46.4 84.5) rotate(208)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(38.8 87.9) rotate(284)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M42.6 86.2 l-3.2 1.4" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(44.6 78.5) rotate(222)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(36.3 79.9) rotate(298)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M40.5 79.2 l-3.4 0.6" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(44.3 72.2) rotate(236)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(35.9 71.6) rotate(312)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M40.1 71.9 l-3.5 -0.2" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(45.5 66.0) rotate(250)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(37.5 63.4) rotate(326)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M41.5 64.7 l-3.3 -1.1" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(48.1 60.3) rotate(264)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(41.0 55.9) rotate(340)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M44.6 58.1 l-3.0 -1.9" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(52.1 55.4) rotate(278)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(46.2 49.4) rotate(354)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M49.2 52.4 l-2.4 -2.5" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(57.1 51.7) rotate(292)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(52.9 44.4) rotate(368)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M55.0 48.0 l-1.8 -3.0" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(62.9 49.2) rotate(306)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(60.6 41.1) rotate(382)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M61.7 45.2 l-1.0 -3.4" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(69.1 48.2) rotate(320)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(68.8 39.8) rotate(396)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M69.0 44.0 l-0.1 -3.5" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(75.4 48.8) rotate(334)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(77.1 40.5) rotate(410)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M76.2 44.7 l0.7 -3.4" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(81.3 50.8) rotate(348)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(85.0 43.3) rotate(424)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M83.2 47.0 l1.5 -3.1" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(86.6 54.2) rotate(362)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(92.0 47.8) rotate(438)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M89.3 51.0 l2.2 -2.7" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(90.9 58.8) rotate(376)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(97.7 53.9) rotate(452)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M94.3 56.4 l2.8 -2.1" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(93.9 64.3) rotate(390)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(101.7 61.2) rotate(466)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M97.8 62.8 l3.2 -1.3" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(95.5 70.4) rotate(404)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(103.9 69.2) rotate(480)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M99.7 69.8 l3.5 -0.5" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(95.7 76.7) rotate(418)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(104.0 77.6) rotate(494)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M99.8 77.1 l3.5 0.4" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(94.2 82.8) rotate(432)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(102.1 85.7) rotate(508)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M98.2 84.3 l3.3 1.2" stroke="#A8873F" stroke-width=".8"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(91.4 88.4) rotate(446)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M0 0 Q 2.6 -1.6 5.2 0 Q 2.6 1.6 0 0 Z" transform="translate(98.4 93.1) rotate(522)" fill="none" stroke="#A8873F" stroke-width="1"/><path d="M94.9 90.8 l2.9 2.0" stroke="#A8873F" stroke-width=".8"/>
   <path d="M53 100 c-6 -4 -11 0 -7 4 c4 3 8 -1 7 -4 z M53 100 c6 -4 11 0 7 4 c-4 3 -8 -1 -7 -4 z" fill="none" stroke="#A8873F" stroke-width="1.1" stroke-linejoin="round"/>
   <path d="M53 102 l-3 8 M53 102 l3 8" stroke="#A8873F" stroke-width=".9" stroke-linecap="round"/>""",
 "workshops": """<g transform="translate(14 12) scale(1.05)" fill="none" stroke="#A8873F" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">
   <path d="M100 84 C 86 70, 70 52, 56 22"/><path d="M62 34 C 52 30, 46 34, 44 42 C 52 44, 60 40, 62 34 Z"/><path d="M70 48 C 60 46, 54 50, 52 58 C 60 60, 68 56, 70 48 Z"/>
   <path d="M80 62 C 70 60, 64 64, 62 72 C 70 74, 78 70, 80 62 Z"/><path d="M66 36 C 76 30, 84 32, 88 38 C 80 42, 72 42, 66 36 Z"/><path d="M76 52 C 86 46, 94 48, 98 54 C 90 58, 82 58, 76 52 Z"/>
   <path d="M58 26 C 62 18, 68 16, 74 18 C 70 24, 64 28, 58 26 Z"/><circle cx="54" cy="20" r="1.6" fill="#A8873F" stroke="none"/><circle cx="60" cy="14" r="1.2" fill="#A8873F" stroke="none"/></g>""",
 "rsvp": """<g fill="none" stroke="#A8873F" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
   <path d="M48 44 H92 Q92 70 70 76 Q48 70 48 44 Z"/><path d="M70 76 V100 M58 102 H82"/>
   <circle cx="63" cy="60" r="1.6"/><circle cx="74" cy="54" r="1.3"/><circle cx="68" cy="66" r="1.1"/><circle cx="79" cy="63" r="1.4"/>
   <path d="M30 40 l1.2 3 3 1.2 -3 1.2 -1.2 3 -1.2 -3 -3 -1.2 3 -1.2 z M106 50 l1 2.4 2.4 1 -2.4 1 -1 2.4 -1 -2.4 -2.4 -1 2.4 -1 z" fill="#A8873F" stroke="none"/></g>""",
 "order": """<g fill="none" stroke="#A8873F" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
   <rect x="36" y="48" width="68" height="46" rx="2"/><path d="M36 50 L70 76 L104 50"/><path d="M36 94 L60 70 M104 94 L80 70"/>
   <circle cx="70" cy="76" r="7" fill="#F3ECDD"/><path d="M70 72 l1.2 2.6 2.8 .4 -2 2 .5 2.8 -2.5 -1.3 -2.5 1.3 .5 -2.8 -2 -2 2.8 -.4 z" fill="#A8873F" stroke="none"/></g>""",
}

def highlight_covers():
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 540, "height": 540}, device_scale_factor=2)
        for name, svg in ICONS.items():
            html = f"""<html><body style="margin:0;width:540px;height:540px;background:#F3ECDD;display:grid;place-items:center">
            <svg viewBox="20 20 100 100" width="300" height="300" style="overflow:visible">{svg}</svg></body></html>"""
            pg.set_content(html); pg.wait_for_timeout(300)
            pg.screenshot(path=f"{OUT}/highlight-{name}.png")
        b.close()
    print("highlight covers")

if __name__ == "__main__":
    post8_footer(); profile_ring(); highlight_covers()
