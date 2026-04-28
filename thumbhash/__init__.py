import importlib.metadata

try:
    __version__ = importlib.metadata.version("thumbhash-python")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

from thumbhash.decode import thumbhash_to_image as thumbhash_to_image
from thumbhash.encode import image_to_thumbhash as image_to_thumbhash

__all__ = ["image_to_thumbhash", "thumbhash_to_image"]
