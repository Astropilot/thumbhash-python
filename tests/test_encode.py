from thumbhash import image_to_thumbhash

from tests.data import ENCODE_DATA_TEST


def test_encode_from_path() -> None:
    for IMAGE_PATH, THUMBHASH in ENCODE_DATA_TEST.items():
        hash = image_to_thumbhash(IMAGE_PATH)

        assert hash == THUMBHASH


def test_encode_from_memfile() -> None:
    for IMAGE_PATH, THUMBHASH in ENCODE_DATA_TEST.items():
        with open(IMAGE_PATH, "rb") as image_file:
            hash = image_to_thumbhash(image_file)

            assert hash == THUMBHASH
