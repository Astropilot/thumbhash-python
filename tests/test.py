from itertools import chain

from PIL import Image
from PIL.ImageOps import exif_transpose

from thumbhash.decode import thumbhash_to_rgba
from thumbhash.encode import rgba_to_thumbhash

image = exif_transpose(Image.open("data/opera.png")).convert("RGBA")

red_band = image.get_flattened_data(band=0)
green_band = image.get_flattened_data(band=1)
blue_band = image.get_flattened_data(band=2)
alpha_band = image.get_flattened_data(band=3)
rgba_data = list(
    chain.from_iterable(zip(red_band, green_band, blue_band, alpha_band, strict=True))
)
width, height = image.size
image.close()

hash = rgba_to_thumbhash(width, height, rgba_data)  # type: ignore

width, height, new_rgba_data = thumbhash_to_rgba(hash)

image = Image.frombytes("RGBA", (width, height), bytes(new_rgba_data))

image.show()
