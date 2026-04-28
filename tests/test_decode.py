# import io
# from base64 import b64decode, b64encode

# from PIL import Image

# from tests.data import ENCODE_DATA_TEST
# from thumbhash.decode import thumbhash_to_rgba


# def test_decode_to_png_base64() -> None:
#     for _, thumb_hash, png_base64 in ENCODE_DATA_TEST:
#         width, height, new_rgba_data = thumbhash_to_rgba(b64decode(thumb_hash))

#         image = Image.frombytes("RGBA", (width, height), bytes(new_rgba_data))
#         b = io.BytesIO()
#         image.save(b, "png")

#         assert b64encode(b.getvalue()).decode("utf-8") == png_base64
