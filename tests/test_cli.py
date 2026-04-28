from typer.testing import CliRunner

from tests.data import ENCODE_DATA_TEST
from thumbhash.cli import app

runner = CliRunner()


def test_encode() -> None:
    for image_path, thumb_hash, _ in ENCODE_DATA_TEST:
        result = runner.invoke(app, ["encode", str(image_path)])

        assert result.exit_code == 0
        assert f"Thumbhash (base64): {thumb_hash}" in result.stdout


# def test_decode_stdout() -> None:
#     for _, thumb_hash, png_base64 in ENCODE_DATA_TEST:
#         result = runner.invoke(app, ["decode", "-", thumb_hash])

#         assert result.exit_code == 0
#         assert result.output.replace("\n", "") == png_base64
