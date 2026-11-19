"""Painted opening for the workshop sample (demo-workshop/).

The invitation opens as a soft oil painting of the bouquet (painted.jpg, made Nov 19 2026 from the
approved painting), holds for ~2 s, then dissolves while the clear bouquet blooms underneath, and keeps a
faint painted skin (22%) plus a canvas-grain overlay so the end state still reads as a painting.
Also adds paper grain to the invitation and booking panels.

Usage: apply(html_text) -> html_text. build_workshop_sample.py calls this last; it is idempotent.
"""
import re

GRAIN = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'>"
         "<filter id='g'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 0.5  0 0 0 0 0.45  0 0 0 0 0.38  0 0 0 1 0'/></filter>"
         "<rect width='220' height='220' filter='url(%23g)'/></svg>\")")
CANVAS = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='4' height='4'>"
          "<path d='M0 2h4M2 0v4' stroke='rgb(70,55,40)' stroke-width='.6' stroke-opacity='.5'/></svg>\")")

CSS = f"""
  /* ---------- Painted opening: oil painting -> clear bouquet, with a painted skin left behind ---------- */
  .stillwrap {{ position: relative; width: calc(100% + 32px); margin: 0 -16px 18px; }}
  .stillwrap .still {{ width: 100%; margin: 0; }}
  .painted-over {{ position: absolute; inset: 0; width: 100%; height: 100%; display: block; pointer-events: none; opacity: .22; filter: blur(.5px); }}
  .stillwrap::after {{ content: ""; position: absolute; inset: 0; pointer-events: none; background-image: {CANVAS}; opacity: .05; mix-blend-mode: multiply; }}
  .invite::after, .rsvp::after {{ content: ""; position: absolute; inset: 0; pointer-events: none; border-radius: inherit; background-image: {GRAIN}; opacity: .08; mix-blend-mode: multiply; z-index: 0; }}
  .invite > *, .rsvp > * {{ position: relative; z-index: 1; }}
  @media (min-width: 900px) {{ .stillwrap {{ width: calc(100% + 80px); margin-left: -40px; margin-right: -40px; }} }}
  @media (prefers-reduced-motion: no-preference) {{
    .painted-over {{ opacity: 1; filter: none; animation: paintout 2.6s ease-in-out 2.9s forwards; }}
  }}
  @keyframes paintout {{ to {{ opacity: .22; filter: blur(.5px) }} }}
"""

SPRIG = '''<svg class="bloom sprig" viewBox="0 0 110 90" aria-hidden="true" fill="none" stroke="#B38F45" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round">
      <path class="draw" d="M100 84 C 86 70, 70 52, 56 22"/>
      <path class="draw" d="M62 34 C 52 30, 46 34, 44 42 C 52 44, 60 40, 62 34 Z"/>
      <path class="draw" d="M70 48 C 60 46, 54 50, 52 58 C 60 60, 68 56, 70 48 Z"/>
      <path class="draw" d="M80 62 C 70 60, 64 64, 62 72 C 70 74, 78 70, 80 62 Z"/>
      <path class="draw" d="M66 36 C 76 30, 84 32, 88 38 C 80 42, 72 42, 66 36 Z"/>
      <path class="draw" d="M76 52 C 86 46, 94 48, 98 54 C 90 58, 82 58, 76 52 Z"/>
      <path class="draw" d="M58 26 C 62 18, 68 16, 74 18 C 70 24, 64 28, 58 26 Z"/>
      <circle cx="54" cy="20" r="1.4" fill="#B38F45" stroke="none"/><circle cx="60" cy="14" r="1.1" fill="#B38F45" stroke="none"/>
    </svg>'''

def apply(h: str) -> str:
    if 'class="painted-over"' in h:
        return h
    # wrap the still-life SVG and overlay the painting
    i = h.index('<svg class="still"')
    depth, k = 0, i
    for m in re.finditer(r'<svg\b|</svg>', h[i:]):
        depth += 1 if m.group() == '<svg' else -1
        if depth == 0:
            k = i + m.end(); break
    svg = h[i:k]
    wrapped = ('<div class="stillwrap" aria-hidden="true">' + svg +
               '<img class="painted-over" src="painted.jpg?v=1" alt="" decoding="async"></div>')
    h = h[:i] + wrapped + h[k:]
    # CSS: after the workshop edition block's .still rule
    h = h.replace("  .still { display: block; width: calc(100% + 32px); margin: 0 -16px 18px; }",
                  "  .still { display: block; width: calc(100% + 32px); margin: 0 -16px 18px; }" + CSS, 1)
    # booking panel: gold line-art sprig instead of the painted rose
    i = h.find('<svg class="bloom" viewBox="0 0 110 90"')
    if i >= 0:
        j = h.index('</svg>', i) + 6
        h = h[:i] + SPRIG + h[j:]
        h = h.replace("  .rsvp .bloom { width: 86px; height: 70px; opacity: .85; right: 4px; bottom: auto; top: 4px; z-index: 0; pointer-events: none; }",
                      "  .rsvp .bloom { width: 86px; height: 70px; opacity: .85; right: 4px; bottom: auto; top: 4px; z-index: 0; pointer-events: none; }\n  .rsvp .sprig { width: 78px; height: 64px; opacity: .9; }\n  .rsvp .sprig .draw { stroke-dasharray: 120; stroke-dashoffset: 120; animation: draw2 1.6s ease-out 1s both; }", 1)
    return h

if __name__ == "__main__":
    import pathlib, sys
    p = pathlib.Path(__file__).resolve().parent.parent / "demo-workshop" / "index.html"
    p.write_text(apply(p.read_text()))
    print("painted opening applied to", p)
