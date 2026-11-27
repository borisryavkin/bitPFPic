from PIL import Image, ImageEnhance

# Settings to experiment with.
GRID_WIDTH = 55
CONTRAST = 1.8
SATURATION = 1.3
SCALE = 8

# Open the photo and convert to RGB.
with Image.open("black.jpg") as sourcePic:
    rgb = sourcePic.convert("RGB")

# Preserve the original proportions.
grid_height = round(rgb.height * GRID_WIDTH / rgb.width)

# Shrink to a small pixel grid.
small = rgb.resize(
    (GRID_WIDTH, grid_height),
    resample=Image.Resampling.LANCZOS,
)

# Strengthen shadows and colours.
small = ImageEnhance.Contrast(small).enhance(CONTRAST)
small = ImageEnhance.Color(small).enhance(SATURATION)

# Choose the colours available in the finished portrait.
colours = [
    (0, 0, 0),        # Black
    (239, 160, 86),   # Warm skin
    (214, 157, 87),   # Darker skin
    (146, 86, 44),    # Brown shadow
    (95, 89, 65),     # Muted olive
    (90, 84, 79),     # Dark gray
    (173, 170, 164),  # Light gray
    (239, 250, 250),  # Pale background
]

# Create a palette image.
palette = Image.new("P", (1, 1))

# Pillow expects 256 RGB entries.
# Fill unused entries with black.
entries = colours + [colours[0]] * (256 - len(colours))

flat_palette = [
    channel
    for colour in entries
    for channel in colour
]

palette.putpalette(flat_palette)

# Map the photo to our palette without dotted shading.
pixel_art = small.quantize(
    palette=palette,
    dither=Image.Dither.NONE,
)

# Enlarge while keeping sharp square pixels.
result = pixel_art.resize(
    (GRID_WIDTH * SCALE, grid_height * SCALE),
    resample=Image.Resampling.NEAREST,
)

# Save and display.
result.save("pixel-avatar.png")
result.show()