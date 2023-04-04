from pathlib import Path
from typing import Any

import typer
from rich import print
from thumbhash import image_to_thumbhash, thumbhash_to_image

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
    )
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
        help="The path where the image created from the hash will be saved",
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
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

    image.save(image_path)


def main() -> Any:
    return app()
