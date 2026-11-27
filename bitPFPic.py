"""Experimental flat-colour pixel portraits using Pillow.

Run: python cartoon_pfp.py
Optional: python cartoon_pfp.py another-photo.jpg --show
"""

import argparse
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


# Change one setting at a time when comparing results.
GRID_WIDTH = 55
SCALE = 8
SMOOTHING = 7             # Odd number: 3, 5, 7, or 9.
CONTRAST = 1.3
POSTERIZE_BITS = 3        # Lower means fewer levels per colour channel.
SHADOW_THRESHOLD = 110    # Higher makes more of the picture black.

COLOURS = [
    (0, 0, 0),           # Black shadows
    (239, 160, 86),      # Main skin tone
    (214, 157, 87),      # Skin shade
    (145, 100, 58),      # Warm accent
    (95, 89, 65),        # Hair accent
    (173, 170, 164),     # Gray highlight
    (255, 255, 255),     # white background
]


def cartoon_portrait(photo):
    photo = photo.convert("RGB")

    # Normalize processing size while keeping the portrait proportions.
    working = photo.copy()
    working.thumbnail((512, 512), Image.Resampling.LANCZOS)

    # Smooth small photographic details before reducing the resolution.
    working = working.filter(ImageFilter.MedianFilter(SMOOTHING))
    height = max(1, round(working.height * GRID_WIDTH / working.width))
    small = working.resize((GRID_WIDTH, height), Image.Resampling.LANCZOS)

    # Measure shadows BEFORE contrast/posterization so this control is stable.
    brightness = small.convert("L")
    shadows = brightness.point(
        lambda value: 255 if value < SHADOW_THRESHOLD else 0
    )

    # Flatten shading and strengthen the separation between light and dark.
    flat = ImageEnhance.Contrast(small).enhance(CONTRAST)
    flat = ImageOps.posterize(flat, POSTERIZE_BITS)

    # Map pixels to a deliberately chosen palette with no dotted shading.
    palette = Image.new("P", (1, 1))
    entries = COLOURS + [COLOURS[0]] * (256 - len(COLOURS))
    palette.putpalette([channel for colour in entries for channel in colour])
    mapped = flat.quantize(palette=palette, dither=Image.Dither.NONE)
    mapped = mapped.convert("RGB")

    # Replace the darkest regions with solid black.
    mapped.paste((0, 0, 0), (0, 0), shadows)

    # Make each grid pixel a sharp SCALE-by-SCALE block.
    return mapped.resize(
        (GRID_WIDTH * SCALE, height * SCALE), Image.Resampling.NEAREST
    )


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, default=folder / "black.jpg")
    parser.add_argument("--output", type=Path, default=folder / "cartoon-avatar.png")
    parser.add_argument("--show", action="store_true", help="Open the saved image")
    args = parser.parse_args()

    with Image.open(args.input) as source:
        result = cartoon_portrait(source)
    result.save(args.output, format="PNG")
    print(f"Saved {result.width} x {result.height} portrait to {args.output}")
    if args.show:
        result.show()
