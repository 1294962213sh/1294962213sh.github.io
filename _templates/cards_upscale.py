"""Storefront upscale pass (after holiday3.py):
#1 paper grain on every card, #2 firmer inks on the light cards, #4 calmer motion (half the twinkles,
slower loops), #3 one painterly element on Friendsgiving / NYE / brunch."""
import re, random, math, xml.etree.ElementTree as ET
REPO = "/home/claude/1294962213sh.github.io"
P = f"{REPO}/invites/index.html"
random.seed(11)
NS = "http://www.w3.org/2000/svg"

def ser(e):
    s = ET.tostring(e, encoding="unicode")
    return re.sub(r'\s?xmlns(:\w+)?="[^"]+"', '', s).replace("ns0:", "")

def dab(cx, cy, rx, ry, fill, op, rot, delay):
    return (f'<ellipse class="dab" style="animation-delay:{delay:.2f}s" cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
            f'fill="{fill}" fill-opacity="{op:.2f}" transform="rotate({rot:.0f} {cx:.1f} {cy:.1f})"/>')

def painterly_runner():
    """Friendsgiving: a soft olive/eucalyptus runner along the table with three pomegranates."""
    out = ['<g filter="url(#soft)">']
    for i in range(26):
        t = i / 25; x = 50 + 60 * t; y = 108 + 2.2 * math.sin(t * math.pi) + random.uniform(-1.2, 1.2)
        out.append(dab(x, y, random.uniform(3, 4.6), random.uniform(1.4, 2), random.choice(["#8A9A6E", "#6E7F5A", "#A7B48A"]), random.uniform(.3, .45), random.uniform(-25, 25), 1.5 + i * .03))
    out.append('</g><g filter="url(#brush)">')
    for i in range(34):
        t = i / 33; x = 48 + 64 * t; y = 107.5 + 2.4 * math.sin(t * math.pi) + random.uniform(-1.6, 1.6)
        out.append(dab(x, y, random.uniform(2.4, 3.6), random.uniform(.9, 1.3), random.choice(["#8A9A6E", "#A7B48A", "#C2CBAA", "#6E7F5A"]), random.uniform(.7, .9), random.uniform(-40, 40), 1.6 + i * .03))
    # a few leaves drooping over the table's front edge
    for x in (58, 74, 92, 104):
        for k in range(4):
            out.append(dab(x + k * 1.6 + random.uniform(-.5, .5), 112 + k * 2.4, 2.6, 1.0, random.choice(["#8A9A6E", "#A7B48A"]), .8, 70 + random.uniform(-10, 10), 2.3 + k * .06))
    out.append('</g>')
    for k, x in enumerate((64, 80, 96)):
        out.append(f'<g class="pop" style="animation-delay:{2.4 + k*.15:.2f}s;transform-origin:{x}px 105px">'
                   f'<circle cx="{x}" cy="105" r="3.2" fill="#C9774F" stroke="#A94A2E" stroke-width=".4"/>'
                   f'<circle cx="{x-1}" cy="104" r=".9" fill="#E4A27E" fill-opacity=".7"/>'
                   f'<path d="M{x-1} 102.2 L{x} 100.8 L{x+1} 102.2" fill="none" stroke="#A94A2E" stroke-width=".5"/></g>')
    return "".join(out)

def painterly_citrus():
    """Brunch: two painted orange halves and leaves at the front of the tray."""
    out = ['<g filter="url(#soft)">']
    for (cx, cy, r) in ((42, 118.5, 4.6), (51, 121.5, 3.6)):
        for i in range(10):
            a = random.uniform(0, 6.28); d = random.uniform(0, r * .7)
            out.append(dab(cx + d * math.cos(a), cy + d * math.sin(a), r * .7, r * .55, random.choice(["#E9A24F", "#F0B569", "#E2913B"]), .5, random.uniform(0, 180), 2.2 + i * .03))
    out.append('</g><g filter="url(#brush)">')
    for (cx, cy, r) in ((42, 118.5, 4.6), (51, 121.5, 3.6)):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#EBA24C" fill-opacity=".85"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r*.8:.1f}" fill="#F6C98A" fill-opacity=".9"/>')
        for k in range(8):
            a = k * math.pi / 4
            out.append(f'<path d="M{cx} {cy} L{cx + r*.78*math.cos(a):.1f} {cy + r*.78*math.sin(a):.1f}" stroke="#E2913B" stroke-width=".35" stroke-opacity=".7"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r=".7" fill="#E2913B" fill-opacity=".8"/>')
    for (x, y, rot) in ((36, 114.5, -35), (56.5, 117, 20), (47, 125, 60)):
        out.append(dab(x, y, 3.2, 1.3, "#8A9A6E", .85, rot, 2.5))
        out.append(dab(x + .4, y - .3, 2.2, .7, "#A7B48A", .8, rot, 2.55))
    out.append('</g>')
    return "".join(out)

def painted_gold_halo():
    """NYE: a soft painted gold light behind the champagne tower."""
    out = ['<g filter="url(#softer)">']
    for i in range(16):
        a = random.uniform(0, 6.28); d = random.uniform(0, 22)
        out.append(dab(80 + d * math.cos(a), 62 + d * .8 * math.sin(a), random.uniform(10, 18), random.uniform(5, 9), random.choice(["#D4B36A", "#F1D27E", "#B99245"]), random.uniform(.05, .11), random.uniform(-20, 20), .2 + i * .04))
    out.append('</g>')
    return "".join(out)

def rework(svg_text, name):
    root = ET.fromstring(svg_text.replace('<svg class="bg"', f'<svg xmlns="{NS}" class="bg"'))
    ch = list(root)
    out = []
    tw_seen = 0
    for k, el in enumerate(ch):
        cls = el.get("class", "")
        if "tw" in cls.split():
            tw_seen += 1
            if tw_seen % 2 == 0: continue             # half the twinkles
        if name == "friends" and k in (58, 59, 60, 61):   # old small runner + pomegranates
            if k == 58: out.append(painterly_runner())
            continue
        if name == "nye" and k == 4:                      # painted light goes under the confetti
            out.append(painted_gold_halo())
        out.append(ser(el))
        if name == "brunch" and k == 33:                  # after the tray + its line art
            out.append(painterly_citrus())
    s = "".join(out)
    if name == "friends": s = s.replace("#B9573A", "#A94A2E")
    if name == "brunch": s = s.replace("#C9A86A", "#B38F45").replace("#F3B86A", "#EBA24C")
    return '<svg class="bg" viewBox="0 0 160 240" aria-hidden="true" preserveAspectRatio="xMidYMid slice">' + s + '</svg>'

html = open(P).read().split("\n")
starts = [k for k, l in enumerate(html) if '<svg class="bg"' in l]
names = ["holiday", "friends", "brunch", "nye"]
# process from the bottom so line numbers stay valid
for st, name in reversed(list(zip(starts, names))):
    if name == "holiday": continue
    j = next(k for k in range(st, len(html)) if "</svg>" in html[k])
    html[st:j + 1] = [rework("\n".join(html[st:j + 1]), name)]
s = "\n".join(html)

# ---- CSS: firmer inks on the light cards
s = s.replace(".s-friends  { --bg: #F6EBDD; --fg: #4A2E22; --fg2: #7A5A48; --ac: #B9573A; }",
              ".s-friends  { --bg: #F5E8D8; --fg: #3B2318; --fg2: #6B4836; --ac: #A94A2E; }")
s = s.replace(".s-brunch   { --bg: #F4EADC; --fg: #4A3A30; --fg2: #8A6E5C; --ac: #C9A86A; }",
              ".s-brunch   { --bg: #F3E7D5; --fg: #3B2C22; --fg2: #7A5A44; --ac: #B38F45; }")
# ---- CSS: calmer motion (slower loops)
rep = {
 "animation: sweep 11s ease-in-out 3s infinite;": "animation: sweep 16s ease-in-out 4s infinite;",
 ".bg .fall { animation: fall 9s ease-in-out infinite; } .bg .f2 { animation-delay: 3s; animation-duration: 11s } .bg .f3 { animation-delay: 6s; animation-duration: 8s }":
 ".bg .fall { animation: fall 13s ease-in-out infinite; } .bg .f2 { animation-delay: 4s; animation-duration: 16s } .bg .f3 { animation-delay: 8s; animation-duration: 12s }",
 ".bg .bokeh { animation: bokeh 7s ease-in-out infinite; }": ".bg .bokeh { animation: bokeh 10s ease-in-out infinite; }",
 ".bg .tw { animation: twinkle 4s ease-in-out infinite; }": ".bg .tw { animation: twinkle 6.5s ease-in-out infinite; }",
 ".bg .strand { animation: swayz 6s ease-in-out infinite; }": ".bg .strand { animation: swayz 8s ease-in-out infinite; }",
 ".bg .wine { animation: slosh 3.6s linear infinite; } .bg .wine2 { animation: slosh 5s linear infinite reverse; }":
 ".bg .wine { animation: slosh 5.2s linear infinite; } .bg .wine2 { animation: slosh 7s linear infinite reverse; }",
 "swaycard 4.5s ease-in-out 3s infinite;": "swaycard 6.5s ease-in-out 3s infinite;",
 ".bg .sp { transform-box: view-box; animation: twinkle2 3.4s ease-in-out infinite; }": ".bg .sp { transform-box: view-box; animation: twinkle2 5.5s ease-in-out infinite; }",
 ".bg .s1 { animation-delay: .8s; animation-duration: 4.1s } .bg .s2 { animation-delay: 1.6s; animation-duration: 2.7s } .bg .s3 { animation-delay: 2.3s } .bg .s4 { animation-delay: 1.1s; animation-duration: 4.6s } .bg .s5 { animation-delay: 2.9s } .bg .s6 { animation-delay: .4s; animation-duration: 5.2s } .bg .s7 { animation-delay: 1.9s }":
 ".bg .s1 { animation-delay: .8s; animation-duration: 6.4s } .bg .s2 { animation-delay: 1.6s; animation-duration: 4.6s } .bg .s3 { animation-delay: 2.3s } .bg .s4 { animation-delay: 1.1s; animation-duration: 7.2s } .bg .s5 { animation-delay: 2.9s } .bg .s6 { animation-delay: .4s; animation-duration: 8s } .bg .s7 { animation-delay: 1.9s }",
 ".bg .bub { animation: rise2 3s ease-in infinite; }": ".bg .bub { animation: rise2 4.5s ease-in infinite; }",
 ".bg .bell { transform-box: view-box; animation: bellswing 3.6s ease-in-out infinite; }": ".bg .bell { transform-box: view-box; animation: bellswing 4.4s ease-in-out infinite; }",
}
for a, b in rep.items():
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
# ---- CSS: paper grain on every invitation card (felt, not seen)
GRAIN = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'>"
         "<filter id='g'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 0.5  0 0 0 0 0.45  0 0 0 0 0.38  0 0 0 1 0'/></filter>"
         "<rect width='220' height='220' filter='url(%23g)'/></svg>\")")
css_grain = ("  .swatch .sin::before { content: \"\"; position: absolute; inset: 0; pointer-events: none; z-index: 1; "
             f"background-image: {GRAIN}; opacity: .09; mix-blend-mode: multiply; }}\n"
             "  .swatch .stext { z-index: 2; }\n")
anchor = "  .swatch .stext { position: absolute;"
assert s.count(anchor) == 1
s = s.replace(anchor, css_grain + anchor)
open(P, "w").write(s)
print("storefront upscale pass written")
