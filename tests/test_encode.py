from tests.data import ENCODE_DATA_TEST
from thumbhash import image_to_thumbhash


def test_encode_from_path() -> None:
    for image_path, thumb_hash, _ in ENCODE_DATA_TEST:
        hash = image_to_thumbhash(image_path)

        assert hash == thumb_hash


def test_encode_from_memfile() -> None:
    for image_path, thumb_hash, _ in ENCODE_DATA_TEST:
        with image_path.open("rb") as image_file:
            hash = image_to_thumbhash(image_file)

            assert hash == thumb_hash
