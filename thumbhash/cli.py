import io
from base64 import b64encode
from pathlib import Path
from typing import Annotated, Any

import typer
from rich import print
from rich.console import Console

from thumbhash import image_to_thumbhash, thumbhash_to_image

app = typer.Typer()


@app.command()
def encode(
    image_path: Annotated[
        Path,
        typer.Argument(
            help="The path of the image to convert",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ],
) -> None:
    """
    Get thumbhash from image
    """
    hash = image_to_thumbhash(image_path)

    print(f"Thumbhash (base64): [green]{hash}[/green]")


@app.command()
def decode(
    image_path: Annotated[
        Path,
        typer.Argument(
            help="The path where the image created from the hash will be saved, '-' for stdout (png base64)",
            file_okay=True,
            dir_okay=False,
            resolve_path=True,
            allow_dash=True,
        ),
    ],
    hash: Annotated[str, typer.Argument(help="The base64-encoded thumbhash")],
    size: Annotated[
        int,
        typer.Option("--size", "-s", help="The base size of the output image", min=1),
    ] = 32,
    saturation: Annotated[
        float, typer.Option(help="The saturation boost factor to use")
    ] = 1.25,
) -> None:
    """
    Save thumbnail image from thumbhash
    """
    image = thumbhash_to_image(hash, size, saturation)

    if str(image_path) == "-":
        b = io.BytesIO()
        console = Console(markup=False, no_color=True, highlight=False)

        image.save(b, "png")
        console.print(b64encode(b.getvalue()).decode("utf-8"))
    else:
        image.save(image_path)


def main() -> Any:
    return app()
