<h1 align="center">
    <br>
    ThumbHash for Python
</h1>

<p align="center">
<a href="https://github.com/Astropilot/thumbhash-python/actions?query=workflow%3ATest+event%3Apush+branch%3Amain" target="_blank">
    <img src="https://github.com/Astropilot/thumbhash-python/workflows/Test/badge.svg?event=push&branch=main" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/Astropilot/thumbhash-python" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/Astropilot/thumbhash-python.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/thumbhash-python" target="_blank">
    <img src="https://img.shields.io/pypi/v/thumbhash-python?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/thumbhash-python" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/thumbhash-python.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://github.com/Astropilot/thumbhash-python/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/Astropilot/thumbhash-python" alt="MIT License">
</a>
</p>

# Introduction

The thumbhash library implements the [Thumbhash](https://evanw.github.io/thumbhash/) image placeholder generation algorithm invented by [Evan Wallace](https://madebyevan.com/) in Python.

A full explanation and interactive example of the algorithm can be found at https://github.com/evanw/thumbhash

# Installation

You need Python 3.7+.

```console
$ pip install thumbhash-python
```

# Usage

Create thumbhash from image file:
```py
from thumbhash import image_to_thumbhash

with open('image.jpg', 'rb') as image_file:
    hash = image_to_thumbhash(image_file)
```

You can also pass file name as parameter to the function:
```py
from thumbhash import image_to_thumbhash

hash = image_to_thumbhash('image.jpg')
```
These functions use the Pillow library to read the image.

If you want to directly convert a rgba array to a thumbhash, you can use the low-level function:
```py
from thumbhash.encode import rgba_to_thumbhash

rgba_to_thumbhash(w: int, h: int, rgba: Sequence[int]) -> bytes
```

To decode a thumbhash into an image:
```py
from thumbhash import thumbhash_to_image

image = thumbhash_to_image("[THUMBHASH]", base_size=128)

image.show()

image.save('path/to/file.png')
```

Alternatively you can use the following function to deal directly with the pixels array (without relying on Pillow):
```py
from thumbhash.decode import thumbhash_to_rgba

def thumbhash_to_rgba(
    hash: bytes, base_size: int = 32, saturation_boost: float = 1.25
) -> Tuple[int, int, List[int]]
```

## CLI

You can also use the CLI mode to encode or decode directly via your shell.

**Usage**:

```console
$ thumbhash [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `decode`: Save thumbnail image from thumbhash
* `encode`: Get thumbhash from image

### `thumbhash decode`

Save thumbnail image from thumbhash

**Usage**:

```console
$ thumbhash decode [OPTIONS] IMAGE_PATH HASH
```

**Arguments**:

* `IMAGE_PATH`: The path where the image created from the hash will be saved  [required]
* `HASH`: The base64-encoded thumbhash  [required]

**Options**:

* `-s, --size INTEGER RANGE`: The base size of the output image  [default: 32; x>=1]
* `--saturation FLOAT`: The saturation boost factor to use  [default: 1.25]
* `--help`: Show this message and exit.

### `thumbhash encode`

Get thumbhash from image

**Usage**:

```console
$ thumbhash encode [OPTIONS] IMAGE_PATH
```

**Arguments**:

* `IMAGE_PATH`: The path of the image to convert  [required]

**Options**:

* `--help`: Show this message and exit.


## Contributing

See [Contributing documentation](./.github/CONTRIBUTING.md)

## License

`thumbhash-python` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
