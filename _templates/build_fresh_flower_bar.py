"""Fresh Flower Bar preview, v2: an Old Master-style floral still life on a light parchment ground.
Blooms open from buds (petal by petal), leaves grow, a butterfly visits, champagne fills, dust drifts in the light.
Built from demo/index.html (the holiday sample). Output: fresh-flower-bar/index.html (+ preview.jpg made separately)."""
import math, random, re, pathlib

random.seed(23)
REPO = pathlib.Path('/home/claude/1294962213sh.github.io')
src = (REPO / 'demo/index.html').read_text()

def f(x): return f"{x:.2f}"

# ------------------------------------------------------------------ palettes (base → mid → edge), lit and shaded variants
PAL = {
  "peony":   dict(lit=("#E9B9AE", "#F4D6CA", "#FBEDE4"), shd=("#C98E88", "#E3B6AC", "#F1D6CB"), heart="#D9937F", st="#C7867E"),
  "oldrose": dict(lit=("#D98B8E", "#EAB0AE", "#F5D2CC"), shd=("#B5686E", "#D08F90", "#E8B7B3"), heart="#A4505C", st="#B8707A"),
  "crimson": dict(lit=("#8E2F42", "#B94D5B", "#D47A86"), shd=("#5E1C2C", "#8E2F42", "#B94D5B"), heart="#4A1522", st="#6E2436"),
  "ivory":   dict(lit=("#E9D6BE", "#F6EBD9", "#FFFBF2"), shd=("#CDB69A", "#E6D4BB", "#F5EAD8"), heart="#D9B98E", st="#CDB69A"),
  "coral":   dict(lit=("#D4654A", "#EC8A6C", "#F7B9A2"), shd=("#AD4A35", "#D4654A", "#EC8A6C"), heart="#8E3322", st="#B4503C"),
  "gold":    dict(lit=("#D3A646", "#E9C76A", "#F6E3A8"), shd=("#B38A34", "#D3A646", "#E9C76A"), heart="#8F6A20", st="#B38A34"),
  "leaf":    dict(lit=("#2F4B33", "#4C6B45", "#7E9A66"), shd=("#1F3324", "#2F4B33", "#4C6B45")),
}
# petal silhouettes, unit length (tip at 0,-1), width ~1
PETAL = {
  "round":  "M0 0 C-.62 -.16 -.6 -.74 -.2 -.98 Q0 -1.08 .2 -.98 C.6 -.74 .62 -.16 0 0 Z",
  "notch":  "M0 0 C-.64 -.16 -.62 -.72 -.3 -.93 Q-.14 -1.03 0 -.95 Q.14 -1.03 .3 -.93 C.62 -.72 .64 -.16 0 0 Z",
  "ruffle": "M0 0 C-.66 -.14 -.66 -.6 -.42 -.84 Q-.34 -.98 -.22 -.9 Q-.1 -1.04 0 -.94 Q.1 -1.04 .22 -.9 Q.34 -.98 .42 -.84 C.66 -.6 .66 -.14 0 0 Z",
  "tulip":  "M0 0 C-.5 -.08 -.56 -.74 -.36 -.98 L-.12 -.86 L0 -1.04 L.12 -.86 L.36 -.98 C.56 -.74 .5 -.08 0 0 Z",
  "leaf":   "M0 0 C-.38 -.28 -.46 -.72 0 -1 C.46 -.72 .38 -.28 0 0 Z",
}
defs = []
for name, p in PAL.items():
    for side in ("lit", "shd"):
        a, b, c = p[side]
        defs.append(f'<linearGradient id="g-{name}-{side}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="-1"><stop offset="0" stop-color="{a}"/><stop offset=".5" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></linearGradient>')
defs.append('<radialGradient id="g-cup" gradientUnits="userSpaceOnUse" cx="0" cy="0" r=".62"><stop offset="0" stop-color="#3A1E22" stop-opacity=".42"/><stop offset=".45" stop-color="#3A1E22" stop-opacity=".14"/><stop offset="1" stop-color="#3A1E22" stop-opacity="0"/></radialGradient>')
defs.append('<radialGradient id="g-hollow" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="1"><stop offset="0" stop-color="#2A1418" stop-opacity=".55"/><stop offset=".55" stop-color="#2A1418" stop-opacity=".2"/><stop offset="1" stop-color="#2A1418" stop-opacity="0"/></radialGradient>')
for k, d in PETAL.items():
    defs.append(f'<path id="p-{k}" d="{d}"/>')

LIGHT_ANGLE = -125  # light from upper-left (SVG y down)
def lit(angle):
    d = (angle - LIGHT_ANGLE + 180) % 360 - 180
    return abs(d) < 95

art = []     # bouquet layer (inside sway group)
t_bloom = [0.0]

def jitter_petal(shape, j=.07):
    """A unique, slightly irregular petal path (unit length), so no two petals are alike."""
    r = lambda k=1: random.uniform(-j, j) * k
    if shape == "ruffle":
        return (f"M0 0 C{-.66+r()} {-.14+r()} {-.66+r()} {-.6+r()} {-.42+r()} {-.84+r()} Q{-.34+r()} {-.98+r()} {-.22+r()} {-.9+r()} "
                f"Q{-.1+r()} {-1.04+r()} 0 {-.94+r()} Q{.1+r()} {-1.04+r()} {.22+r()} {-.9+r()} Q{.34+r()} {-.98+r()} {.42+r()} {-.84+r()} C{.66+r()} {-.6+r()} {.66+r()} {-.14+r()} 0 0 Z")
    if shape == "notch":
        return (f"M0 0 C{-.64+r()} {-.16+r()} {-.62+r()} {-.72+r()} {-.3+r()} {-.93+r()} Q{-.14+r()} {-1.03+r()} 0 {-.95+r()} "
                f"Q{.14+r()} {-1.03+r()} {.3+r()} {-.93+r()} C{.62+r()} {-.72+r()} {.64+r()} {-.16+r()} 0 0 Z")
    return (f"M0 0 C{-.62+r()} {-.16+r()} {-.6+r()} {-.74+r()} {-.2+r()} {-.98+r()} Q0 {-1.08+r()} {.2+r()} {-.98+r()} C{.6+r()} {-.74+r()} {.62+r()} {-.16+r()} 0 0 Z")

TIP = "M-.3 -.9 Q0 -1.02 .3 -.9"   # the lit edge along a petal's tip (local coords)

def flower(cx, cy, r, pal, kind="rose", t0=1.0, squash=.9, tilt=0, target=None):
    """A bloom that opens from a bud. kind: rose | peony | anemone | ranunculus. Local frame: flower center at 0,0."""
    target = art if target is None else target
    P = PAL[pal]
    g = [f'<g class="breathe" style="transform-origin:{f(cx)}px {f(cy)}px;animation-delay:-{random.uniform(0,7):.1f}s">',
         f'<g transform="translate({f(cx)} {f(cy)}) rotate({tilt}) scale(1 {squash})">']
    g.append(f'<ellipse class="bshadow" style="animation-delay:{t0+.6:.2f}s" cx="{f(r*.14)}" cy="{f(r*.2)}" rx="{f(r*1.0)}" ry="{f(r*.88)}" fill="#3A2A1E" fill-opacity=".25" filter="url(#blur3)"/>')
    # rings: (radius factor, count, length factor, width factor, shape) — wide petals that overlap
    if kind == "rose":
        rings = [(1.0, 7, .82, 1.1, "notch"), (.74, 6, .66, 1.05, "notch"), (.5, 5, .52, .95, "round"), (.3, 5, .38, .85, "round")]
    elif kind == "peony":
        rings = [(1.0, 8, .84, 1.0, "ruffle"), (.82, 8, .7, .95, "ruffle"), (.64, 7, .56, .9, "ruffle"), (.46, 7, .44, .85, "ruffle"), (.28, 6, .32, .75, "round")]
    elif kind == "anemone":
        rings = [(1.0, 7, .9, 1.15, "round"), (.84, 6, .76, 1.05, "round")]
    elif kind == "ranunculus":
        rings = [(1.0, 9, .64, .95, "round"), (.82, 9, .52, .9, "round"), (.64, 8, .42, .85, "round"), (.46, 7, .32, .8, "round"), (.3, 6, .24, .7, "round")]
    nr = len(rings)
    for ri, (rf, n, lf, wf, shape) in enumerate(rings):
        ring_delay = t0 + (nr - 1 - ri) * 0.28           # innermost first
        off = random.uniform(0, 360)
        for k in range(n):
            a = off + k * 360 / n + random.uniform(-10, 10)
            rr = r * rf * random.uniform(.94, 1.06)
            L = rr * lf; base = rr - L
            bx, by = base * math.cos(math.radians(a)), base * math.sin(math.radians(a))
            w = L * wf * random.uniform(.9, 1.1)
            side = "lit" if lit(a) else "shd"
            pd = ring_delay + random.uniform(0, .22)
            rot0 = random.uniform(-45, 45)
            tf = f'translate({f(bx)} {f(by)}) rotate({a+90+random.uniform(-6,6):.1f}) scale({f(w)} {f(L)})'
            d = jitter_petal(shape)
            g.append(f'<g class="pt" style="transform-origin:0px 0px;animation-delay:{pd:.2f}s;--r:{rot0:.0f}deg">'
                     f'<path d="{d}" transform="{tf}" fill="url(#g-{pal}-{side})" stroke="{P["st"]}" stroke-width=".3" vector-effect="non-scaling-stroke" stroke-opacity=".5"/>'
                     f'<path d="{d}" transform="{tf}" fill="url(#g-cup)"/>')
            if side == "lit" and ri < 2:
                g.append(f'<path d="{TIP}" transform="{tf}" fill="none" stroke="#FFFDF7" stroke-width=".8" vector-effect="non-scaling-stroke" stroke-opacity=".5" stroke-linecap="round"/>')
            g.append('</g>')
        if ri == nr - 2:   # the cup's shadow, under the innermost petals
            g.append(f'<circle class="pt" style="transform-origin:0px 0px;animation-delay:{ring_delay:.2f}s" r="{f(r*.46)}" fill="url(#g-hollow)"/>')
    # heart
    if kind == "anemone":
        g.append(f'<g class="pt" style="transform-origin:0px 0px;animation-delay:{t0:.2f}s"><circle r="{f(r*.3)}" fill="#2B1B24"/>' + ''.join(f'<circle cx="{f(r*.3*math.cos(math.radians(a)))}" cy="{f(r*.3*math.sin(math.radians(a)))}" r="{f(r*.045)}" fill="#5A3B4A"/>' for a in range(0, 360, 24)) + '</g>')
    else:
        for i in range(5):   # curled heart
            a = i * 72 + 20
            g.append(f'<g class="pt" style="transform-origin:0px 0px;animation-delay:{t0 - .1 + i*.04:.2f}s;--r:{-60+i*10}deg"><path d="{jitter_petal("round")}" transform="translate({f(r*.08*math.cos(math.radians(a)))} {f(r*.08*math.sin(math.radians(a)))}) rotate({a+140}) scale({f(r*.16)} {f(r*.22)})" fill="{P["heart"]}" fill-opacity=".95"/></g>')
    bud_col = P["shd"][1]
    g.append(f'<g class="bud" style="transform-origin:0px 0px;--d0:{t0-.55:.2f}s;--d1:{t0+.35:.2f}s">'
             f'<ellipse cx="0" cy="{f(-r*.05)}" rx="{f(r*.3)}" ry="{f(r*.42)}" fill="{bud_col}"/>'
             f'<path d="M{f(-r*.3)} {f(r*.1)} Q0 {f(-r*.7)} {f(r*.3)} {f(r*.1)}" fill="{P["lit"][2]}" fill-opacity=".6"/>'
             + ''.join(f'<use href="#p-round" transform="rotate({a}) scale({f(r*.22)} {f(r*.5)})" fill="#4C6B45" fill-opacity=".95"/>' for a in (150, 180, 210)) + '</g>')
    g.append('</g></g>')
    target.append(''.join(g))

def tulip(cx, cy, size, ang, t0, flames=True, target=None):
    """A striped tulip cup pointing along ang (deg), opening from a tight bud."""
    target = art if target is None else target
    g = [f'<g class="breathe" style="transform-origin:{f(cx)}px {f(cy)}px;animation-delay:-{random.uniform(0,7):.1f}s"><g transform="translate({f(cx)} {f(cy)}) rotate({ang+90})">']
    for i, (dx, w, side, d) in enumerate([(-.22, .52, "shd", .5), (.22, .52, "lit", .5), (0, .62, "lit", 0)]):
        g.append(f'<g class="pt" style="transform-origin:0px 0px;animation-delay:{t0+d:.2f}s;--r:{dx*40:.0f}deg">'
                 f'<use href="#p-tulip" transform="translate({f(dx*size)} 0) rotate({dx*28:.0f}) scale({f(size*w)} {f(size)})" fill="url(#g-coral-{side})" stroke="#9C3A2C" stroke-width=".35" vector-effect="non-scaling-stroke" stroke-opacity=".6"/>')
        if flames:  # ivory feathering
            g.append(f'<path d="M{f(dx*size)} 0 q{f(size*.08)} {f(-size*.3)} 0 {f(-size*.55)} q{f(-size*.06)} {f(-size*.2)} {f(size*.04)} {f(-size*.4)}" fill="none" stroke="#F6E6D4" stroke-width="{f(size*.11)}" stroke-opacity=".8" stroke-linecap="round" transform="rotate({dx*28:.0f} {f(dx*size)} 0)"/>')
        g.append('</g>')
    g.append(f'<g class="bud" style="transform-origin:0px 0px;--d0:{t0-.5:.2f}s;--d1:{t0+.3:.2f}s"><use href="#p-tulip" transform="scale({f(size*.42)} {f(size*.9)})" fill="#4C6B45"/></g>')
    g.append('</g></g>')
    target.append(''.join(g))

def leaf(x, y, ang, L, t0, w=.4, target=None):
    target = art if target is None else target
    side = "lit" if lit(ang) else "shd"
    j = lambda: random.uniform(-.06, .06)
    d = f"M0 0 C{-.42+j()} {-.22+j()} {-.5+j()} {-.62+j()} {-.08+j()} {-.98} L0 -1.04 L{.08+j()} {-.98} C{.5+j()} {-.62+j()} {.42+j()} {-.22+j()} 0 0 Z"
    tf = f'translate({f(x)} {f(y)}) rotate({ang+90:.1f}) scale({f(L*w)} {f(L)})'
    target.append(f'<g class="lf" style="transform-origin:{f(x)}px {f(y)}px;animation-delay:{t0:.2f}s">'
                  f'<path d="{d}" transform="{tf}" fill="url(#g-leaf-{side})" stroke="#1B2C20" stroke-width=".3" vector-effect="non-scaling-stroke" stroke-opacity=".55"/>'
                  f'<path d="M0 0 C-.42 -.22 -.5 -.62 -.08 -.98 L0 -1.04 L0 0 Z" transform="{tf}" fill="#0F1C14" fill-opacity="{.18 if side=="lit" else .3}"/>'
                  f'<path d="M0 -.04 L0 -.96" transform="{tf}" fill="none" stroke="#B9C9A0" stroke-width=".5" vector-effect="non-scaling-stroke" stroke-opacity=".55"/></g>')

def stem(x0, y0, x1, y1, t0, bend=10, target=None, col="#3B4D36", wdt=1.2):
    target = art if target is None else target
    mx, my = (x0 + x1) / 2 + bend, (y0 + y1) / 2
    target.append(f'<path class="stem" style="animation-delay:{t0:.2f}s" d="M{f(x0)} {f(y0)} Q{f(mx)} {f(my)} {f(x1)} {f(y1)}" fill="none" stroke="{col}" stroke-width="{wdt}" stroke-linecap="round"/>')

def spray(x0, y0, ang, L, t0, col="#FFFDF6", n=6, target=None):
    """A thin arching stem with tiny white/blue florets that pop along it."""
    target = art if target is None else target
    pts = [(x0 + math.cos(math.radians(ang + 25*t)) * L * t, y0 + math.sin(math.radians(ang + 25*t)) * L * t) for t in [i/n for i in range(n+1)]]
    target.append(f'<path class="stem" style="animation-delay:{t0:.2f}s" d="M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts) + '" fill="none" stroke="#4C6B45" stroke-width=".7" stroke-linecap="round"/>')
    for i, (x, y) in enumerate(pts[1:], 1):
        target.append(f'<g class="pt" style="transform-origin:{f(x)}px {f(y)}px;animation-delay:{t0+.5+i*.08:.2f}s">' + ''.join(
            f'<ellipse cx="{f(x+math.cos(math.radians(a))*1.6)}" cy="{f(y+math.sin(math.radians(a))*1.6)}" rx="1.5" ry=".9" fill="{col}" fill-opacity=".95" transform="rotate({a} {f(x+math.cos(math.radians(a))*1.6)} {f(y+math.sin(math.radians(a))*1.6)})"/>' for a in range(0, 360, 72)) + f'<circle cx="{f(x)}" cy="{f(y)}" r=".6" fill="#E9C76A"/></g>')


def vine(x0, y0, ang, L, t0, target=None):
    """A trailing eucalyptus sprig: curved stem with pairs of round leaves that pop along it."""
    target = art if target is None else target
    n = 9
    pts = [(x0 + math.cos(math.radians(ang + 30*t)) * L * t, y0 + math.sin(math.radians(ang + 30*t)) * L * t) for t in [i/n for i in range(n+1)]]
    target.append(f'<path class="stem" style="animation-delay:{t0:.2f}s" d="M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts) + '" fill="none" stroke="#56705A" stroke-width=".9" stroke-linecap="round"/>')
    for i, (x, y) in enumerate(pts[1:], 1):
        t = i / n; a = ang + 30 * t
        for side in (-1, 1):
            la = a + side * 75; rr = 4.6 * (1 - t * .35)
            ex, ey = x + math.cos(math.radians(la)) * rr * .9, y + math.sin(math.radians(la)) * rr * .9
            col = random.choice(["#8FA98F", "#A6BBA3", "#7E9A86", "#B8C9B2"])
            target.append(f'<g class="pt" style="transform-origin:{f(x)}px {f(y)}px;animation-delay:{t0+.4+i*.09:.2f}s"><ellipse cx="{f(ex)}" cy="{f(ey)}" rx="{f(rr)}" ry="{f(rr*.82)}" fill="{col}" stroke="#4C6B45" stroke-width=".3" stroke-opacity=".5"/><ellipse cx="{f(ex-rr*.3)}" cy="{f(ey-rr*.3)}" rx="{f(rr*.4)}" ry="{f(rr*.25)}" fill="#FFFFFF" fill-opacity=".28"/></g>')

def berries(x0, y0, ang, L, t0, target=None):
    """Winterberry: a dark twig with a cluster of glossy red berries that pop in."""
    target = art if target is None else target
    x1, y1 = x0 + math.cos(math.radians(ang)) * L, y0 + math.sin(math.radians(ang)) * L
    target.append(f'<path class="stem" style="animation-delay:{t0:.2f}s" d="M{f(x0)} {f(y0)} Q{f((x0+x1)/2 + 4)} {f((y0+y1)/2)} {f(x1)} {f(y1)}" fill="none" stroke="#4A2E24" stroke-width=".9" stroke-linecap="round"/>')
    for i in range(9):
        t = .45 + .55 * (i / 8)
        bx = x0 + (x1 - x0) * t + random.uniform(-4.5, 4.5); by = y0 + (y1 - y0) * t + random.uniform(-4.5, 4.5)
        r = random.uniform(1.6, 2.3); col = random.choice(["#B81F2E", "#C92C38", "#A4192A"])
        target.append(f'<g class="pt" style="transform-origin:{f(bx)}px {f(by)}px;animation-delay:{t0+.4+i*.07:.2f}s">'
                      f'<path d="M{f(bx)} {f(by)} L{f(x0+(x1-x0)*t)} {f(y0+(y1-y0)*t)}" stroke="#4A2E24" stroke-width=".5"/>'
                      f'<circle cx="{f(bx)}" cy="{f(by)}" r="{f(r)}" fill="{col}"/><circle cx="{f(bx+r*.3)}" cy="{f(by+r*.35)}" r="{f(r*.8)}" fill="#6E0F1C" fill-opacity=".35"/>'
                      f'<circle cx="{f(bx-r*.35)}" cy="{f(by-r*.4)}" r="{f(r*.32)}" fill="#FFE8E0" fill-opacity=".85"/></g>')


def pine(x, y, ang, L, t0, target=None):
    """A sprig of pine: a twig with soft needle pairs, grows out from the bouquet."""
    target = art if target is None else target
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    x1, y1 = x + ca * L, y + sa * L
    needles = []
    for i in range(1, 13):
        t = i / 12; px, py = x + ca * L * t, y + sa * L * t
        nl = 5.5 * (1 - t * .55)
        for side in (-1, 1):
            a = ang + side * (38 + random.uniform(-6, 6))
            needles.append(f'<path d="M{f(px)} {f(py)} L{f(px+math.cos(math.radians(a))*nl)} {f(py+math.sin(math.radians(a))*nl)}" stroke="{random.choice(["#2F4A35","#3B5A40","#27402E"])}" stroke-width=".8" stroke-linecap="round"/>')
    target.append(f'<g class="lf" style="transform-origin:{f(x)}px {f(y)}px;animation-delay:{t0:.2f}s"><path d="M{f(x)} {f(y)} L{f(x1)} {f(y1)}" stroke="#4A3A2A" stroke-width=".9" stroke-linecap="round"/>' + ''.join(needles) + '</g>')


def bauble(x, y, r, t0, target=None):
    """A small gold ornament on a pick, tucked into the bouquet; it catches the light now and then."""
    target = art if target is None else target
    target.append(f'<g class="pt" style="transform-origin:{f(x)}px {f(y)}px;animation-delay:{t0:.2f}s">'
                  f'<path d="M{f(x)} {f(y-r)} L{f(x)} {f(y-r-7)}" stroke="#8C7A66" stroke-width=".6"/>'
                  f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="url(#g-bauble)"/>'
                  f'<rect x="{f(x-1.3)}" y="{f(y-r-1.6)}" width="2.6" height="2" rx=".5" fill="#C9A24A"/>'
                  f'<ellipse cx="{f(x-r*.35)}" cy="{f(y-r*.4)}" rx="{f(r*.3)}" ry="{f(r*.2)}" fill="#FFF8DC" fill-opacity=".85" transform="rotate(-30 {f(x-r*.35)} {f(y-r*.4)})"/>'
                  f'<path class="gleam" d="M{f(x-r*.1)} {f(y-r*.2)} l1.2 0 l.35 1.2 l.35 -1.2 l1.2 0 l-1 -.75 l.4 -1.2 l-.95 .75 l-.95 -.75 l.4 1.2 Z" fill="#FFFBEA" style="transform-origin:{f(x+.7)}px {f(y-r*.2)}px;animation-delay:{random.uniform(0,5):.1f}s"/></g>')


defs.append('<radialGradient id="g-bauble" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#FFF1BF"/><stop offset=".35" stop-color="#E2B95C"/><stop offset=".8" stop-color="#9E7322"/><stop offset="1" stop-color="#6B4C12"/></radialGradient>')
defs.append('<radialGradient id="g-bulb" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFF6D9"/><stop offset=".35" stop-color="#FFE9A8" stop-opacity=".9"/><stop offset="1" stop-color="#FFD98A" stop-opacity="0"/></radialGradient>')

# ------------------------------------------------------------------ compose the bouquet (viewBox 0 0 320 250; ledge at y=196; vase mouth 160,150)
VX, VY = 160, 150
# stems first (drawn at ~0.2s)
for (x1, y1, bend) in [(116, 96, -8), (196, 86, 10), (162, 124, 0), (150, 70, 2), (108, 44, -14), (226, 112, 16), (168, 30, 6), (100, 132, -14), (212, 46, 12), (84, 80, -18), (240, 70, 18), (138, 136, -4), (204, 124, 8)]:
    stem(VX + random.uniform(-6, 6), VY, x1, y1, 0.15 + random.uniform(0, .3), bend)
# back leaves
for (x, y, ang, L, w) in [(146, 144, 205, 40, .42), (174, 142, -25, 42, .42), (152, 146, 240, 30, .4), (168, 146, -62, 30, .4),
                          (112, 120, 185, 30, .4), (212, 108, 0, 32, .4), (130, 62, 225, 24, .36), (194, 46, -45, 26, .36),
                          (96, 104, 160, 24, .4), (232, 92, 20, 26, .4), (176, 56, -80, 22, .34), (140, 48, 255, 22, .34), (160, 142, 95, 18, .5)]:
    leaf(x, y, ang, L, 0.5 + random.uniform(0, .5), w)
spray(150, 140, 232, 64, .6)
spray(172, 138, -58, 60, .7)
spray(156, 136, 272, 48, .8, col="#9FB0DA", n=5)
# holiday greenery behind: pine sprigs fanning out
pine(152, 142, 215, 58, .7); pine(170, 140, -40, 56, .8); pine(160, 136, 262, 44, .9); pine(146, 144, 190, 40, 1.0); pine(176, 142, -8, 42, 1.0)
# back blooms
flower(168, 30, 12, "coral", "anemone", t0=1.6, tilt=-10)
tulip(108, 44, 22, -118, t0=1.7)
flower(212, 46, 13, "crimson", "rose", t0=2.3, tilt=15)
flower(240, 70, 10, "gold", "ranunculus", t0=2.6)
flower(84, 80, 11, "gold", "ranunculus", t0=2.7)
flower(150, 70, 21, "ivory", "rose", t0=1.9)
# mid leaves tucked between blooms
for (x, y, ang, L, w) in [(134, 104, 200, 22, .38), (186, 100, -10, 22, .38), (160, 108, 260, 16, .36), (120, 122, 150, 20, .38), (214, 118, 10, 20, .38)]:
    leaf(x, y, ang, L, 1.2 + random.uniform(0, .4), w)
flower(196, 86, 28, "oldrose", "rose", t0=2.1)
flower(116, 96, 33, "peony", "peony", t0=2.4, squash=.88)
tulip(226, 112, 20, 62, t0=2.8)
flower(100, 132, 14, "crimson", "rose", t0=2.9, tilt=-20)
flower(204, 124, 16, "oldrose", "rose", t0=3.1, tilt=25)
flower(162, 124, 25, "crimson", "rose", t0=3.0, squash=.92)
flower(138, 136, 10, "ivory", "rose", t0=4.2, tilt=30)   # opens last
spray(156, 138, 300, 34, 3.2, n=4)
# winterberry sprigs and two gold ornaments tucked in
berries(154, 138, 255, 54, 3.0); berries(168, 136, -70, 50, 3.2); berries(146, 140, 200, 36, 3.4)
bauble(134, 66, 5.2, 3.6); bauble(190, 110, 4.6, 3.8)
vine(150, 146, 150, 62, 2.6)
vine(170, 146, 30, 58, 2.8)
vine(142, 142, 125, 40, 3.0)

bouquet = ''.join(art)

# ------------------------------------------------------------------ vase, ledge, champagne, plate, butterfly, motes
vase = ('<g class="vase">'
        '<ellipse cx="176" cy="195" rx="36" ry="5" fill="#3A2A1E" fill-opacity=".35" filter="url(#blur3)"/>'
        '<path d="M144 150 Q136 166 142 180 Q146 190 160 191 Q174 190 178 180 Q184 166 176 150 Z" fill="url(#g-glass)"/>'
        '<path d="M150 154 Q146 170 150 184" stroke="#FFFFFF" stroke-width="3" stroke-opacity=".32" stroke-linecap="round" filter="url(#blur1)"/>'
        '<path d="M172 156 Q176 170 173 184" stroke="#FFFFFF" stroke-width="1.2" stroke-opacity=".18" stroke-linecap="round"/>'
        '<ellipse cx="160" cy="150" rx="16" ry="3.2" fill="#DCE3D6" fill-opacity=".35" stroke="#8FA38E" stroke-width=".6" stroke-opacity=".7"/>'
        '<path d="M146 191 Q160 196 174 191" stroke="#6D7F6A" stroke-width=".8" fill="none" stroke-opacity=".6"/>'
        '<path d="M139 166 Q160 171 181 166 L180.5 169.5 Q160 174.5 139.5 169.5 Z" fill="#C9A24A" fill-opacity=".9"/>'
        '<path d="M141 167.6 Q160 172 179 167.6" stroke="#FFF1BF" stroke-width=".5" fill="none" stroke-opacity=".8"/>'
        '</g>')
# glamour: gold sparkles twinkling over the bouquet, and a string of warm little lights across the top
sparkles = ''.join(
    f'<path class="spark" d="M{f(x)} {f(y-s)} Q{f(x)} {f(y)} {f(x+s)} {f(y)} Q{f(x)} {f(y)} {f(x)} {f(y+s)} Q{f(x)} {f(y)} {f(x-s)} {f(y)} Q{f(x)} {f(y)} {f(x)} {f(y-s)} Z" fill="#FFF3C4" stroke="#E2B95C" stroke-width=".3" style="transform-origin:{f(x)}px {f(y)}px;animation-delay:{random.uniform(4,14):.1f}s;animation-duration:{random.uniform(2.4,4.6):.1f}s"/>'
    for x, y, s in [(random.uniform(60, 262), random.uniform(14, 160), random.uniform(1.8, 4.2)) for _ in range(22)])
lights = ['<path d="M-4 4 Q80 28 160 21 Q240 28 324 4" fill="none" stroke="#4A3A2A" stroke-width=".7" stroke-opacity=".8"/>']
for i in range(11):
    t = (i + .5) / 11; lx = -4 + 328 * t
    ly = 4 + (21 - 4) * (1 - (2 * t - 1) ** 2) + 2 * math.sin(t * 6.28)  # sags along the wire
    lights.append(f'<g class="bulb" style="animation-delay:{random.uniform(0,3):.1f}s;animation-duration:{random.uniform(2,3.6):.1f}s"><circle cx="{f(lx)}" cy="{f(ly+4)}" r="7" fill="url(#g-bulb)" opacity=".8"/>'
                  f'<rect x="{f(lx-1)}" y="{f(ly)}" width="2" height="2.2" fill="#6B5A48"/><ellipse cx="{f(lx)}" cy="{f(ly+4.2)}" rx="1.7" ry="2.3" fill="#FFF1BF"/></g>')
lights = '<g class="lights">' + ''.join(lights) + '</g>'
ledge = ('<rect x="0" y="194" width="320" height="34" fill="url(#g-ledge)"/>'
         '<path d="M0 194 H320" stroke="#FFF8EA" stroke-width="1.2" stroke-opacity=".7"/>'
         '<path d="M0 195.5 H320" stroke="#8C7A66" stroke-width=".6" stroke-opacity=".5"/>')
# champagne coupe (left, front)
bub = ''.join(f'<circle class="bub" cx="{f(random.uniform(48,72))}" cy="{f(random.uniform(166,176))}" r="{random.uniform(.5,1.2):.1f}" fill="#FFFBE8" fill-opacity=".95" style="animation-delay:{random.uniform(0,3.4):.1f}s;animation-duration:{random.uniform(2.2,3.8):.1f}s"/>' for _ in range(12))
coupe = ('<g class="coupe">'
         '<ellipse cx="66" cy="195" rx="14" ry="2.4" fill="#3A2A1E" fill-opacity=".25" filter="url(#blur1)"/>'
         '<defs><clipPath id="cbowl"><path d="M42 152 H78 Q77 174 60 177 Q43 174 42 152 Z"/></clipPath></defs>'
         '<g clip-path="url(#cbowl)"><g class="cfill" style="transform-origin:60px 177px"><rect x="40" y="157" width="40" height="22" fill="url(#g-champ)"/>'
         '<path class="fizz" d="M20 157 q6 -2 12 0 t12 0 t12 0 t12 0 t12 0 t12 0 t12 0 V161 H20 Z" fill="#FFF6D6" fill-opacity=".9"/></g>' + bub + '</g>'
         '<path d="M42 152 H78 Q77 174 60 177 Q43 174 42 152 Z" fill="#FFFFFF" fill-opacity=".08" stroke="#B9A98C" stroke-width=".8" stroke-opacity=".8"/>'
         '<ellipse cx="60" cy="152" rx="18" ry="2.2" fill="none" stroke="#D9CBB0" stroke-width=".6" stroke-opacity=".8"/>'
         '<path d="M60 177 V191" stroke="#B9A98C" stroke-width="1.6" stroke-opacity=".8"/><path d="M50 193 Q60 189 70 193" stroke="#B9A98C" stroke-width="1" fill="none" stroke-opacity=".8"/>'
         '<path class="glint" d="M46 155 Q47 165 52 171" stroke="#FFFFFF" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-opacity=".8"/>'
         '</g>')
wine = ('<g class="wine">'
        '<defs><clipPath id="wbowl"><path d="M80 140 Q78 160 92 166 Q106 160 104 140 Q104 128 92 126 Q80 128 80 140 Z"/></clipPath></defs>'
        '<g clip-path="url(#wbowl)"><g class="cfill" style="transform-origin:92px 166px;animation-delay:1.5s"><rect x="76" y="146" width="32" height="22" fill="url(#g-wine)"/><path class="fizz" d="M56 146 q5 -1.6 10 0 t10 0 t10 0 t10 0 t10 0 t10 0 V150 H56 Z" fill="#9C3346" fill-opacity=".9"/></g></g>'
        '<path d="M80 140 Q78 160 92 166 Q106 160 104 140 Q104 128 92 126 Q80 128 80 140 Z" fill="#FFFFFF" fill-opacity=".06" stroke="#B9A98C" stroke-width=".8" stroke-opacity=".75"/>'
        '<path d="M92 166 V189" stroke="#B9A98C" stroke-width="1.5" stroke-opacity=".75"/><path d="M83 191 Q92 187 101 191" stroke="#B9A98C" stroke-width="1" fill="none" stroke-opacity=".75"/>'
        '<path class="glint" d="M83 134 Q82 146 86 156" stroke="#FFFFFF" stroke-width="1.2" fill="none" stroke-linecap="round" stroke-opacity=".7" style="animation-delay:4.5s"/>'
        '</g>')
# a silver dish with figs and grapes (right, front), painted small and quiet
grapes = ''.join(f'<circle cx="{f(246+(k%4)*3.1+(k//4)*1.5)}" cy="{f(178+(k//4)*2.6)}" r="1.9" fill="{["#4A2E4D","#5E3C62","#3B2440"][k%3]}"/><circle cx="{f(245.4+(k%4)*3.1+(k//4)*1.5)}" cy="{f(177.4+(k//4)*2.6)}" r=".5" fill="#EBD9E8" fill-opacity=".7"/>' for k in range(11))
dish = ('<g class="dish" transform="translate(262 189) scale(1.28) translate(-262 -189)">'
        '<ellipse cx="262" cy="193" rx="34" ry="3.5" fill="#3A2A1E" fill-opacity=".28" filter="url(#blur1)"/>'
        '<ellipse cx="262" cy="189" rx="32" ry="6.5" fill="url(#g-pewter)"/><ellipse cx="262" cy="188" rx="30" ry="5.4" fill="#C9CDCF" fill-opacity=".55"/>'
        '<path d="M232 188 Q262 181 292 188" stroke="#FFFFFF" stroke-width=".9" fill="none" stroke-opacity=".7"/>'
        + grapes +
        '<ellipse cx="272" cy="183" rx="5.2" ry="6" fill="#4B2A47"/><path d="M272 177 q1 -3 0 -5" stroke="#5B7A5E" stroke-width=".9" fill="none"/>'
        '<ellipse cx="282" cy="185" rx="5" ry="5.6" fill="#5A3356"/><ellipse cx="282" cy="185" rx="3.4" ry="4" fill="#C8667A"/><ellipse cx="282" cy="185" rx="1.8" ry="2.4" fill="#E8A0AE"/>'
        + ''.join(f'<circle cx="{f(282+math.cos(math.radians(a))*2.6)}" cy="{f(185+math.sin(math.radians(a))*3)}" r=".35" fill="#F7E4D0"/>' for a in range(0,360,40)) +
        '<path d="M236 186 L250 184 L249 190 Z" fill="#F0E3B8"/><path d="M236 186 L249 190 L248 192 L235 188 Z" fill="#DCCB95"/>'
        '<path d="M253 190 q6 -3 12 0" stroke="#5B7A5E" stroke-width=".7" fill="none"/>' + ''.join(f'<ellipse cx="{f(254.5+k*2.1)}" cy="{f(189.4-abs(math.sin(k))*.8)}" rx="1.1" ry=".4" fill="#6F8F6E" transform="rotate({-35 if k%2 else 35} {f(254.5+k*2.1)} {f(189.4)})"/>' for k in range(6)) +
        '</g>')
# fallen petals on the ledge
fallen = ('<g class="fallen">'
          '<use href="#p-notch" transform="translate(112 203) rotate(70) scale(7 9)" fill="url(#g-oldrose-lit)" fill-opacity=".9"/>'
          '<use href="#p-notch" transform="translate(126 207) rotate(-110) scale(6 8)" fill="url(#g-peony-shd)" fill-opacity=".9"/>'
          '<use href="#p-round" transform="translate(206 204) rotate(100) scale(5 7)" fill="url(#g-crimson-lit)" fill-opacity=".9"/>'
          '<ellipse cx="118" cy="207" rx="8" ry="1.6" fill="#3A2A1E" fill-opacity=".15" filter="url(#blur1)"/>'
          '</g>')
# butterfly (red admiral, painterly), flies in and rests on the peony
wing = lambda s: (f'<path d="M0 0 C{s*6} {-s*9} {s*16} {-s*12} {s*18} {-s*4} C{s*17} {s*2} {s*8} {s*6} 0 {s*1} Z" fill="#2E1F1A"/>'
                  f'<path d="M{s*4} {-s*3} C{s*9} {-s*7} {s*14} {-s*8} {s*16} {-s*5} C{s*14} {-s*2} {s*9} {-s*1} {s*5} {-s*1} Z" fill="#D8552F"/>'
                  f'<circle cx="{s*13}" cy="{-s*9}" r="{s*.9}" fill="#FFF4E6"/><circle cx="{s*16}" cy="{-s*7.5}" r="{s*.7}" fill="#FFF4E6"/>'
                  f'<path d="M0 0 C{s*4} {s*5} {s*10} {s*7} {s*12} {s*3}" fill="#3B2824" stroke="none"/>')
butterfly = ('<g class="bfly"><g class="bflyin">'
             '<g class="wing wl" style="transform-origin:0px 0px"><g transform="scale(-1 1)">' + wing(1) + '</g></g>'
             '<g class="wing wr" style="transform-origin:0px 0px">' + wing(1) + '</g>'
             '<ellipse cx="0" cy="0" rx="1.1" ry="4" fill="#2A1B16"/><path d="M-1 -4 Q-3 -8 -4 -9 M1 -4 Q3 -8 4 -9" stroke="#2A1B16" stroke-width=".5" fill="none"/>'
             '</g></g>')
motes = ''.join(f'<circle class="mote" cx="{random.uniform(20,200):.0f}" cy="{random.uniform(10,150):.0f}" r="{random.uniform(.5,1.2):.1f}" fill="#F1D9A0" style="animation-delay:-{random.uniform(0,12):.1f}s;animation-duration:{random.uniform(9,16):.1f}s;--dx:{random.uniform(-10,10):.0f}px;--dy:{random.uniform(-18,-8):.0f}px"/>' for _ in range(14))

still = ('<svg class="still" viewBox="0 0 320 228" aria-hidden="true">'
         '<defs>' + ''.join(defs) +
         '<filter id="blur3" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>'
         '<filter id="blur1" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="1.2"/></filter>'
         '<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .3 0 0 0 0 .25 0 0 0 0 .2 0 0 0 .9 0"/></filter>'
         '<radialGradient id="g-light" cx="30%" cy="22%" r="60%"><stop offset="0" stop-color="#FFF3D2" stop-opacity=".95"/><stop offset=".6" stop-color="#FBEBD2" stop-opacity=".2"/><stop offset="1" stop-color="#E9D7BC" stop-opacity="0"/></radialGradient>'
         '<linearGradient id="g-wall" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F9F1E3"/><stop offset=".55" stop-color="#EFE1CB"/><stop offset="1" stop-color="#DCC7A8"/></linearGradient>'
         '<linearGradient id="g-ledge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C9B59C"/><stop offset=".25" stop-color="#B49F86"/><stop offset="1" stop-color="#8E7A64"/></linearGradient>'
         '<linearGradient id="g-glass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5E7461"/><stop offset=".35" stop-color="#2C3E31"/><stop offset=".7" stop-color="#1E2D23"/><stop offset="1" stop-color="#46594A"/></linearGradient>'
         '<linearGradient id="g-wine" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E2537"/><stop offset="1" stop-color="#4E0F1E"/></linearGradient><linearGradient id="g-champ" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F3DC94"/><stop offset="1" stop-color="#D9B257"/></linearGradient>'
         '<linearGradient id="g-pewter" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B9BDBF"/><stop offset="1" stop-color="#6E7375"/></linearGradient>'
         '</defs>'
         '<rect width="320" height="228" fill="url(#g-wall)"/>'
         '<rect class="lightpool" width="320" height="228" fill="url(#g-light)"/>'
         + ledge + lights + motes +
         '<g class="bouquet" style="transform-origin:160px 192px"><g transform="translate(160 150) scale(1.14) translate(-160 -150)">' + bouquet + '</g></g>'
         + vase + wine + coupe + dish + fallen + butterfly + sparkles +
         '<rect width="320" height="228" filter="url(#grain)" opacity=".08" style="mix-blend-mode:multiply"/>'
         '</svg>')

# a small static rose for the booking paper's corner
mini = []
flower(44, 40, 24, "oldrose", "rose", t0=.6, target=mini)
leaf(20, 62, 150, 22, .3, target=mini); leaf(70, 60, 20, 20, .4, target=mini)
mini_svg = ('<svg class="bloom" viewBox="0 0 110 90" aria-hidden="true"><defs>' + ''.join(defs) +
            '<filter id="blur3" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter></defs>' + ''.join(mini) + '</svg>')

# ------------------------------------------------------------------ page edits
h = src
h = re.sub(r':root \{.*?color-scheme: dark;\n  \}', '''  :root {
    --ground: #E7DCCB;        /* page: warm parchment */
    --card: #FBF6EC;          /* invitation card */
    --card-deep: #F1E6D4;
    --gold: #B8933E;          /* gold: frame, rules, small caps */
    --gold-dim: rgba(184,147,62,.5);
    --cream: #2E3A2F;         /* display text on card: deep garden green */
    --cream-soft: #5F6E5F;
    --berry: #B23A48;
    --pine: #9DB4A2;
    --paper: #FFFBF4;         /* booking card: ivory */
    --paper-line: rgba(184,147,62,.55);
    --ink: #2E3A2F;
    --ink-soft: #6B7A6A;
    --display: "Cormorant Garamond", "Garamond", "Georgia", serif;
    --body: "Jost", "Futura", "Helvetica Neue", Arial, sans-serif;
    color-scheme: light;
  }'''.replace('  :root', ':root', 1), h, count=1, flags=re.S)
assert '--ground: #E7DCCB' in h

css = '''
  /* ---------- Fresh Flower Bar edition: a painted still life on parchment ---------- */
  .invite { box-shadow: 0 24px 60px rgba(70,50,30,.22); background: radial-gradient(120% 80% at 50% 0%, var(--card) 0%, var(--card-deep) 100%); }
  .frame { padding-top: 0; overflow: hidden; }
  .still { display: block; width: calc(100% + 32px); margin: 0 -16px 18px; }
  .corner { display: none; }
  .actions .pill { background: rgba(255,255,255,.5); }
  .pill:hover { background: #fff; }
  .foot { color: rgba(46,58,47,.6); }
  .credit, .credit a { color: rgba(46,58,47,.6); }
  h1 span { font-size: .34em; letter-spacing: .24em; margin-top: 12px; color: var(--gold); font-weight: 500; }
  .when { white-space: nowrap; font-size: clamp(16px, 4.7vw, 21px) !important; }
  .petals { position: absolute; inset: 0; overflow: hidden; pointer-events: none; }
  .petals i { position: absolute; top: -8px; width: 5px; height: 5px; background: radial-gradient(circle, #FFF6D0 0%, #E2B95C 55%, rgba(226,185,92,0) 72%); clip-path: polygon(50% 0, 62% 38%, 100% 50%, 62% 62%, 50% 100%, 38% 62%, 0 50%, 38% 38%); opacity: 0; }
  .petals b { position: absolute; top: -14px; width: 10px; height: 7px; border-radius: 80% 0 80% 0; background: var(--c); opacity: 0; box-shadow: inset 0 0 2px rgba(80,30,30,.15); }
  .book { text-align: center; }
  .book h2 { margin-bottom: 8px; }
  .book .price { margin: 0 0 14px; font-family: var(--display); font-size: 20px; color: var(--ink-soft); }
  .book .price b { font-size: 30px; font-weight: 500; color: var(--ink); }
  .incl { list-style: none; padding: 0; margin: 0 auto 18px; max-width: 34ch; display: grid; gap: 7px; text-align: left; font-size: 14.5px; color: var(--ink); }
  .incl li { display: grid; grid-template-columns: 14px 1fr; gap: 8px; }
  .incl li::before { content: "\\2726"; color: var(--gold); font-size: 10px; margin-top: 4px; }
  .book .btn { display: block; text-decoration: none; text-align: center; }
  .book .hint { margin-top: 12px; }
  .book .field { text-align: left; }
  input[type="email"] { width: 100%; font: 17px var(--body); color: var(--ink); padding: 12px 14px; border: 1px solid var(--gold); border-radius: 4px; background: #fff; }
  #form-view, #thanks-view { display: none !important; }
  .rsvp .bloom { width: 86px; height: 70px; opacity: .9; right: 4px; bottom: auto; top: 4px; }
  @media (min-width: 900px) {
    body { padding: 28px 24px; }
    .wrap { max-width: 720px; gap: 20px; }
    .frame { padding-left: 40px; padding-right: 40px; padding-bottom: 30px; }
    .still { width: calc(100% + 80px); margin-left: -40px; margin-right: -40px; }
    h1 { font-size: 46px; }
    .note { max-width: 56ch; margin-left: auto; margin-right: auto; font-size: 17px; }
    .actions > .actions { display: contents; }
    .actions { grid-template-columns: 1fr 1fr 1fr; align-items: end; gap: 10px; }
    .actions .lbl { grid-column: 1 / -1; }
    .actions .row2 { display: contents; }
    #map { margin: 0; }
    .rsvp { padding: 30px 40px 28px; }
    .incl { max-width: 44ch; }
  }
  .rsvp { color-scheme: light; }
  .btn:hover { background: #3F5240; }
  @media (prefers-reduced-motion: no-preference) {
    .bouquet { animation: swaygrp 9s ease-in-out 4s infinite; }
    .breathe { transform-box: view-box; animation: breathe2 7s ease-in-out 4.5s infinite; }
    .pt { transform-box: view-box; opacity: 0; animation: unfurl 1.5s cubic-bezier(.2,.75,.2,1) both; }
    .bud { transform-box: view-box; animation: budin .55s ease-out var(--d0) both, budout .9s ease-in var(--d1) forwards; }
    .bshadow { opacity: 0; animation: fadein 1.2s ease-out both; }
    .lf { transform-box: view-box; animation: grow 1.1s cubic-bezier(.2,.75,.2,1) both; }
    .stem { stroke-dasharray: 140; stroke-dashoffset: 140; animation: draw2 1.4s ease-out both; }
    .lightpool { animation: lightbreathe 6s ease-in-out infinite; }
    .mote { opacity: 0; animation-name: mote; animation-timing-function: ease-in-out; animation-iteration-count: infinite; }
    .cfill { transform-box: view-box; animation: fill 1.8s cubic-bezier(.4,0,.2,1) 1.2s both; }
    .fizz { animation: slosh 3.2s linear infinite; }
    .bub { animation-name: rise; animation-timing-function: ease-in; animation-iteration-count: infinite; }
    .glint { animation: glint 4.5s ease-in-out 3s infinite; }
    .bfly { animation: flight 18s ease-in-out 5s infinite both; opacity: 0; }
    .bflyin { animation: hover 2.4s ease-in-out infinite; }
    .wing { animation: flutter .42s ease-in-out infinite alternate; }
    .wl { animation-direction: alternate-reverse; }
    .petals b { animation: petalfall linear infinite; }
    .petals i { animation: glitterfall linear infinite, twinkle var(--tw, 1.2s) ease-in-out infinite alternate; }
    .spark { opacity: 0; transform-box: view-box; animation-name: sparkle; animation-timing-function: ease-in-out; animation-iteration-count: infinite; }
    .bulb { animation-name: bulb; animation-timing-function: ease-in-out; animation-iteration-count: infinite; animation-direction: alternate; }
    .gleam { opacity: 0; transform-box: view-box; animation: sparkle 3.6s ease-in-out infinite; }
    .orn::before, .orn::after { background: linear-gradient(90deg, var(--gold-dim), var(--gold), #F3DEA3, var(--gold), var(--gold-dim)); background-size: 200% 100%; animation: goldshimmer 6s linear infinite; }
    .orn svg { animation: ornspin 8s ease-in-out infinite; }
    .book .btn { position: relative; overflow: hidden; }
    .book .btn::after { content: ""; position: absolute; inset: 0; background: linear-gradient(115deg, transparent 40%, rgba(255,240,200,.35) 50%, transparent 60%); background-size: 260% 100%; animation: sweep 6s ease-in-out 2s infinite; }
  }
  @keyframes unfurl { 0% { opacity: 0; transform: rotate(var(--r, 0deg)) scale(.08) } 35% { opacity: 1 } 100% { opacity: 1; transform: rotate(0deg) scale(1) } }
  @keyframes budin { from { opacity: 0; transform: scale(.2) } to { opacity: 1; transform: scale(1) } }
  @keyframes budout { from { opacity: 1; transform: scale(1) } to { opacity: 0; transform: scale(1.6) } }
  @keyframes grow { from { opacity: 0; transform: scale(.05) rotate(-25deg) } 40% { opacity: 1 } to { opacity: 1; transform: none } }
  @keyframes fadein { to { opacity: 1 } }
  @keyframes breathe2 { 0%,100% { transform: scale(1) } 50% { transform: scale(1.035) } }
  @keyframes swaygrp { 0%,100% { transform: rotate(0deg) } 50% { transform: rotate(1.2deg) } }
  @keyframes lightbreathe { 0%,100% { opacity: .75 } 50% { opacity: 1 } }
  @keyframes mote { 0% { opacity: 0; transform: translate(0,0) } 20% { opacity: .9 } 80% { opacity: .5 } 100% { opacity: 0; transform: translate(var(--dx), var(--dy)) } }
  @keyframes rise { 0% { transform: translateY(0); opacity: 0 } 15% { opacity: 1 } 100% { transform: translateY(-18px); opacity: 0 } }
  @keyframes flight { 0% { opacity: 0; transform: translate(330px, 30px) rotate(-20deg) } 6% { opacity: 1 } 18% { transform: translate(236px, 58px) rotate(-10deg) } 30% { transform: translate(150px, 34px) rotate(8deg) } 40% { transform: translate(104px, 62px) rotate(-6deg) } 42%,70% { transform: translate(104px, 64px) rotate(0deg); opacity: 1 } 84% { transform: translate(40px, 20px) rotate(14deg); opacity: 1 } 92% { opacity: 0; transform: translate(-30px, -10px) rotate(18deg) } 100% { opacity: 0; transform: translate(330px, 30px) } }
  @keyframes hover { 0%,100% { transform: translateY(0) } 50% { transform: translateY(-1.5px) } }
  @keyframes flutter { from { transform: scaleX(1) } to { transform: scaleX(.3) } }
  @keyframes glitterfall { 0% { transform: translate(0,0) rotate(0); opacity: 0 } 6% { opacity: 1 } 50% { transform: translate(var(--dx), 300px) rotate(180deg) } 90% { opacity: .8 } 100% { transform: translate(calc(var(--dx) * -.5), 600px) rotate(360deg); opacity: 0 } }
  @keyframes twinkle { from { filter: brightness(.8) } to { filter: brightness(1.6) } }
  @keyframes sparkle { 0%, 100% { opacity: 0; transform: scale(.2) rotate(0deg) } 50% { opacity: 1; transform: scale(1) rotate(45deg) } }
  @keyframes bulb { from { opacity: .55 } to { opacity: 1 } }
  @keyframes ornspin { 0%,100% { transform: rotate(0) scale(1) } 50% { transform: rotate(180deg) scale(1.25) } }
  @keyframes goldshimmer { from { background-position: 200% 0 } to { background-position: -200% 0 } }
  @keyframes petalfall { 0% { transform: translate(0,0) rotate(0); opacity: 0 } 8% { opacity: .9 } 30% { transform: translate(calc(var(--dx) * .6), 170px) rotate(120deg) } 55% { transform: translate(calc(var(--dx) * -.3), 320px) rotate(220deg) } 85% { opacity: .75 } 100% { transform: translate(var(--dx), 560px) rotate(360deg); opacity: 0 } }
'''
h = h.replace('</style>\n</head>', css + '</style>\n</head>', 1)

# remove the sample's corner boughs and sparkles and strip; put the still life at the top of the frame
h = re.sub(r'\s*<!-- Corner art.*?<!-- Sparkles -->', '\n      ', h, count=1, flags=re.S)
h = re.sub(r'\s*<svg class="art sparkle.*?</svg>(?=\s*\n)', '', h, flags=re.S)
h = re.sub(r'\s*<svg class="glass".*?</svg>', '\n      ' + still, h, count=1, flags=re.S)
h = re.sub(r'\s*<svg class="tea strip".*?</svg>', '', h, count=1, flags=re.S)
petals = ''.join(f'<b style="left:{random.uniform(2,98):.1f}%;--dx:{random.uniform(-50,50):.0f}px;--c:{random.choice(["#EAB0AE","#F4D6CA","#F6EBD9","#D47A86","#EC8A6C","#B8232F","#FFFBF2","#C9A24A"])};transform:scale({random.uniform(.7,1.25):.2f});animation-duration:{random.uniform(9,16):.1f}s;animation-delay:{random.uniform(3,16):.1f}s"></b>' for _ in range(26))
petals += ''.join(f'<i style="left:{random.uniform(1,99):.1f}%;--dx:{random.uniform(-30,30):.0f}px;animation-duration:{random.uniform(11,19):.1f}s;animation-delay:{random.uniform(2,20):.1f}s;--tw:{random.uniform(.9,1.8):.1f}s"></i>' for _ in range(34))
h = h.replace('<div class="frame">', '<div class="frame">\n      <div class="petals" aria-hidden="true">' + petals + '</div>', 1)
assert 'class="still"' in h and 'class="art corner' not in h

# booking panel
book = '''<div id="book-view" class="book">
      <h2 id="book-h">Reserve your seat</h2>
      <p class="price" id="price"></p>
      <ul class="incl" id="incl"></ul>
      <a class="btn" id="book-btn" href="#" target="_blank" rel="noopener" hidden>Reserve your seat</a>
      <form id="interest" novalidate hidden>
        <div class="field"><label for="i-name">Your name</label><input type="text" id="i-name" autocomplete="name" placeholder="First and last name"></div>
        <div class="field"><label for="i-email">Email</label><input type="email" id="i-email" autocomplete="email" placeholder="We'll write when booking opens"></div>
        <div class="field"><div class="toggle-row"><div class="q">How many seats?</div>
          <div class="stepper"><button type="button" id="i-minus" aria-label="Fewer">−</button><span id="i-n">1</span><button type="button" id="i-plus" aria-label="More">+</button></div></div></div>
        <button class="btn" type="submit" id="i-send">Save me a seat</button>
        <p class="err" id="i-err" hidden></p>
      </form>
      <div id="i-thanks" class="thanks" hidden><h2>You're on the list</h2><p id="i-thanks-p"></p></div>
      <p class="hint" id="book-hint"></p>
    </div>
    '''
h = h.replace('<div id="form-view">', book + '<div id="form-view">', 1)
h = re.sub(r'<svg class="bloom".*?</svg>', mini_svg, h, count=1, flags=re.S)

h = h.replace('<p class="foot">With love, from Mara &amp; Theo</p>', '<p class="foot">Fresh Flower Bar · Fairfield, Connecticut</p>')
h = h.replace('invites/?ref=sample', 'invites/?ref=guest')
h = re.sub(r'<title>.*?</title>', '<title>Holiday Flower Arranging Class · Fresh Flower Bar</title>', h, count=1)
desc = "Learn the art of floral design: a holiday flower arranging class at Fresh Flower Bar, Fairfield CT. Wednesday, December 16 · 7–9pm. Champagne or wine and a charcuterie board for every guest."
h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h, count=1)
h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', h, count=1)
h = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Holiday Flower Arranging Class · December 16">', h, count=1)
h = h.replace('https://1294962213sh.github.io/demo/preview.jpg', 'https://1294962213sh.github.io/fresh-flower-bar/preview.jpg')
h = h.replace('<meta name="theme-color" content="#3A0F1B">', '<meta name="theme-color" content="#E7DCCB">')
h = h.replace('href="icon.svg"', 'href="../demo/icon.svg"')
h = re.sub(r'<!--\n  SAMPLE INVITATION.*?-->', '<!--\n  PREVIEW for Fresh Flower Bar (Sarah O\'Brien): Holiday Flower Arranging Class, Dec 16, 2026.\n  Built from demo/ by _templates/build_fresh_flower_bar.py. Edit the EVENT block at the bottom.\n  Booking: while EVENT.bookUrl is empty the panel collects an interest list ("Save me a seat");\n  set bookUrl to their booking page to switch the button to "Reserve your seat" (same link, nothing to resend).\n-->', h, count=1, flags=re.S)

ev_new = '''const EVENT = {
  title: "Holiday Flower Arranging",
  subtitle: "Beginners welcome",
  eyebrow: "Fresh Flower Bar",
  sub: "Learn the art of floral design",
  start: "2026-12-16T19:00:00",      // local time
  end:   "2026-12-16T21:00:00",
  tz:    "America/New_York",
  dateLabel: "Wednesday, December 16 · 7–9pm",
  poll: { active: false, label: "", entry: "", resultsCsv: "", options: [] },
  address: "Fresh Flower Bar, 1301 Bronson Road, Fairfield, CT 06824",
  addressDisplay: "Fresh Flower Bar Studio<br>1301 Bronson Road, Fairfield, CT",
  details: "An evening in our studio loft: step by step, our designers guide you through a lush holiday arrangement of premium seasonal flowers and greenery, yours to take home. A glass of champagne or wine and your own charcuterie board while you work.",
  // BOOKING — tickets stay on Fresh Flower Bar's own system.
  // Empty bookUrl: the panel collects an interest list (name, email, seats). Set it to their booking page to switch to "Reserve your seat".
  bookUrl: "",
  price: "<b>$219</b> per guest",       // TO CONFIRM with Sarah
  includes: [
    "Step-by-step guidance from Fresh Flower Bar's award-winning designers",
    "Premium holiday flowers and greenery, and the arrangement you make to take home",
    "A glass of champagne or wine",
    "Your own charcuterie board"
  ],
  hint: "Seats are limited · questions? Call or text (203) 800-3830",
  preview: true,                      // design preview: the interest form doesn't save anything
  analyticsId: "",                    // a Google Analytics measurement ID for this client's invitations; empty = no tracking
  // Interest-list Google Form (filled in once Sarah says yes)
  interest: { action: "", name: "", email: "", seats: "" },
  form: { action: "", name: "", attending: "", dinner: "" }
};'''
h = re.sub(r'const EVENT = \{.*?\n\};', ev_new, h, count=1, flags=re.S)

js = '''<script>
/* ===== Booking panel: interest list now, booking link later. Optional visit/tap counting via EVENT.analyticsId. ===== */
(function () {
  const $ = id => document.getElementById(id);
  let track = function () {};
  if (EVENT.analyticsId) {
    const s = document.createElement("script"); s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + EVENT.analyticsId; document.head.appendChild(s);
    window.dataLayer = window.dataLayer || []; function gtag() { dataLayer.push(arguments); }
    gtag("js", new Date()); gtag("config", EVENT.analyticsId, { page_title: EVENT.title });
    track = (name, params) => gtag("event", name, params || {});
  }
  $("price").innerHTML = EVENT.price || ""; $("price").hidden = !EVENT.price;
  $("incl").innerHTML = (EVENT.includes || []).map(t => "<li>" + t + "</li>").join("");
  $("book-hint").textContent = EVENT.hint || "";
  if (EVENT.bookUrl) {
    const b = $("book-btn"); b.href = EVENT.bookUrl; b.hidden = false;
    b.addEventListener("click", () => track("reserve_click"));
    return;
  }
  $("book-h").textContent = "Save me a seat";
  $("interest").hidden = false;
  let n = 1; const show = () => $("i-n").textContent = n;
  $("i-minus").onclick = () => { n = Math.max(1, n - 1); show(); };
  $("i-plus").onclick = () => { n = Math.min(10, n + 1); show(); };
  $("interest").addEventListener("submit", async e => {
    e.preventDefault();
    const name = $("i-name").value.trim(), email = $("i-email").value.trim(), err = $("i-err");
    if (!name) { err.textContent = "Please add your name."; err.hidden = false; return; }
    if (!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(email)) { err.textContent = "Please add an email so we can tell you when booking opens."; err.hidden = false; return; }
    err.hidden = true;
    const I = EVENT.interest || {};
    if (!EVENT.preview && I.action) {
      const fd = new URLSearchParams(); fd.append(I.name, name); fd.append(I.email, email); fd.append(I.seats, String(n));
      try { await fetch(I.action, { method: "POST", mode: "no-cors", body: fd }); } catch (x) {}
    }
    track("interest_submit", { seats: n });
    $("interest").hidden = true; $("book-h").hidden = true; $("price").hidden = true; $("incl").hidden = true;
    $("i-thanks-p").textContent = EVENT.preview
      ? "Design preview: nothing was saved. On the live page, " + name.split(" ")[0] + " would hear from Fresh Flower Bar the moment booking opens."
      : "Thank you, " + name.split(" ")[0] + ". We'll email you the moment booking opens, before anyone else.";
    $("i-thanks").hidden = false;
  });
})();
</script>
'''
h = h.replace('</body>', js + '</body>', 1)

outdir = REPO / 'fresh-flower-bar'; outdir.mkdir(exist_ok=True)
(outdir / 'index.html').write_text(h)
print('written', len(h))
