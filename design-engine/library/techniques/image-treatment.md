# Technique — image treatment (the re-ink pipeline)

Turns ANY supplied image (board reference, operator's Midjourney output, a
photo) into a brand asset. This is the default way to produce hero art —
it inherits the reference's craft density for free.

## The pipeline (worked example: the arch-hall hero)
```sh
T=design-engine/tools
# 1. know what's in it
python3 $T/image_lab.py sample library/boards/midcentury-editorial/arch-hall.jpg --k 10
# 2. size for the web first (map is O(pixels))
python3 $T/image_lab.py resize IN.jpg --width 1400 --out /tmp/w.png
# 3. re-ink onto the brand palette: brand inks + warm neutrals so paper-ish
#    areas map to neutrals and orange stays reserved for the glow
python3 $T/image_lab.py map /tmp/w.png --levels 5 --boost 1.05 \
  --palette "#F7F2E3,#FBF8EE,#EFE7D2,#DCD2BA,#C9BC9E,#AE9F7C,#6E7182,#4C4F5E,#24408E,#3355B4,#557CD4,#6E93E0,#131C33,#1D1F28,#E8752C,#B4531A" \
  --out /tmp/inked.png
# 4. paper grain
python3 $T/image_lab.py grain /tmp/inked.png --amount 6 --out hero.png
```

## Palette selection rules
- Start from brand.json theme values + line tokens (the neutrals matter: they
  catch documents/machines so orange stays the single glow).
- 12–16 inks total. Fewer = posterier/stronger; more = softer.
- If an unwanted color dominates, REMOVE the ink it maps to rather than
  editing pixels.

## Variants
- `duotone --dark "#131C33" --light "#F7F2E3" [--mid "#3355B4"]` — quiet
  section art, backgrounds behind text.
- `halftone --color "#3355B4" --bg "#F7F2E3" --cell 6` — print-dot texture
  panels, OG card backgrounds.
- `outline` composited over a map/duotone = printed-illustration ink pass.

## Delivery rules
- Artifacts must be self-contained: embed processed images as data-URI JPEG
  (quality ~85, sized to display width) — sandboxed viewers load nothing
  external.
- Production assets: commit the processed file + record source image, command
  and palette in the asset's sidecar note (regenerability = brand law).

## Generating NEW imagery (imagegen.py)
When no suitable reference exists, generate one — then re-ink it like any
reference:
```sh
python3 design-engine/tools/imagegen.py \
  "a vast reading room of receding blue arches, archive shelves of printed
   documents, one glowing orange pendant lamp, a figure reading" \
  --style midcentury-editorial --reink --out design-engine/out/gen/hero.png
```
Needs IMAGEGEN_PROVIDER + the provider's key in the environment. --style
bakes the board's system language into the prompt; --reink guarantees the
output lands on the brand palette. Generated files are treated exactly like
board references afterwards (crop, composite, grain, commit with sidecar).
