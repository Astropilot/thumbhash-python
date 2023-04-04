from thumbhash.cli import app
from typer.testing import CliRunner

from tests.data import ENCODE_DATA_TEST

runner = CliRunner()


def test_encode() -> None:
    for IMAGE_PATH, THUMBHASH in ENCODE_DATA_TEST.items():
        result = runner.invoke(app, ["encode", str(IMAGE_PATH)])

        assert result.exit_code == 0
        assert f"Thumbhash (base64): {THUMBHASH}" in result.stdout
