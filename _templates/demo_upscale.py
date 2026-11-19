"""Holiday sample page (demo/index.html): wreath emblem replaces the glass icon, hairline + ✦ replaces
the bauble strip, deeper berries, paper grain, calmer motion."""
import re
REPO = "/home/claude/1294962213sh.github.io"
P = f"{REPO}/demo/index.html"
s = open(P).read()
emblem = open("/home/claude/ig/site/emblem.svg").read()

# 1. glass icon -> wreath emblem
a = s.index('      <svg class="glass" viewBox="0 0 54 76"')
b = s.index('</svg>', a) + len('</svg>')
s = s[:a] + "      " + emblem + s[b:]

# 2. bauble strip -> gold hairline with a single ✦ (same ornament as the title divider)
a = s.index('      <svg class="tea strip"')
b = s.index('</svg>', a) + len('</svg>')
s = s[:a] + '      <div class="orn tea2" aria-hidden="true"><svg viewBox="0 0 10 10"><path d="M5 0 L6.2 3.8 L10 5 L6.2 6.2 L5 10 L3.8 6.2 L0 5 L3.8 3.8 Z" fill="currentColor"/></svg></div>' + s[b:]

# 3. deeper berries in the corner garlands (card's own wine red)
s = s.replace('fill="#C73D58"', 'fill="#A8233C"').replace('fill="#D04A64"', 'fill="#B3263A"')

# 4. CSS for the emblem + divider + grain
GRAIN = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'>"
         "<filter id='g'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 0.5  0 0 0 0 0.45  0 0 0 0 0.38  0 0 0 1 0'/></filter>"
         "<rect width='220' height='220' filter='url(%23g)'/></svg>\")")
css = f"""  .glass.wreath-emblem {{ width: 128px; height: 141px; margin: 0 auto 10px; overflow: visible; }}
  .orn.tea2 {{ margin: 18px auto 2px; }}
  .invite::after, .rsvp::after {{ content: ""; position: absolute; inset: 0; pointer-events: none; border-radius: inherit; background-image: {GRAIN}; opacity: .08; mix-blend-mode: multiply; z-index: 0; }}
  .invite > *, .rsvp > * {{ position: relative; z-index: 1; }}
"""
s = s.replace("  .glass { display: block; margin: 0 auto 14px; width: 48px; height: 70px; }",
              "  .glass { display: block; margin: 0 auto 14px; width: 48px; height: 70px; }\n" + css)
motion = """    .glass .lf { opacity: 0; animation: paint .8s ease-out both; }
    .glass .pop { transform-box: view-box; animation: pop .7s ease-out both; }
    .glass .bell { transform-box: view-box; animation: bellswing 4.4s ease-in-out infinite; }
    .glass .sp { transform-box: view-box; animation: twinkle 5.5s ease-in-out infinite; } .glass .s2 { animation-delay: 1.4s; animation-duration: 6.4s } .glass .s4 { animation-delay: 2.6s; animation-duration: 7.2s }
    .glass .draw { stroke-dasharray: 220; stroke-dashoffset: 220; animation: draw2 2s ease-out .5s both; }
    .glass .glint2 { animation: glint 5s ease-in-out 2.6s infinite; }
    .orn.tea2 { animation-delay: .92s }
"""
anchor = "    .glass .liquid { animation: fill 1.4s cubic-bezier(.4,0,.2,1) .4s both, sway 4.5s ease-in-out 2s infinite; }"
assert s.count(anchor) == 1
s = s.replace(anchor, motion + "    .glass .liquid { animation: fill 1.4s cubic-bezier(.4,0,.2,1) .6s both, sway 6.5s ease-in-out 2s infinite; }")
s = s.replace("  @keyframes pop {", "  @keyframes paint { from { opacity: 0 } to { opacity: 1 } }\n  @keyframes bellswing { 0%,100% { transform: rotate(-6deg) } 50% { transform: rotate(6deg) } }\n  @keyframes pop {", 1)

# 5. calmer motion
rep = {
 "    .glass .wine { animation: slosh 3.6s linear infinite; }": "    .glass .wine { animation: slosh 5.2s linear infinite; }",
 "    .glass .wine2 { animation: slosh 5s linear infinite reverse; }": "    .glass .wine2 { animation: slosh 7s linear infinite reverse; }",
 "    .corner .bokeh, .bloom .bokeh { animation: bokeh 6s ease-in-out infinite; }": "    .corner .bokeh, .bloom .bokeh { animation: bokeh 9s ease-in-out infinite; }",
 "    .corner .strand { transform-box: view-box; animation: swayz 6s ease-in-out infinite; }": "    .corner .strand { transform-box: view-box; animation: swayz 8s ease-in-out infinite; }",
 "    .sparkle { animation: twinkle 3.2s ease-in-out infinite; }": "    .sparkle { animation: twinkle 5.2s ease-in-out infinite; }",
 "    .corner { animation: glow 5s ease-in-out 2.5s infinite; }": "    .corner { animation: glow 7s ease-in-out 2.5s infinite; }",
}
for k, v in rep.items():
    assert s.count(k) == 1, k
    s = s.replace(k, v)
s = re.sub(r"animation: sweep 9s ease-in-out (\d+)s infinite", r"animation: sweep 14s ease-in-out \1s infinite", s)
# half the loose sparkles: drop s2, s4, s6, s8
s = re.sub(r'\s*<svg class="art sparkle s[2468]"[^\n]*\n', "\n", s)
# remove the now-unused tea/strip CSS lines
s = s.replace("  .tea { display: block; width: 150px; height: 44px; margin: 16px auto 0; }\n  .tea .steam { opacity: .7; }\n", "")
open(P, "w").write(s)
print("demo page written")
