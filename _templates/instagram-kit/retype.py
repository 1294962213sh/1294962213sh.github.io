"""Post 9 (pinned offer): bigger painted bouquet in a gold-rimmed medallion, serif body copy.
Post 8: re-set the five-line table so every row is one line and evenly spaced."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = "/home/claude/ig/fonts"
K = "/home/claude/ig/kit"; OUT = "/home/claude/ig/v4"

def font(name, size, wght):
    f = ImageFont.truetype(f"{F}/{name}", size)
    try: f.set_variation_by_axes([wght])
    except Exception as e: print("variation failed", e)
    return f

def tracked(d, xy, text, f, fill, tracking, anchor="m"):
    """Draw letter-spaced text centred (anchor m) or left (l) at xy."""
    widths = [d.textlength(ch, font=f) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x, y = xy
    if anchor == "m": x = x - total / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=f, fill=fill); x += w + tracking
    return total

# ---------- Post 9 ----------
def post9():
    src = Image.open(f"{K}/post-9-offer.jpg").convert("RGB")
    W, H = src.size
    bg = (239, 230, 215)
    im = Image.new("RGB", (W, H), bg)
    im.paste(src.crop((0, 0, W, 430)), (0, 0))          # keep eyebrow + headline exactly
    d = ImageDraw.Draw(im)
    # medallion
    cx, cy, R = W // 2, 728, 285
    ground = (243, 236, 220)
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=ground)
    # the painting, from the approved profile picture (same art), scaled to ~82% of the medallion
    pp = Image.open(f"{K}/profile-picture.jpg").convert("RGB")
    art = pp.crop((144, 225, 970, 850))                  # soft-edged painting incl. vignette
    scale = 470 / 685                                   # painted mass 685px -> 470px
    art = art.resize((int(art.width * scale), int(art.height * scale)), Image.LANCZOS)
    # feather the art's rectangle so it melts into the medallion ground
    mask = Image.new("L", art.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((18, 18, art.width - 18, art.height - 18), radius=120, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(22))
    ax, ay = cx - art.width // 2 + 4, cy - art.height // 2 + 6
    im.paste(art, (ax, ay), mask)
    # gold double hairline ring (like the card frames)
    gold = (168, 135, 63)
    for r, w in ((R + 2, 2), (R + 14, 1)):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=gold, width=w)
    # body copy in the serif, three lines, then the offer line in gold small caps
    ink = (47, 58, 47)
    body = font("CormorantGaramond[wght].ttf", 38, 500)
    y = 1078
    for line in ["Custom, animated invitations, made to order",
                 "One link from a text, Instagram or email  ·  RSVP in one tap",
                 "Plus a short clip for your socials"]:
        d.text((cx, y), line, font=body, fill=ink, anchor="mm"); y += 51
    cta = font("Jost[wght].ttf", 24, 500)
    tracked(d, (cx, 1246), "YOUR FIRST ONE IS ON US  —  DM “INVITE”", cta, (147, 118, 50), 5.5)
    # hairline above the offer line
    d.line((cx - 60, 1226, cx + 60, 1226), fill=(205, 190, 160), width=1)
    im.save(f"{OUT}/post-9-offer.jpg", quality=93, subsampling=0)
    return im

# ---------- Post 8 ----------
ROWS = [("From a gallery", "Made for you, inspired by art"),
        ("A still image", "Animated. It moves"),
        ("Guests sign in", "No app, no sign-up for guests"),
        ("You wire the RSVP", "RSVP tracking built in, for you"),
        ("Ads and upsells", "$15, flat")]

def post8(rows=ROWS, src_path=f"{OUT}/post-8-not-a-template.jpg", out_path=f"{OUT}/post-8-not-a-template.jpg", pad=135):
    im = Image.open(src_path).convert("RGB")
    d = ImageDraw.Draw(im)
    card = (250, 246, 235)
    L, Rr = 168, 910
    top, bot = 337 + pad, 876 + pad
    d.rectangle((L - 10, top - 1, Rr + 10, bot + 2), fill=card)   # clear the old table
    rule = (214, 204, 186); grey = (138, 128, 120); wine = (74, 16, 32); arrow_c = (191, 180, 152)
    left_f = font("CormorantGaramond[wght].ttf", 27, 400)
    right_f = font("CormorantGaramond-Italic[wght].ttf", 44, 500)
    arrow_f = font("Jost[wght].ttf", 20, 400)
    n = len(rows); rh = (bot - top) / n
    for i, (a, b) in enumerate(rows):
        y0 = top + i * rh; ym = y0 + rh / 2
        d.line((L, round(y0), Rr, round(y0)), fill=rule, width=1)
        d.text((L, ym), a, font=left_f, fill=grey, anchor="lm")
        w = d.textlength(a, font=left_f)
        d.line((L, ym + 1, L + w, ym + 1), fill=grey, width=1)                 # strikethrough
        # small hairline arrow (the sans has no arrow glyph)
        d.line((414, ym, 436, ym), fill=arrow_c, width=2)
        d.line((430, ym - 6, 436, ym), fill=arrow_c, width=2); d.line((430, ym + 6, 436, ym), fill=arrow_c, width=2)
        d.text((445, ym), b, font=right_f, fill=wine, anchor="lm")
    d.line((L, bot, Rr, bot), fill=rule, width=1)
    im.save(out_path, quality=93, subsampling=0)
    return im

if __name__ == "__main__":
    post9(); post8(); print("ok")
