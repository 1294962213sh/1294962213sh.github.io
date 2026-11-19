"""Holiday card v3 = v2 centre art (crescent wreath · gold wine glass · velvet bow · two bells)
+ the old card's corner garlands. Writes the card SVG into invites/index.html and emblem.svg
for the sample page. Pure-Python SVG generation (no deps)."""
import math, random, re, xml.etree.ElementTree as ET, sys

REPO = "/home/claude/1294962213sh.github.io"
SAGE = ["#4C6B55", "#6E8A6A", "#8FA585", "#A9BC9C"]
random.seed(7)

def centre_art(prefix="w"):
    """Centre art for viewBox 160x240; wreath centre (80,74) r31, open at the bottom."""
    cx, cy, R = 80.0, 74.0, 31.0
    out = []
    # --- wreath leaves: fine almond leaves along the arc 118° → 388°, alternating sides
    leaves = []
    a0, a1 = 118, 388
    n = 58
    out.append(f'<path class="lf" style="animation-delay:.8s" d="M{cx+R*math.cos(math.radians(a0)):.2f} {cy+R*math.sin(math.radians(a0)):.2f} A{R} {R} 0 1 1 {cx+R*math.cos(math.radians(a1)):.2f} {cy+R*math.sin(math.radians(a1)):.2f}" fill="none" stroke="#4C6B55" stroke-width=".55" stroke-opacity=".9"/>')
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        side = 1 if i % 2 == 0 else -1
        rr = R + side * 1.5 + random.uniform(-.3, .3)
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        tangent = math.degrees(a) + 90 + side * random.uniform(18, 34)
        L = random.uniform(3.9, 5.3); W = random.uniform(1.5, 2.0)
        col = random.choice(SAGE); op = random.uniform(.78, .95)
        delay = .9 + 1.1 * i / n
        # almond leaf: two quadratic arcs
        d = f"M0 0 Q {L*.5:.2f} {-W:.2f} {L:.2f} 0 Q {L*.5:.2f} {W:.2f} 0 0 Z"
        leaves.append(f'<g class="lf" style="animation-delay:{delay:.2f}s"><path transform="translate({x:.2f} {y:.2f}) rotate({tangent:.1f})" d="{d}" fill="{col}" fill-opacity="{op:.2f}"/>'
                      f'<path transform="translate({x:.2f} {y:.2f}) rotate({tangent:.1f})" d="M0.6 0 H{L-.6:.2f}" stroke="#2F4A3A" stroke-width=".25" stroke-opacity=".5"/></g>')
    out += leaves
    # eucalyptus dots (soft round leaves) tucked between
    for i in range(14):
        a = math.radians(a0 + (a1 - a0) * (i + .5) / 14)
        rr = R + random.choice([-2.8, 3.0])
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        out.append(f'<circle class="lf" style="animation-delay:{1.6 + i*.06:.2f}s" cx="{x:.2f}" cy="{y:.2f}" r="{random.uniform(1.1,1.5):.2f}" fill="{random.choice(SAGE[2:])}" fill-opacity=".8"/>')
    # 5 small berry clusters
    for k, ang in enumerate([150, 205, 262, 318, 365]):
        a = math.radians(ang); x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        cl = [f'<g class="pop" style="animation-delay:{2.0 + k*.12:.2f}s;transform-origin:{x:.1f}px {y:.1f}px">']
        for dx, dy in [(-1.3, .6), (1.2, .2), (0, -1.3)]:
            c = "#9E1C30" if (dx + dy) < 0 else "#B3263A"
            cl.append(f'<circle cx="{x+dx:.2f}" cy="{y+dy:.2f}" r="1.15" fill="{c}"/><circle cx="{x+dx-.35:.2f}" cy="{y+dy-.4:.2f}" r=".3" fill="#FFE9D6" fill-opacity=".8"/>')
        cl.append('</g>'); out.append("".join(cl))
    # --- wine glass (slim gold line art), wine sloshing inside
    bowl = "M73.2 50 C 68.5 57, 68.6 66, 72.6 71.2 Q 80 77 87.4 71.2 C 91.4 66, 91.5 57, 86.8 50 Z"
    out.append(f'<defs><clipPath id="{prefix}bowl"><path d="{bowl}"/></clipPath>'
               f'<radialGradient id="{prefix}bell" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#FBE9B0"/><stop offset=".55" stop-color="#D9B45E"/><stop offset="1" stop-color="#A9822F"/></radialGradient></defs>')
    out.append(f'<g clip-path="url(#{prefix}bowl)"><g class="liquid wine-liquid" style="transform-origin:80px 76px">'
               '<path class="wine" d="M30 63.5 Q36 62 42 63.5 T54 63.5 T66 63.5 T78 63.5 T90 63.5 T102 63.5 T114 63.5 T126 63.5 T138 63.5 V80 H30 Z" fill="#9A1834"/>'
               '<path class="wine wine2" d="M30 64.6 Q36 66 42 64.6 T54 64.6 T66 64.6 T78 64.6 T90 64.6 T102 64.6 T114 64.6 T126 64.6 T138 64.6 V80 H30 Z" fill="#C02A48" opacity=".5"/>'
               '</g></g>')
    out.append(f'<g fill="none" stroke="#D6B36A" stroke-width=".9" stroke-linecap="round"><path class="draw" d="{bowl}"/>'
               '<path class="draw" d="M80 77 V93.5 M74.5 95 H85.5"/></g>')
    out.append('<path class="glint2" d="M74.5 54 Q73.5 61 75.5 67" fill="none" stroke="#FFF4D6" stroke-width=".9" stroke-linecap="round" opacity="0"/>')
    # --- velvet bow at the lower-left end of the crescent (angle 118°)
    bx, by = cx + R * math.cos(math.radians(118)), cy + R * math.sin(math.radians(118))
    out.append(f'<g class="pop" style="animation-delay:2.5s;transform-origin:{bx:.1f}px {by:.1f}px">'
               f'<path d="M{bx:.2f} {by:.2f} C {bx-4.5:.2f} {by-5.5:.2f}, {bx-9:.2f} {by-2:.2f}, {bx-4.2:.2f} {by+.6:.2f} Q {bx-2:.2f} {by+1.4:.2f} {bx:.2f} {by:.2f} Z" fill="#8E1B33"/>'
               f'<path d="M{bx:.2f} {by:.2f} C {bx+4.5:.2f} {by-5.5:.2f}, {bx+9:.2f} {by-2:.2f}, {bx+4.2:.2f} {by+.6:.2f} Q {bx+2:.2f} {by+1.4:.2f} {bx:.2f} {by:.2f} Z" fill="#8E1B33"/>'
               f'<path d="M{bx-1.6:.2f} {by-1.6:.2f} C {bx-4:.2f} {by-3.6:.2f}, {bx-6.4:.2f} {by-2.4:.2f}, {bx-4:.2f} {by-.6:.2f}" fill="none" stroke="#B3263A" stroke-width=".45" stroke-opacity=".8"/>'
               f'<path d="M{bx+1.6:.2f} {by-1.6:.2f} C {bx+4:.2f} {by-3.6:.2f}, {bx+6.4:.2f} {by-2.4:.2f}, {bx+4:.2f} {by-.6:.2f}" fill="none" stroke="#B3263A" stroke-width=".45" stroke-opacity=".8"/>'
               f'<path d="M{bx-.8:.2f} {by+.8:.2f} l-2.4 6.2 l1.9 -.5 l1.1 -5.3 Z M{bx+.8:.2f} {by+.8:.2f} l2.6 6 l-1.9 -.4 l-1.3 -5.2 Z" fill="#7A1630"/>'
               f'<ellipse cx="{bx:.2f}" cy="{by:.2f}" rx="1.5" ry="1.2" fill="#5E0F24"/></g>')
    # --- two gold jingle bells hanging from the knot, swinging
    for j, (dx, dy, ph) in enumerate([(-4.2, 11.8, 0), (2.4, 13.4, 1.6)]):
        kx, ky = bx, by + 1
        ex, ey = bx + dx, by + dy
        out.append(f'<g class="bell" style="transform-origin:{kx:.1f}px {ky:.1f}px;animation-delay:{ph}s">'
                   f'<path d="M{kx:.2f} {ky:.2f} L{ex:.2f} {ey-3.2:.2f}" stroke="#D6B36A" stroke-width=".45" fill="none"/>'
                   f'<circle cx="{ex:.2f}" cy="{ey:.2f}" r="2.6" fill="url(#{prefix}bell)"/>'
                   f'<path d="M{ex-1.3:.2f} {ey+1.1:.2f} h2.6" stroke="#8C6A24" stroke-width=".5" stroke-linecap="round"/>'
                   f'<circle cx="{ex:.2f}" cy="{ey+2.4:.2f}" r=".55" fill="#8C6A24"/></g>')
    # --- three tiny sparkles
    for k, (sx, sy, s) in enumerate([(114, 48, 2.2), (46, 92, 1.8), (118, 98, 1.9)]):
        d = f"M{sx} {sy-s} L{sx+s*.35:.2f} {sy-s*.35:.2f} L{sx+s} {sy} L{sx+s*.35:.2f} {sy+s*.35:.2f} L{sx} {sy+s} L{sx-s*.35:.2f} {sy+s*.35:.2f} L{sx-s} {sy} L{sx-s*.35:.2f} {sy-s*.35:.2f} Z"
        out.append(f'<path class="sp s{k*2}" style="transform-origin:{sx}px {sy}px" d="{d}" fill="#F6E3A8"/>')
    return "\n".join(out)

def build_card():
    html = open(f"{REPO}/invites/index.html").read().split("\n")
    # find the holiday card svg (first <svg class="bg") and its closing line
    i = next(k for k, l in enumerate(html) if '<svg class="bg"' in l)
    j = next(k for k in range(i, len(html)) if "</svg>" in html[k])
    svg = "\n".join(html[i:j + 1]).replace('<svg class="bg"', '<svg xmlns="http://www.w3.org/2000/svg" class="bg"')
    root = ET.fromstring(svg)
    ch = list(root)
    keep, garland = [], []
    for k, el in enumerate(ch):
        tag = el.tag.split('}')[-1]; cls = el.get("class", ""); d = el.get("d", "")
        if k <= 3: keep.append(el); continue                         # defs, ground, wash, bokeh
        if 4 <= k <= 31: garland.append(el); continue                 # corner garlands + berries
        if tag == "rect" and el.get("fill") == "none": keep.append(el); continue   # gold frame
        # everything else (string lights, twinkles, old glass, sparkles) is dropped
    # deepen the berries to the card's own wine red
    for el in garland:
        for c in el.iter():
            if c.get("fill") == "#C73D58": c.set("fill", "#A8233C")
    # serialise: ground layers, then garlands clipped inside the outer frame line, then frame, then centre art
    def ser(e):
        s = ET.tostring(e, encoding="unicode")
        return re.sub(r'\s?xmlns(:\w+)?="[^"]+"', '', s).replace("ns0:", "")
    keep[0] = ET.fromstring(re.sub(r'<ns0:clipPath id="hpbowl">.*?</ns0:clipPath>', '', ET.tostring(keep[0], encoding='unicode'), flags=re.S))
    parts = [ser(e) for e in keep[:4]]
    parts.append('<clipPath id="hpin"><rect x="7.5" y="7.5" width="145" height="225"/></clipPath>')
    parts.append('<g clip-path="url(#hpin)">' + "".join(ser(e) for e in garland) + '</g>')
    parts += [ser(e) for e in keep[4:]]
    parts.append(centre_art("hp3"))
    new_svg = ('<svg class="bg" viewBox="0 0 160 240" aria-hidden="true" preserveAspectRatio="xMidYMid slice">'
               + "".join(parts) + '</svg>')
    html[i:j + 1] = [new_svg]
    open(f"{REPO}/invites/index.html", "w").write("\n".join(html))
    # standalone emblem for the sample page (centre art only, cropped)
    emblem = ('<svg class="glass wreath-emblem" viewBox="40 36 80 88" aria-hidden="true">' + centre_art("em") + '</svg>')
    open("/home/claude/ig/site/emblem.svg", "w").write(emblem)
    print("card written; emblem.svg written")

if __name__ == "__main__":
    build_card()
