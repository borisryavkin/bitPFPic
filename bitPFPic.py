from PIL import Image, ImageOps

with Image.open("black.jpg") as sourcePic:

#create rgb converter variable
    rgb = sourcePic.convert("RGB")

#crop a square and shrink

small = ImageOps.fit(
    rgb,(64, 64),
    method=Image.Resampling.LANCZOS,
)

#reduce to a 32 color palette 

pixel_art = small.quantize(
    colors=32,
    method=Image.Quantize.MEDIANCUT,
)

pixel_art.show()

#enalrge with shar pixel edges

result = pixel_art.resize(
    (512, 512),
    resample=Image.Resampling.NEAREST,
)
result.show()