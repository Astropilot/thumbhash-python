from typing import List, Tuple

from thumbhash.hash import Hash


def thumbhash_to_rgba(
    hash: bytes, base_size: int = 32, saturation_boost: float = 1.25
) -> Tuple[int, int, List[int]]:
    hash_decoded = Hash.decode(hash, saturation_boost)

    w, h = hash_decoded.size(base_size)

    idx = 0
    data: List[int] = [0] * (w * h * 4)

    for y in range(h):
        for x in range(w):
            fx, fy = hash_decoded.coefficients(x, y, w, h)

            l = hash_decoded.l_dc  # noqa: E741
            j = 0
            for cy in range(hash_decoded.ly):
                cx = 1 if cy == 0 else 0
                fy2 = fy[cy] * 2.0

                while cx * hash_decoded.ly < hash_decoded.lx * (hash_decoded.ly - cy):
                    l += hash_decoded.l_ac[j] * fx[cx] * fy2  # noqa: E741
                    j += 1
                    cx += 1

            p = hash_decoded.p_dc
            q = hash_decoded.q_dc

            j = 0
            for cy in range(3):
                cx = 1 if cy == 0 else 0
                fy2 = fy[cy] * 2.0

                while cx < 3 - cy:
                    f = fx[cx] * fy2
                    p += hash_decoded.p_ac[j] * f
                    q += hash_decoded.q_ac[j] * f
                    j += 1
                    cx += 1

            a = hash_decoded.a_dc

            if hash_decoded.has_alpha:
                j = 0
                for cy in range(5):
                    cx = 1 if cy == 0 else 0
                    fy2 = fy[cy] * 2.0

                    while cx < 5 - cy:
                        a += hash_decoded.a_ac[j] * fx[cx] * fy2
                        j += 1
                        cx += 1

            b = l - 2.0 / 3.0 * p
            r = (3.0 * l - b + q) / 2.0
            g = r - q

            data[idx] = round(max(0.0, min(1.0, r) * 255.0))
            data[idx + 1] = round(max(0.0, min(1.0, g) * 255.0))
            data[idx + 2] = round(max(0.0, min(1.0, b) * 255.0))
            data[idx + 3] = round(max(0.0, min(1.0, a) * 255.0))

            idx += 4

    return w, h, data
