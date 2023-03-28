from itertools import chain

from PIL import Image
from PIL.ImageOps import exif_transpose
from thumbhash.decode import thumbhash_to_rgba
from thumbhash.encode import rgba_to_thumbhash

image = exif_transpose(Image.open("data/opera.png")).convert("RGBA")

red_band = image.getdata(band=0)
green_band = image.getdata(band=1)
blue_band = image.getdata(band=2)
alpha_band = image.getdata(band=3)
rgba_data = list(chain.from_iterable(zip(red_band, green_band, blue_band, alpha_band)))
width, height = image.size
image.close()

hash = rgba_to_thumbhash(width, height, rgba_data)

width, height, rgba_data = thumbhash_to_rgba(hash)

image = Image.frombytes("RGBA", (width, height), bytes(rgba_data))

image.show()
