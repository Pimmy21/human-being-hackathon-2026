# Purrpose design

A design example for the logo and home screen. No product code here.

## Logo (`logo/`)

The mark is a speech bubble shaped like a cat's head: one sly eye, one wink, a small nose, a "ω" mouth and three whiskers a side, all cut out of one solid shape. The speech bubble stands for "you talk to it", and the cat face for the animals.

| File | Use |
|---|---|
| `purrpose-lockup.svg` / `.png` | Main logo: gradient cat + `purrpose.` wordmark |
| `purrpose-lockup-black.svg`, `-white.svg` | One-colour lockups for print and dark backgrounds |
| `purrpose-symbol.svg` | The cat on its own (black master) |
| `purrpose-symbol-gradient.svg` | The cat in the brand gradient |
| `purrpose-symbol-small.svg` | Simplified cat for 16–32 px (no whiskers or nose, heavier eyes and mouth) |
| `purrpose-app-icon.svg`, `-small.svg` | White cat on the gradient tile |
| `purrpose-wordmark.svg` | `purrpose.` on its own |
| `variants/` | Black, white, single-colour violet and square versions + 512 px PNGs |
| `web/` | `favicon.ico`, `favicon.svg`, favicon PNGs, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png` |

**Colours** (Lovable-style gradient, top-left to bottom-right):
Blue `#4B7BFF` → Lavender `#A993FF` → Pink `#FF3D9A`. Text `#1B1B1F`, background `#FBFAF7`. One-colour violet `#7B6CFF`.

**Warm alternative:** Amber `#FFB21E` → Coral `#FF6A5C` → Pink `#FF3D9A` → Lavender `#A993FF`. Warm versions of the gradient files are in `logo/warm/`, and warm favicons are in `logo/web/warm/`. The one-colour files are the same for both schemes.

**Type:** Inter (SIL Open Font License), weight 650, outlined in the wordmark.

**Small sizes:** use `purrpose-symbol-small.svg` / `purrpose-app-icon-small.svg` below about 48 px.

To rebuild every SVG from the geometry, you need Python with `skia-pathops` and `fontTools`, plus the Inter variable font:
`python logo/source/build_logo.py logo path/to/Inter[opsz,wght].ttf`

## Home screen (`home/index.html`)

Open the file in a browser; there's no build step. It shows the light theme, the soft gradient glow, the navigation, the headline and the prompt box. The two round swatches in the header switch between the Lovable (cool) and warm colour schemes; this changes the logo, the glow and the favicon, and the page remembers the choice. The example chips fill the box. Sending only shows a "design preview" note, because nothing is connected and the example appeals are made up.
