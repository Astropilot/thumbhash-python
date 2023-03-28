from base64 import b64encode
from itertools import chain

from PIL import Image
from PIL.ImageOps import exif_transpose
from thumbhash.encode import rgba_to_thumbhash

from tests.data import ENCODE_DATA_TEST


def test_encode() -> None:
    for IMAGE_PATH, THUMBHASH in ENCODE_DATA_TEST.items():
        image = exif_transpose(Image.open(IMAGE_PATH)).convert("RGBA")

        red_band = image.getdata(band=0)
        green_band = image.getdata(band=1)
        blue_band = image.getdata(band=2)
        alpha_band = image.getdata(band=3)
        rgb_data = list(
            chain.from_iterable(zip(red_band, green_band, blue_band, alpha_band))
        )
        width, height = image.size
        image.close()

        hash = rgba_to_thumbhash(width, height, rgb_data)
        hash_b64 = b64encode(hash).decode("utf-8")

        assert hash_b64 == THUMBHASH
