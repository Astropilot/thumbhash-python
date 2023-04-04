import math
from base64 import b64encode
from itertools import chain
from pathlib import Path
from typing import BinaryIO, List, Sequence, Tuple, Union

from PIL import Image
from PIL.ImageOps import exif_transpose
from thumbhash.hash import Hash


def image_to_thumbhash(
    image: Union[str, bytes, Path, BinaryIO],
) -> str:
    m_image = exif_transpose(Image.open(image)).convert("RGBA")

    m_image.thumbnail((100, 100))

    red_band = m_image.getdata(band=0)
    green_band = m_image.getdata(band=1)
    blue_band = m_image.getdata(band=2)
    alpha_band = m_image.getdata(band=3)
    rgb_data = list(
        chain.from_iterable(zip(red_band, green_band, blue_band, alpha_band))
    )
    width, height = m_image.size
    m_image.close()

    hash = rgba_to_thumbhash(width, height, rgb_data)

    return b64encode(hash).decode("utf-8")


def rgba_to_thumbhash(w: int, h: int, rgba: Sequence[int]) -> bytes:
    if w > 100 or h > 100:
        raise ValueError(f"{w}x{h} doesn't fit in 100x100")
    if len(rgba) != w * h * 4:
        raise ValueError("Image data does not fit the given size")

    nb_pixels = w * h
    is_landscape = w > h
    avg_r = 0.0
    avg_g = 0.0
    avg_b = 0.0
    avg_a = 0.0

    for i in range(nb_pixels):
        alpha = float(rgba[i * 4 + 3]) / 255.0
        avg_r += alpha / 255.0 * float(rgba[i * 4])
        avg_g += alpha / 255.0 * float(rgba[i * 4 + 1])
        avg_b += alpha / 255.0 * float(rgba[i * 4 + 2])
        avg_a += alpha

    if avg_a > 0.0:
        avg_r /= avg_a
        avg_g /= avg_a
        avg_b /= avg_a

    has_alpha = avg_a < float(nb_pixels)
    l_limit = 5.0 if has_alpha else 7.0
    max_wh = max(w, h)
    lx = max(1, round((l_limit * w) / max_wh))
    ly = max(1, round((l_limit * h) / max_wh))
    l_channel: List[float] = [0.0] * nb_pixels
    p_channel: List[float] = [0.0] * nb_pixels
    q_channel: List[float] = [0.0] * nb_pixels
    a_channel: List[float] = [0.0] * nb_pixels

    for i in range(nb_pixels):
        alpha = float(rgba[i * 4 + 3]) / 255.0

        r = avg_r * (1.0 - alpha) + alpha / 255.0 * float(rgba[i * 4])
        g = avg_g * (1.0 - alpha) + alpha / 255.0 * float(rgba[i * 4 + 1])
        b = avg_b * (1.0 - alpha) + alpha / 255.0 * float(rgba[i * 4 + 2])

        l_channel[i] = (r + g + b) / 3.0
        p_channel[i] = (r + g) / 2.0 - b
        q_channel[i] = r - g
        a_channel[i] = alpha

    def encode_channel(
        channel: List[float], nx: int, ny: int
    ) -> Tuple[float, List[float], float]:
        dc = 0.0
        ac: List[float] = []
        scale = 0.0
        fx: List[float] = [0.0] * w

        for cy in range(ny):
            cyf = float(cy)
            cx = 0

            while cx * ny < nx * (ny - cy):
                cxf = float(cx)
                f = 0.0

                for x in range(w):
                    fx[x] = math.cos(math.pi / w * cxf * (float(x) + 0.5))

                for y in range(h):
                    fy = math.cos(math.pi / h * cyf * (float(y) + 0.5))

                    for x in range(w):
                        f += channel[x + y * w] * fx[x] * fy

                f /= float(nb_pixels)

                if cx > 0 or cy > 0:
                    ac.append(f)
                    scale = max(scale, abs(f))
                else:
                    dc = f

                cx += 1

        if scale > 0.0:
            for i in range(len(ac)):
                ac[i] = 0.5 + 0.5 / scale * ac[i]

        return (dc, ac, scale)

    l_dc, l_ac, l_scale = encode_channel(l_channel, max(lx, 3), max(ly, 3))
    p_dc, p_ac, p_scale = encode_channel(p_channel, 3, 3)
    q_dc, q_ac, q_scale = encode_channel(q_channel, 3, 3)
    a_dc, a_ac, a_scale = (
        encode_channel(a_channel, 5, 5) if has_alpha else (1.0, [], 1.0)
    )

    hash = Hash(
        l_dc=l_dc,
        p_dc=p_dc,
        q_dc=q_dc,
        l_scale=l_scale,
        has_alpha=has_alpha,
        lx=lx,
        ly=ly,
        p_scale=p_scale,
        q_scale=q_scale,
        is_landscape=is_landscape,
        a_dc=a_dc,
        a_scale=a_scale,
        l_ac=l_ac,
        p_ac=p_ac,
        q_ac=q_ac,
        a_ac=a_ac,
        l_count=0,
    )

    return hash.encode()
