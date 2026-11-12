"""Build fresh-flower-bar/index.html from the holiday sample (demo/index.html).
Light ivory card in Fresh Flower Bar's sage + gold, a painted still life (holiday arrangement,
champagne coupe with rising bubbles, charcuterie board), falling gold glitter, and a booking panel
that starts as an interest list and switches to their booking page when EVENT.bookUrl is set."""
import math, random, re, pathlib

random.seed(7)
REPO = pathlib.Path('/home/claude/1294962213sh.github.io')
src = (REPO / 'demo/index.html').read_text()

def f(x): return f"{x:.1f}"

# ---------------------------------------------------------------- hero still life
out = []
delay = [0.3]
def nd(step=0.035):
    delay[0] += step
    return f"{delay[0]:.2f}s"

IDENT = (lambda x, y: (x, y), False)

def bloom(cx, cy, r, tones, center, kind="rose", target=None, M=IDENT, t0=None):
    """A flower that opens: bud, then inner petals, then outer petals unfurl; then it breathes."""
    target = out if target is None else target
    mp, flip = M
    cx, cy = mp(cx, cy)
    d = t0 if t0 is not None else delay[0]
    delay[0] = max(delay[0], d) + 0.16
    o = f"transform-origin:{f(cx)}px {f(cy)}px"
    g = [f'<g class="breathe" style="{o};animation-delay:-{random.uniform(0,5):.1f}s">']
    g.append(f'<circle class="wash" style="{o};animation-delay:{d:.2f}s" cx="{f(cx)}" cy="{f(cy)}" r="{f(r*1.05)}" fill="{tones[0]}" fill-opacity=".55" filter="url(#hb2)"/>')
    rings = [(r*0.62, 9, r*0.55, r*0.36, tones[1], .72), (r*0.36, 7, r*0.42, r*0.28, tones[2], .8)]
    if kind == "ranunculus":
        rings = [(r*0.6, 11, r*0.5, r*0.3, tones[1], .75), (r*0.42, 9, r*0.4, r*0.25, tones[2], .8), (r*0.22, 6, r*0.28, r*0.18, tones[3], .85)]
    nring = len(rings)
    for i, (dist, n, rx, ry, col, op) in enumerate(rings):
        ring_delay = d + 0.18 + (nring - 1 - i) * 0.22      # inner rings open first, outer last
        g.append(f'<g class="ring" style="{o};animation-delay:{ring_delay:.2f}s">')
        off = random.uniform(0, 360)
        for k in range(n):
            a = off + k * 360 / n + random.uniform(-8, 8)
            px = cx + dist * math.cos(math.radians(a)); py = cy + dist * math.sin(math.radians(a)) * 0.92
            g.append(f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="{f(rx*random.uniform(.85,1.1))}" ry="{f(ry*random.uniform(.85,1.1))}" fill="{col}" fill-opacity="{op:.2f}" transform="rotate({a+90:.0f} {f(px)} {f(py)})"/>')
        g.append('</g>')
    g.append(f'<circle class="bud" style="{o};animation-delay:{d:.2f}s" cx="{f(cx)}" cy="{f(cy)}" r="{f(r*0.18)}" fill="{center}" fill-opacity=".85"/>')
    hx, hy = cx - r*.35, cy - r*.4
    g.append(f'<ellipse class="ring" style="{o};animation-delay:{d+0.6:.2f}s" cx="{f(hx)}" cy="{f(hy)}" rx="{f(r*.22)}" ry="{f(r*.1)}" fill="#FFFDF6" fill-opacity=".55" transform="rotate(-30 {f(hx)} {f(hy)})"/>')
    g.append('</g>')
    target.append(''.join(g))

def sprig(x0, y0, ang, length, col, leaf="needle", sway=True, n=None, target=None, M=IDENT, t0=None):
    target = out if target is None else target
    mp, flip = M
    n = n or int(length / 4)
    pts = []
    for k in range(n + 1):
        t = k / n
        a = math.radians(ang + 18 * math.sin(t * 2.2))
        pts.append((x0 + math.cos(a) * length * t, y0 + math.sin(a) * length * t))
    P = [mp(x, y) for x, y in pts]
    bx, by = P[0]
    d = t0 if t0 is not None else delay[0]
    g = [f'<g class="{"sway" if sway else ""}" style="transform-origin:{f(bx)}px {f(by)}px;animation-delay:-{random.uniform(0,4):.1f}s">']
    g.append(f'<path class="stem" style="animation-delay:{d:.2f}s" d="M' + " L".join(f"{f(x)} {f(y)}" for x, y in P) + f'" stroke="{col[0]}" stroke-width=".8" fill="none" stroke-linecap="round"/>')
    for k, (x, y) in enumerate(pts[1:], 1):
        t = k / n
        a = ang + 18 * math.sin(t * 2.2)
        leaves = []
        for side in (-1, 1):
            if leaf == "needle":
                la = a + side * 55; L = 5.5 * (1 - t * 0.55)
                ex = x + math.cos(math.radians(la)) * L / 2; ey = y + math.sin(math.radians(la)) * L / 2
                leaves.append(('e', ex, ey, L/2, .9, la))
            elif leaf == "euc" and k % 2 == 0:
                la = a + side * 70; L = 4.2 * (1 - t * 0.35)
                leaves.append(('c', x + math.cos(math.radians(la)) * L * .8, y + math.sin(math.radians(la)) * L * .8, L*.75, 0, 0))
            elif leaf == "leaf" and k % 2 == 1:
                la = a + side * 40; L = 8 * (1 - t * 0.4)
                ex = x + math.cos(math.radians(la)) * L / 2; ey = y + math.sin(math.radians(la)) * L / 2
                leaves.append(('e', ex, ey, L/2, L/4.5, la))
        if not leaves: continue
        mx, my = mp(x, y)
        g.append(f'<g class="leaf" style="transform-origin:{f(mx)}px {f(my)}px;animation-delay:{d + t*0.9:.2f}s">')
        for typ, ex, ey, rx, ry, la in leaves:
            ex, ey = mp(ex, ey); la = -la if flip else la
            col_ = random.choice(col[1:])
            if typ == 'e':
                g.append(f'<ellipse cx="{f(ex)}" cy="{f(ey)}" rx="{f(rx)}" ry="{f(ry)}" fill="{col_}" fill-opacity=".85" transform="rotate({la:.0f} {f(ex)} {f(ey)})"/>')
            else:
                g.append(f'<circle cx="{f(ex)}" cy="{f(ey)}" r="{f(rx)}" fill="{col_}" fill-opacity=".8"/>')
        g.append('</g>')
    g.append('</g>')
    target.append(''.join(g))

def berries(cx, cy, n=5, col="#B23A48", target=None, M=IDENT, t0=None):
    target = out if target is None else target
    mp, flip = M
    cx, cy = mp(cx, cy)
    d = t0 if t0 is not None else delay[0] + 0.4
    g = [f'<g class="pop" style="animation-delay:{d:.2f}s;transform-origin:{f(cx)}px {f(cy)}px">']
    for k in range(n):
        x = cx + random.uniform(-5, 5); y = cy + random.uniform(-4, 4)
        g.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{random.uniform(1.6,2.3):.1f}" fill="{col}"/><circle cx="{f(x-.6)}" cy="{f(y-.6)}" r=".55" fill="#FFF4E6" fill-opacity=".8"/>')
    g.append('</g>')
    target.append(''.join(g))

PINE = ["#3F5F48", "#4C6B55", "#5E7D63", "#2F4A3A"]
EUC = ["#7E9A86", "#9DB4A2", "#B5C7B4", "#8DA893"]
LEAF = ["#5B7A5E", "#6F8F6E", "#88A383"]
BLUSH = ["#F0C7BD", "#E9A9A0", "#D98A84", "#C86E6E"]
PEACH = ["#F7D3B5", "#F2B48E", "#E8976E", "#D9785A"]
IVORY = ["#FBF2E6", "#F5E6D5", "#EBD3C0", "#E2C1AD"]
WINE = ["#C7707C", "#A84458", "#8E2F45", "#6E2034"]

# arrangement: greenery grows out first, then the blooms open one after another
S = 1.22                                   # arrangement scale around its base
def AX(x, y): return (130 + (x - 130) * S, 104 + (y - 104) * S)
AM = (AX, False)
for (x0, y0, ang, L, col, lf) in [(130, 88, 200, 62, PINE, "needle"), (130, 88, -15, 58, PINE, "needle"), (128, 84, 230, 50, EUC, "euc"),
                                 (132, 84, -45, 46, EUC, "euc"), (130, 80, 255, 44, PINE, "needle"), (130, 80, 285, 40, EUC, "euc"),
                                 (126, 92, 165, 52, LEAF, "leaf"), (134, 92, 12, 50, LEAF, "leaf"), (128, 95, 150, 44, EUC, "euc"), (132, 95, 30, 40, PINE, "needle")]:
    sprig(x0, y0, ang, L, col, lf, M=AM, t0=0.25 + random.uniform(0, .5))
delay[0] = 0.9
for (cx, cy, r, pal, cen, kind) in [
    (130, 84, 17, PEACH, "#B65F45", "ranunculus"), (118, 66, 15, IVORY, "#C9A27A", "rose"), (142, 62, 16, BLUSH, "#B5545E", "rose"),
    (104, 84, 13, BLUSH, "#B5545E", "rose"), (157, 82, 13, IVORY, "#C9A27A", "ranunculus"), (130, 46, 11, PEACH, "#B65F45", "rose"),
    (112, 47, 9, WINE, "#4E1525", "rose"), (150, 44, 9, IVORY, "#C9A27A", "rose"),
    (92, 70, 9, WINE, "#4E1525", "ranunculus"), (168, 66, 9, PEACH, "#B65F45", "rose"),
]:
    bloom(cx, cy, r, pal, cen, kind, M=AM)
for (bx, by) in [(100, 58), (161, 52), (122, 100), (146, 101), (84, 88), (176, 86), (136, 32)]:
    berries(bx, by, M=AM)

# floral corner sprays (replace the sample's pine boughs): one spray, mapped into each corner
def corner_svg(cls, W, flipx, flipy):
    parts = []
    mp = lambda x, y: ((W - x) if flipx else x, (W - y) if flipy else y)
    M = (mp, flipx != flipy)
    base = 0.2 if not flipy else 1.2
    sprig(2, 4, 8, 78, EUC, "euc", target=parts, M=M, t0=base)
    sprig(4, 2, 80, 74, PINE, "needle", target=parts, M=M, t0=base + .1)
    sprig(6, 6, 40, 60, LEAF, "leaf", target=parts, M=M, t0=base + .2)
    sprig(3, 8, 22, 52, PINE, "needle", target=parts, M=M, t0=base + .15)
    bloom(22, 20, 12, BLUSH, "#B5545E", "rose", target=parts, M=M, t0=base + .5)
    bloom(40, 12, 8, IVORY, "#C9A27A", "ranunculus", target=parts, M=M, t0=base + .75)
    bloom(12, 40, 8, PEACH, "#B65F45", "rose", target=parts, M=M, t0=base + .9)
    berries(52, 26, target=parts, M=M, t0=base + 1.2)
    berries(26, 50, 4, target=parts, M=M, t0=base + 1.3)
    return f'<svg class="art corner {cls}" viewBox="0 0 {W} {W}" aria-hidden="true">' + ''.join(parts) + '</svg>'
CORNERS = (corner_svg("tl", 136, False, False) + "\n" + corner_svg("tr", 136, True, False) + "\n"
           + corner_svg("bl", 136, False, True) + "\n" + corner_svg("br", 136, True, True))

# compote vase (gold line, faint glaze)
vase = ('<g class="vase" transform="translate(130 104) scale(1.22) translate(-130 -104)" fill="none" stroke="#B8933E" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">'
        '<path class="draw" d="M104 100 Q130 122 156 100" fill="#FBF3E4" fill-opacity=".55"/>'
        '<path class="draw" d="M102 100 H158"/>'
        '<path class="draw" d="M126 112 Q127 120 124 127 H136 Q133 120 134 112"/>'
        '<path class="draw" d="M116 130 Q130 125 144 130 Q130 134 116 130 Z" fill="#FBF3E4" fill-opacity=".6"/>'
        '</g>')

# champagne: a pair of coupes, left, clinking; champagne fills, bubbles keep rising, a sparkle burst at the rims
def coupe(dx, dy, cid, sc=1.0):
    X = lambda x: 43 + (x - 43) * sc + dx
    Y = lambda y: 126 + (y - 126) * sc + dy
    bub = []
    for k in range(11):
        x = random.uniform(X(31), X(55)); r = random.uniform(.6, 1.4) * sc
        bub.append(f'<circle class="bub" cx="{f(x)}" cy="{f(random.uniform(Y(116),Y(124)))}" r="{r:.1f}" fill="#FFF8E1" fill-opacity=".95" style="animation-delay:{random.uniform(0,3.2):.1f}s;animation-duration:{random.uniform(2.0,3.4):.1f}s"/>')
    bowl = f"M{f(X(26))} {f(Y(104))} H{f(X(60))} Q{f(X(59))} {f(Y(124))} {f(X(43))} {f(Y(126))} Q{f(X(27))} {f(Y(124))} {f(X(26))} {f(Y(104))} Z"
    return (f'<g class="coupe"><defs><clipPath id="{cid}"><path d="{bowl}"/></clipPath></defs>'
            f'<g clip-path="url(#{cid})"><g class="cfill" style="transform-origin:{f(X(43))}px {f(Y(126))}px"><rect x="{f(X(22))}" y="{f(Y(108))}" width="{f(44*sc)}" height="{f(22*sc)}" fill="#F1D891" fill-opacity=".8"/>'
            f'<path class="fizz" d="M{f(X(4))} {f(Y(108))} q6 -2 12 0 t12 0 t12 0 t12 0 t12 0 t12 0 t12 0 V{f(Y(112))} H{f(X(4))} Z" fill="#FFF3C9" fill-opacity=".95"/></g>'
            + ''.join(bub) + '</g>'
            '<g fill="none" stroke="#B8933E" stroke-width="1.05" stroke-linecap="round">'
            f'<path class="draw" d="{bowl}"/>'
            f'<path class="draw" d="M{f(X(43))} {f(Y(126))} V{f(Y(146))}"/><path class="draw" d="M{f(X(34))} {f(Y(148))} Q{f(X(43))} {f(Y(145))} {f(X(52))} {f(Y(148))}"/></g>'
            f'<path class="glint" d="M{f(X(30))} {f(Y(107))} Q{f(X(31))} {f(Y(116))} {f(X(36))} {f(Y(121))}" stroke="#FFFDF4" stroke-width="1.3" fill="none" stroke-linecap="round" opacity=".85"/>'
            '</g>')
burst = ''.join(f'<path class="clink" style="animation-delay:{k*0.08:.2f}s" d="M{44+math.cos(math.radians(a))*3:.1f} {112+math.sin(math.radians(a))*3:.1f} L{44+math.cos(math.radians(a))*10:.1f} {112+math.sin(math.radians(a))*10:.1f}" stroke="#D4AF5A" stroke-width=".9" stroke-linecap="round"/>' for k, a in enumerate([-150,-120,-90,-60,-30]))
coupe_svg = coupe(-14, 8, 'cb1', .82) + coupe(14, 14, 'cb2', .76) + '<g class="clinkg">' + burst + '</g>'

# charcuterie board, front right: wood oval with handle, cheese, salami, grapes, crackers, rosemary
cb = ['<g class="board">',
      '<g class="pop" style="animation-delay:.25s;transform-origin:205px 146px">',
      '<ellipse cx="206" cy="146" rx="44" ry="15" fill="#C9A47C"/><ellipse cx="206" cy="144" rx="44" ry="15" fill="#D8B68D"/>',
      '<path d="M249 141 h14 a3 3 0 0 1 0 6 h-14" fill="#C9A47C"/><circle cx="259" cy="144" r="1.3" fill="#8F6E4B"/>',
      '<path d="M170 141 Q206 133 242 141" stroke="#BC9670" stroke-width=".7" fill="none" opacity=".7"/>',
      '<path d="M174 148 Q206 155 238 148" stroke="#BC9670" stroke-width=".7" fill="none" opacity=".6"/></g>']
items = []
# cheese wedges
items.append('<path d="M178 141 L196 136 L194 147 Z" fill="#F2D98C"/><path d="M178 141 L194 147 L192 150 L177 144 Z" fill="#E3C46F"/><circle cx="186" cy="142" r=".8" fill="#E3C46F"/>')
items.append('<path d="M214 136 L232 139 L222 146 Z" fill="#F7EBC8"/><path d="M222 146 L232 139 L232 142 L222 149 Z" fill="#E8D8A8"/>')
# salami rounds, fanned
for k, (x, y) in enumerate([(200, 148), (205, 149.5), (210, 150), (215, 149)]):
    items.append(f'<ellipse cx="{x}" cy="{y}" rx="4.4" ry="3" fill="#B5475A"/><circle cx="{x-1.4}" cy="{y-.6}" r=".5" fill="#F3D6CF"/><circle cx="{x+1.2}" cy="{y+.5}" r=".45" fill="#F3D6CF"/>')
# grapes
for k in range(9):
    gx = 197 + (k % 3) * 2.6 + (k // 3) * 1.1; gy = 137 + (k // 3) * 2.3
    items.append(f'<circle cx="{f(gx)}" cy="{f(gy)}" r="1.6" fill="{["#6E3552","#83405F","#5B2A44"][k%3]}"/><circle cx="{f(gx-.5)}" cy="{f(gy-.5)}" r=".4" fill="#F4E3EC" fill-opacity=".7"/>')
# crackers
for k in range(3):
    items.append(f'<rect x="{224+k*3.2}" y="{144+k*.6}" width="7" height="5" rx=".8" fill="#E9C994" stroke="#D2AE73" stroke-width=".4" transform="rotate({-12+k*6} {227+k*3.2} {146+k*.6})"/>')
# rosemary + a fig
items.append('<path d="M182 151 Q192 148 202 151" stroke="#5B7A5E" stroke-width=".7" fill="none"/>' + ''.join(
    f'<ellipse cx="{184+k*2.4}" cy="{150.4-math.sin(k/2)*1.2}" rx="1.4" ry=".45" fill="#6F8F6E" transform="rotate({-30 if k%2 else 30} {184+k*2.4} {150.4-math.sin(k/2)*1.2})"/>' for k in range(8)))
items.append('<circle cx="238" cy="146" r="3.4" fill="#7A3B5A"/><path d="M236 146 Q238 143 240 146 Q238 148 236 146 Z" fill="#E7909B"/>')
for k, it in enumerate(items):
    cb.append(f'<g class="pop" style="animation-delay:{0.55 + k*0.06:.2f}s;transform-origin:206px 144px">{it}</g>')
cb.append('</g>')

# little gold sparkles around the still life
spk = []
for k, (x, y, s) in enumerate([(74, 40, 5), (190, 34, 6), (210, 70, 4), (60, 76, 4), (100, 22, 3.5), (236, 110, 4.5), (18, 92, 3.5)]):
    spk.append(f'<path class="tw" style="animation-delay:{k*0.45:.2f}s;transform-origin:{x}px {y}px" d="M{x} {y-s} L{x+s*.22} {y-s*.22} L{x+s} {y} L{x+s*.22} {y+s*.22} L{x} {y+s} L{x-s*.22} {y+s*.22} L{x-s} {y} L{x-s*.22} {y-s*.22} Z" fill="#C9A24E"/>')

glow = ''.join(f'<circle class="bk" cx="{x}" cy="{y}" r="{r}" fill="#F1D27E" fill-opacity="{o}" filter="url(#hb6)" style="animation-delay:{d}s"/>' for x,y,r,o,d in [(130,70,46,.22,0),(52,112,18,.3,1.2),(206,138,22,.22,2.1),(84,40,8,.4,.6),(186,46,7,.45,1.8),(238,96,6,.4,2.6),(28,70,6,.35,3.1)])
hero = ('<svg class="still" viewBox="8 14 262 144" aria-hidden="true">'
        '<defs><filter id="hb2" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.2"/></filter><filter id="hb6" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6"/></filter></defs>'
        + glow + ''.join(out) + vase + coupe_svg + ''.join(cb) + ''.join(spk) + '</svg>')

# ---------------------------------------------------------------- page edits
h = src

# palette: ivory card on sage, gold frame, deep-green ink
h = re.sub(r':root \{.*?color-scheme: dark;\n  \}', '''  :root {
    --ground: #CFD8C6;        /* page: Fresh Flower Bar sage */
    --card: #FFFBF4;          /* invitation card: warm ivory */
    --card-deep: #F6EAE2;     /* card bottom: a blush wash */
    --gold: #B8933E;          /* their gold: frame, line art, rules */
    --gold-dim: rgba(184,147,62,.5);
    --cream: #2E4636;         /* display text on card: deep garden green */
    --cream-soft: #5F7062;    /* secondary text on card */
    --berry: #B23A48;
    --pine: #9DB4A2;          /* eucalyptus: other bars */
    --paper: #FFFBF4;         /* booking card: ivory */
    --paper-line: rgba(184,147,62,.55);
    --ink: #2E4636;           /* headings, buttons */
    --ink-soft: #6B7A6A;
    --display: "Cormorant Garamond", "Garamond", "Georgia", serif;
    --body: "Jost", "Futura", "Helvetica Neue", Arial, sans-serif;
    color-scheme: light;
  }'''.replace('  :root', ':root', 1), h, count=1, flags=re.S)
assert '--ground: #CFD8C6' in h

extra_css = '''
  /* ---------- Fresh Flower Bar edition ---------- */
  .invite { box-shadow: 0 24px 60px rgba(46,70,54,.22); }
  .actions .pill { background: rgba(255,255,255,.55); }
  .pill:hover { background: #fff; }
  .foot { color: rgba(46,70,54,.6); }
  .credit, .credit a { color: rgba(46,70,54,.6); }
  .still { display: block; width: 108%; max-width: 380px; margin: -30px -4% 10px; overflow: visible; }
  h1 span { font-size: .34em; letter-spacing: .24em; margin-top: 12px; color: var(--gold); font-weight: 500; }
  .when { white-space: nowrap; font-size: clamp(16px, 4.7vw, 21px) !important; }
  .glitter { position: absolute; inset: 0; overflow: hidden; pointer-events: none; }
  .glitter i { position: absolute; top: -8px; width: 3px; height: 3px; border-radius: 50%; background: #D4AF5A; opacity: 0; box-shadow: 0 0 4px rgba(212,175,90,.8); }
  .glitter i:nth-child(3n) { width: 2px; height: 2px; background: #E9CF8A; }
  .glitter i:nth-child(4n) { width: 4px; height: 2px; border-radius: 1px; background: #C9A24E; }
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
  .rsvp .bloom { opacity: .55; }
  @media (prefers-reduced-motion: no-preference) {
    .still .pop { transform-box: view-box; animation: pop .7s ease-out both; }
    .still .sway { transform-box: view-box; animation: swayz 7s ease-in-out infinite; }
    .still .draw { stroke-dasharray: 160; stroke-dashoffset: 160; animation: draw2 1.6s ease-out .2s both; }
    .still .cfill { transform-box: view-box; transform-origin: 43px 126px; animation: fill 1.6s cubic-bezier(.4,0,.2,1) .6s both; }
    .still .fizz { animation: slosh 3.2s linear infinite; }
    .still .bub { animation-name: rise; animation-timing-function: ease-in; animation-iteration-count: infinite; }
    .still .glint { animation: glint 4.5s ease-in-out 2s infinite; }
    .still .tw { transform-box: view-box; animation: twinkle 3.4s ease-in-out infinite; }
    .still .bk { animation: bokeh 6s ease-in-out infinite; }
    .still .clink { stroke-dasharray: 10; stroke-dashoffset: 10; animation: clink 4s ease-out 2.4s infinite; }
    .glitter i { animation: fall linear infinite; }
    .book .btn { position: relative; overflow: hidden; }
    .book .btn::after { content: ""; position: absolute; inset: 0; background: linear-gradient(115deg, transparent 40%, rgba(255,240,200,.35) 50%, transparent 60%); background-size: 260% 100%; animation: sweep 6s ease-in-out 2s infinite; }
  }

  .glitter b { position: absolute; top: -12px; width: 9px; height: 6px; border-radius: 80% 0 80% 0; background: var(--c); opacity: 0; box-shadow: inset 0 0 2px rgba(0,0,0,.08); }
  .corner { width: 128px; height: 128px; }
  @media (prefers-reduced-motion: no-preference) {
    .breathe { transform-box: view-box; animation: breathe2 6s ease-in-out 3.5s infinite; }
    .ring, .bud, .wash { transform-box: view-box; animation: open 1.5s cubic-bezier(.2,.8,.25,1) both; }
    .bud { animation-duration: .7s; }
    .wash { animation: washin 1.8s ease-out both; }
    .leaf { transform-box: view-box; animation: open .8s ease-out both; }
    .stem { stroke-dasharray: 120; stroke-dashoffset: 120; animation: draw2 1.2s ease-out both; }
    .glitter b { animation: petalfall linear infinite; }
  }
  @keyframes open { from { opacity: 0; transform: scale(.1) rotate(-40deg) } 60% { opacity: 1 } to { opacity: 1; transform: none } }
  @keyframes washin { from { opacity: 0; transform: scale(.3) } to { opacity: 1; transform: none } }
  @keyframes breathe2 { 0%,100% { transform: scale(1) } 50% { transform: scale(1.045) } }
  @keyframes petalfall { 0% { transform: translate(0,0) rotate(0); opacity: 0 } 8% { opacity: .9 } 30% { transform: translate(calc(var(--dx) * .6), 170px) rotate(120deg) } 55% { transform: translate(calc(var(--dx) * -.3), 320px) rotate(220deg) } 85% { opacity: .75 } 100% { transform: translate(var(--dx), 560px) rotate(360deg); opacity: 0 } }
  @keyframes clink { 0% { stroke-dashoffset: 10; opacity: 0 } 6% { opacity: 1 } 18% { stroke-dashoffset: 0; opacity: 1 } 34%,100% { stroke-dashoffset: -10; opacity: 0 } }
  @keyframes rise { 0% { transform: translateY(0); opacity: 0 } 15% { opacity: 1 } 100% { transform: translateY(-20px); opacity: 0 } }
  @keyframes fall { 0% { transform: translate(0, 0) rotate(0); opacity: 0 } 10% { opacity: .95 } 80% { opacity: .8 } 100% { transform: translate(var(--dx, 10px), 560px) rotate(240deg); opacity: 0 } }
'''
h = h.replace('</style>\n</head>', extra_css + '</style>\n</head>', 1)

# corners: floral sprays instead of pine boughs
h = re.sub(r'<svg class="art corner tl".*?</svg>\s*<svg class="art corner br".*?</svg>\s*<svg class="art corner tr".*?</svg>\s*<svg class="art corner bl".*?</svg>', lambda m: CORNERS, h, count=1, flags=re.S)
assert 'class="breathe"' in h
# hero: replace the wine glass with the still life; drop the bauble strip
h = re.sub(r'<svg class="glass".*?</svg>', hero, h, count=1, flags=re.S)
h = re.sub(r'\s*<svg class="tea strip".*?</svg>', '', h, count=1, flags=re.S)

# glitter layer inside the frame
petals = ''.join(f'<b style="left:{random.uniform(2,98):.1f}%;--dx:{random.uniform(-40,40):.0f}px;--c:{random.choice(["#F0C7BD","#E9A9A0","#F7D3B5","#FBF2E6","#E8976E"])};animation-duration:{random.uniform(9,16):.1f}s;animation-delay:{random.uniform(0,12):.1f}s"></b>' for _ in range(14))
gl = petals + ''.join(f'<i style="left:{random.uniform(3,97):.1f}%;--dx:{random.uniform(-24,24):.0f}px;animation-duration:{random.uniform(7,13):.1f}s;animation-delay:{random.uniform(0,10):.1f}s"></i>' for _ in range(18))
h = h.replace('<div class="frame">', '<div class="frame">\n      <div class="glitter" aria-hidden="true">' + gl + '</div>', 1)

# booking panel (interest list now, booking link later), placed before the old RSVP views
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

# text, meta, footer
h = h.replace('<p class="foot">With love, from Mara &amp; Theo</p>', '<p class="foot">Fresh Flower Bar · Fairfield, Connecticut</p>')
h = h.replace('invites/?ref=sample', 'invites/?ref=guest')
h = re.sub(r'<title>.*?</title>', '<title>Holiday Flower Arranging Class · Fresh Flower Bar</title>', h, count=1)
desc = "Learn the art of floral design: a holiday flower arranging class at Fresh Flower Bar, Fairfield CT. Wednesday, December 16 · 7–9pm. Champagne or wine and a charcuterie board for every guest."
h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h, count=1)
h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', h, count=1)
h = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Holiday Flower Arranging Class · December 16">', h, count=1)
h = h.replace('https://1294962213sh.github.io/demo/preview.jpg', 'https://1294962213sh.github.io/fresh-flower-bar/preview.jpg')
h = h.replace('<meta name="theme-color" content="#3A0F1B">', '<meta name="theme-color" content="#CFD8C6">')
h = h.replace('href="icon.svg"', 'href="../demo/icon.svg"')
h = re.sub(r'<!--\n  SAMPLE INVITATION.*?-->', '<!--\n  PREVIEW for Fresh Flower Bar (Sarah O\'Brien): Holiday Flower Arranging Class, Dec 16, 2026.\n  Built from demo/ (the holiday sample). Edit the EVENT block at the bottom.\n  Booking: while EVENT.bookUrl is empty the panel collects an interest list ("Save me a seat");\n  set bookUrl to their booking page to switch the button to "Reserve your seat" (same link, nothing to resend).\n-->', h, count=1, flags=re.S)

# EVENT block
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
  // Interest-list Google Form (filled in once Sarah says yes)
  interest: { action: "", name: "", email: "", seats: "" },
  form: { action: "", name: "", attending: "", dinner: "" }
};'''
h = re.sub(r'const EVENT = \{.*?\n\};', ev_new, h, count=1, flags=re.S)
assert 'bookUrl' in h

# booking-panel script, appended before </body>
js = '''<script>
/* ===== Booking panel: interest list now, booking link later ===== */
(function () {
  const $ = id => document.getElementById(id);
  $("price").innerHTML = EVENT.price || ""; $("price").hidden = !EVENT.price;
  $("incl").innerHTML = (EVENT.includes || []).map(t => "<li>" + t + "</li>").join("");
  $("book-hint").textContent = EVENT.hint || "";
  if (EVENT.bookUrl) {
    const b = $("book-btn"); b.href = EVENT.bookUrl; b.hidden = false;
    b.addEventListener("click", () => { try { window.gtag && gtag("event", "reserve_click"); } catch (e) {} });
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
