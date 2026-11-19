"""Convert the square kit posts to 4:5 (1080x1350) by extending the background
top and bottom, seamlessly. Writes to ../v4/."""
import os, sys
from PIL import Image, ImageFilter, ImageDraw
import numpy as np

K = "/home/claude/ig/kit"; OUT = "/home/claude/ig/v4"
os.makedirs(OUT, exist_ok=True)
PAD = 135  # (1350-1080)/2

def extend_cream(im):
    """Flat-ish cream backgrounds: replicate the edge rows with a tiny ramp, feather the seam."""
    w, h = im.size
    a = np.asarray(im).astype(np.float32)
    top = a[0:1].repeat(PAD, axis=0)        # replicate top row
    bot = a[h-1:h].repeat(PAD, axis=0)      # replicate bottom row
    # gentle continuation of the vertical light (top gets +1.5 lighter, bottom -1.5 darker)
    ramp = np.linspace(1.5, 0, PAD)[:, None, None]
    top = np.clip(top + ramp, 0, 255)
    ramp2 = np.linspace(0, -1.5, PAD)[:, None, None]
    bot = np.clip(bot + ramp2, 0, 255)
    out = np.concatenate([top, a, bot], axis=0)
    o = Image.fromarray(out.astype(np.uint8))
    # soften the two seams a touch (blur a 24px band around each)
    for y in (PAD, PAD + h):
        band = o.crop((0, y - 12, w, y + 12)).filter(ImageFilter.GaussianBlur(3))
        o.paste(band, (0, y - 12))
    return o

def extend_burgundy(im):
    """Post 8: rebuild the radial burgundy ground, re-place the card with a feathered edge."""
    w, h = im.size
    W, H = w, h + 2 * PAD
    a = np.asarray(im).astype(np.float32)
    # sample: centre-top (90,26,42), edges/corners (46,11,18); card region ~ x 97-983, y 75-1005
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W / 2, 160.0
    d = np.sqrt(((xx - cx) / 760) ** 2 + ((yy - cy) / 1500) ** 2)
    d = np.clip(d, 0, 1)
    c0 = np.array([92, 27, 43]); c1 = np.array([44, 10, 17])
    bg = c0 * (1 - d[..., None]) + c1 * d[..., None]
    bgim = Image.fromarray(bg.astype(np.uint8))
    # card + its shadow, with a feathered mask
    m = 40
    box = (97 - m, 75 - m, 983 + m, 1005 + m)
    card = im.crop(box)
    mask = Image.new("L", card.size, 0)
    ImageDraw.Draw(mask).rectangle((m - 8, m - 8, card.size[0] - m + 8, card.size[1] - m + 8), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(14))
    bgim.paste(card, (box[0], box[1] + PAD), mask)
    return bgim

if __name__ == "__main__":
    for n in ["post-1-hero", "post-4-1-holiday", "post-4-2-friends", "post-4-3-nye", "post-4-4-brunch", "post-6-phone", "post-7-rsvp"]:
        im = Image.open(f"{K}/{n}.jpg").convert("RGB")
        o = extend_cream(im)
        o.save(f"{OUT}/{n}.jpg", quality=93, subsampling=0)
        print(n, o.size)
    im = Image.open(f"{K}/post-8-not-a-template.jpg").convert("RGB")
    extend_burgundy(im).save(f"{OUT}/post-8-not-a-template.jpg", quality=93, subsampling=0)
    print("post-8 done")
