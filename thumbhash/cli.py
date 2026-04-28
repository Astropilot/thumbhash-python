from base64 import b64encode
import io
from pathlib import Path
from typing import Any

import typer
from rich import print
from thumbhash import image_to_thumbhash, thumbhash_to_image
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def encode(
    image_path: Path = typer.Argument(
        ...,
        help="The path of the image to convert",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
    ),
) -> None:
    """
    Get thumbhash from image
    """
    hash = image_to_thumbhash(image_path)

    print(f"Thumbhash (base64): [green]{hash}[/green]")


@app.command()
def decode(
    image_path: Path = typer.Argument(
        ...,
        help="The path where the image created from the hash will be saved, '-' for stdout (base64)",
        file_okay=True,
        dir_okay=False,
    ),
    hash: str = typer.Argument(..., help="The base64-encoded thumbhash"),
    size: int = typer.Option(
        32, "--size", "-s", help="The base size of the output image", min=1
    ),
    saturation: float = typer.Option(1.25, help="The saturation boost factor to use"),
) -> None:
    """
    Save thumbnail image from thumbhash
    """
    image = thumbhash_to_image(hash, size, saturation)

    if f"{image_path}" == "-":
        b = io.BytesIO()
        image.save(b, "png")
        print(f"PNG (base64): [green]{b64encode(b.getvalue()).decode('utf-8')}[/green]")
    else:
        image.save(image_path)


def main() -> Any:
    return app()
