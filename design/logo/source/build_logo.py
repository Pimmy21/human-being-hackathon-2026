"""Build final Purrpose logo SVGs (solid paths, no masks/strokes/text) from the v4-A sketch geometry."""
import sys, os
import pathops
from fontTools.svgLib.path import parse_path
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

OUT, FONT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

BUBBLE = "M4.5 2.5l3.6 4h7.8l3.6-4V12a7 7 0 0 1-7 7H9.2L4.5 22.5V12z"
EYE_L = "M7.5 10.1q1.7.1 3.1 1.2"
EYE_R = "M13.5 11.3q1.5-1.5 3 0"
WHISK = ["M4.5 12.9l2.6.5", "M4.5 14.6h2.6", "M4.5 16.3l2.4-.643",
         "M19.7 12.9l-2.6.5", "M19.7 14.6h-2.6", "M19.7 16.3l-2.4-.643"]
NOSE = "M11.2 12.6h1.6l-.8.9z"
MOUTH_L = "M12 13.7q-.1.9-1.1.9q-1.2 0-1.9-1.1"
MOUTH_R = "M12 13.7q.1.9 1.1.9q1.2 0 1.9-1.1"


def P(d):
    p = pathops.Path()
    parse_path(d, p.getPen())
    return p


def stroked(d, w):
    p = P(d)
    p.stroke(w, pathops.LineCap.ROUND_CAP, pathops.LineJoin.ROUND_JOIN, 4)
    p.convertConicsToQuads()
    return p


def union(paths):
    out = paths[0]
    for p in paths[1:]:
        out = pathops.op(out, p, pathops.PathOp.UNION)
    return out


def to_d(path, transform=(1, 0, 0, 1, 0, 0)):
    pen = SVGPathPen(None, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
    path.draw(TransformPen(pen, transform))
    return pen.getCommands()


def mark(small=False):
    if small:  # favicon cut: heavier features, no whiskers or nose
        cuts = [stroked(EYE_L, 1.9), stroked(EYE_R, 1.9), stroked(MOUTH_L, 1.5), stroked(MOUTH_R, 1.5)]
    else:
        nose = P(NOSE)
        nose_round = stroked(NOSE, .5)
        cuts = [stroked(EYE_L, 1.2), stroked(EYE_R, 1.2), nose, nose_round,
                stroked(MOUTH_L, 1.0), stroked(MOUTH_R, 1.0)] + [stroked(w, .8) for w in WHISK]
    return pathops.op(P(BUBBLE), union(cuts), pathops.PathOp.DIFFERENCE)


# 24-unit sketch -> 256 canvas, centred (bubble bbox x 4.5..19.7, y 2.5..22.5), nudged 2px up optically
S = 10.4
T = (S, 0, 0, S, 128 - 12.1 * S, 126 - 12.5 * S)


def svg(body, w=256, h=256, title="Purrpose logo", defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{defs}{body}</svg>\n')


GRAD = ('<defs><linearGradient id="pp" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#4B7BFF"/><stop offset=".55" stop-color="#A993FF"/>'
        '<stop offset="1" stop-color="#FF3D9A"/></linearGradient></defs>')

full, small = mark(), mark(small=True)
d_full, d_small = to_d(full, T), to_d(small, T)


def write(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(text)


write("purrpose-symbol.svg", svg(f'<path fill="#000" fill-rule="evenodd" d="{d_full}"/>'))
write("purrpose-symbol-small.svg", svg(f'<path fill="#000" fill-rule="evenodd" d="{d_small}"/>', title="Purrpose logo (small sizes)"))
write("purrpose-symbol-gradient.svg", svg(f'<path fill="url(#pp)" fill-rule="evenodd" d="{d_full}"/>', defs=GRAD))
# App tile: gradient squircle-ish rounded square with white mark at ~62% size
TT = (S * .62, 0, 0, S * .62, 128 - 12.1 * S * .62, 127 - 12.5 * S * .62)
write("purrpose-app-icon.svg", svg(
    f'<rect width="256" height="256" rx="58" fill="url(#pp)"/>'
    f'<path fill="#fff" fill-rule="evenodd" d="{to_d(full, TT)}"/>', defs=GRAD, title="Purrpose app icon"))
TS = (S * .66, 0, 0, S * .66, 128 - 12.1 * S * .66, 127 - 12.5 * S * .66)
write("purrpose-app-icon-small.svg", svg(
    f'<rect width="256" height="256" rx="58" fill="url(#pp)"/>'
    f'<path fill="#fff" fill-rule="evenodd" d="{to_d(small, TS)}"/>', defs=GRAD, title="Purrpose app icon (small sizes)"))

# Wordmark "purrpose." in Inter SemiBold-ish (wght 650, opsz 32), outlined, tracking -2%
font = instantiateVariableFont(TTFont(FONT), {"wght": 650, "opsz": 32})
gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
upm = font["head"].unitsPerEm
text, track = "purrpose.", -0.02 * upm
x = 0
word = pathops.Path()
for ch in text:
    g = cmap[ord(ch)]
    gp = pathops.Path()
    gs[g].draw(TransformPen(gp.getPen(), (1, 0, 0, 1, x, 0)))
    word.addPath(gp)
    x += hmtx[g][0] + track
word = pathops.simplify(word, clockwise=False)
xmin, ymin, xmax, ymax = word.bounds
x_height = font["OS/2"].sxHeight
# Lockup: wordmark x-height ~= 46% of symbol height; baseline aligned near bubble's lower body
sym_h = (22.5 - 2.5) * S                     # 208 px
ws = (sym_h * 0.46) / x_height
gap = 34
sym_w = (19.7 - 4.5) * S
LX0 = 24
sym_T = (S, 0, 0, S, LX0 - 4.5 * S, 24 - 2.5 * S)   # symbol occupies y 24..232
baseline = 24 + 16.6 * S                         # sits at the bottom of the face, above the tail
word_x = LX0 + sym_w + gap - xmin * ws
W_T = (ws, 0, 0, -ws, word_x, baseline)
total_w = int(word_x + xmax * ws + 24)
d_word = to_d(word, W_T)
d_sym_l = to_d(full, sym_T)
write("purrpose-lockup.svg", svg(
    f'<path fill="url(#pp)" fill-rule="evenodd" d="{d_sym_l}"/><path fill="#1B1B1F" d="{d_word}"/>',
    w=total_w, defs=GRAD, title="Purrpose"))
write("purrpose-lockup-black.svg", svg(
    f'<path fill="#000" fill-rule="evenodd" d="{d_sym_l}"/><path fill="#000" d="{d_word}"/>', w=total_w, title="Purrpose"))
write("purrpose-lockup-white.svg", svg(
    f'<path fill="#fff" fill-rule="evenodd" d="{d_sym_l}"/><path fill="#fff" d="{d_word}"/>', w=total_w, title="Purrpose"))
# Wordmark alone
wpad = 8
write("purrpose-wordmark.svg", svg(
    f'<path fill="#1B1B1F" d="{to_d(word, (1, 0, 0, -1, -xmin + wpad, ymax + wpad))}"/>',
    w=int(xmax - xmin + 2 * wpad), h=int(ymax - ymin + 2 * wpad), title="purrpose."))
print("contours full/small:", len(list(full.contours)), len(list(small.contours)), "lockup width", total_w)

# Warm colour scheme: same artwork, amber -> coral -> pink -> lavender gradient
GRAD_WARM = ('<defs><linearGradient id="pp" x1="0" y1="0" x2="1" y2="1">'
             '<stop offset="0" stop-color="#FFB21E"/><stop offset=".5" stop-color="#FF6A5C"/>'
             '<stop offset=".8" stop-color="#FF3D9A"/><stop offset="1" stop-color="#A993FF"/></linearGradient></defs>')
os.makedirs(os.path.join(OUT, "warm"), exist_ok=True)
for name in ["purrpose-lockup", "purrpose-symbol-gradient", "purrpose-app-icon", "purrpose-app-icon-small"]:
    with open(os.path.join(OUT, name + ".svg"), encoding="utf-8") as f:
        src = f.read()
    assert GRAD in src
    write(os.path.join("warm", name + "-warm.svg"), src.replace(GRAD, GRAD_WARM))
