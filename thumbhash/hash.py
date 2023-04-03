import math
from dataclasses import dataclass
from typing import List, Tuple

# Hash binary representation:
#
# L DC:        6 bit
# P DC:        6 bit
# Q DC:        6 bit
# L scale:     5 bit
# HasAlpha:    1 bit
#
# L count:     3 bit
# P scale:     6 bit
# Q scale:     6 bit
# IsLandscape: 1 bit
#
# If HasAlpha:
# A DC:        4 bit
# A scale:     4 bit
#
# L AC:        4 bit each
# P AC:        4 bit each
# Q AC:        4 bit each
#
# If HasAlpha:
# A AC:        4 bit each


# Hash represents the set of data stored in an image hash.
@dataclass
class Hash:
    l_dc: float
    p_dc: float
    q_dc: float
    l_scale: float
    has_alpha: bool

    lx: int
    ly: int
    l_count: int
    p_scale: float
    q_scale: float
    is_landscape: bool

    a_dc: float  # if has_alpha
    a_scale: float  # if has_alpha

    l_ac: List[float]
    p_ac: List[float]
    q_ac: List[float]
    a_ac: List[float]  # if has_alpha

    def encode(self) -> bytes:
        # Compute the size of the hash
        nb_ac = len(self.l_ac) + len(self.p_ac) + len(self.q_ac)
        if self.has_alpha:
            nb_ac += len(self.a_ac)
        hash_size = 3 + 2 + (nb_ac + 1) / 2
        if self.has_alpha:
            hash_size += 1

        hash: bytearray = bytearray(int(hash_size))

        # First block (3 bytes)
        header24 = round(63.0 * self.l_dc)
        header24 |= round(31.5 + 31.5 * self.p_dc) << 6
        header24 |= round(31.5 + 31.5 * self.q_dc) << 12
        header24 |= round(31.0 * self.l_scale) << 18
        if self.has_alpha:
            header24 |= 1 << 23

        hash[0] = header24 & 255
        hash[1] = (header24 >> 8) & 255
        hash[2] = header24 >> 16

        # Second block (2 bytes)
        self.l_count = self.lx
        if self.is_landscape:
            self.l_count = self.ly

        header16 = self.l_count
        header16 |= round(63.0 * self.p_scale) << 3
        header16 |= round(63.0 * self.q_scale) << 9
        if self.is_landscape:
            header16 |= 1 << 15
        else:
            header16 |= 0

        hash[3] = header16 & 255
        hash[4] = header16 >> 8

        if self.has_alpha:
            hash[5] = round(15.0 * self.a_dc) | (round(15.0 * self.a_scale) << 4)

        acs: List[List[float]] = [self.l_ac, self.p_ac, self.q_ac]
        if self.has_alpha:
            acs.append(self.a_ac)

        start = 6 if self.has_alpha else 5
        idx = 0

        for i in range(len(acs)):
            ac = acs[i]

            for j in range(len(ac)):
                f = ac[j]

                hash[start + math.floor(idx / 2)] |= round(15.0 * f) << ((idx & 1) * 4)
                idx += 1

        return bytes(hash)

    @staticmethod
    def decode(hash: bytes, saturation_boost: float) -> "Hash":
        if len(hash) < 5:
            raise ValueError("Invalid size hash! Must be at least 5 bytes")

        # First block
        header24 = int(hash[0]) | int(hash[1]) << 8 | int(hash[2]) << 16

        l_dc = float(header24 & 63) / 63.0
        p_dc = float((header24 >> 6) & 63) / 31.5 - 1.0
        q_dc = float((header24 >> 12) & 63) / 31.5 - 1.0
        l_scale = float((header24 >> 18) & 31) / 31.0
        has_alpha = (header24 >> 23) != 0

        # Second block
        header16 = int(hash[3]) | int(hash[4]) << 8

        p_scale = float((header16 >> 3) & 63) / 63.0
        q_scale = float((header16 >> 9) & 63) / 63.0
        is_landscape = (header16 >> 15) != 0

        l_count = int(header16 & 7)
        l_max = 5 if has_alpha else 7
        lx = max(3, l_max if is_landscape else l_count)
        ly = max(3, l_count if is_landscape else l_max)

        a_dc = 1.0
        a_scale = 1.0

        if has_alpha:
            if len(hash) < 6:
                raise ValueError("Invalid size hash! Must be at least 6 bytes")
            a_dc = float(hash[5] & 15) / 15.0
            a_scale = float(hash[5] >> 4) / 15.0

        start = 6 if has_alpha else 5
        idx = 0

        def decode_channel(nx: int, ny: int, scale: float) -> List[float]:
            ac: List[float] = []
            nonlocal idx

            for cy in range(ny):
                cx = 1 if cy == 0 else 0

                while cx * ny < nx * (ny - cy):
                    hidx = start + math.floor(idx / 2)
                    if hidx >= len(hash):
                        raise ValueError("Invalid size hash!")

                    f = (
                        float((hash[hidx] >> ((idx & 1) * 4)) & 15) / 7.5 - 1.0
                    ) * scale
                    ac.append(f)
                    idx += 1
                    cx += 1
            return ac

        l_ac = decode_channel(lx, ly, l_scale)
        p_ac = decode_channel(3, 3, p_scale * saturation_boost)
        q_ac = decode_channel(3, 3, q_scale * saturation_boost)

        a_ac = []
        if has_alpha:
            a_ac = decode_channel(5, 5, a_scale)

        return Hash(
            l_dc=l_dc,
            p_dc=p_dc,
            q_dc=q_dc,
            l_scale=l_scale,
            has_alpha=has_alpha,
            lx=lx,
            ly=ly,
            l_count=l_count,
            p_scale=p_scale,
            q_scale=q_scale,
            is_landscape=is_landscape,
            a_dc=a_dc,
            a_scale=a_scale,
            l_ac=l_ac,
            p_ac=p_ac,
            q_ac=q_ac,
            a_ac=a_ac,
        )

    def size(self, base_size: int) -> Tuple[int, int]:
        ratio = float(self.lx) / float(self.ly)

        if ratio > 1.0:
            return (base_size, round(float(base_size) / ratio))
        else:
            return (round(float(base_size) * ratio), base_size)

    def coefficients(
        self, x: int, y: int, w: int, h: int
    ) -> Tuple[List[float], List[float]]:
        xf, yf, wf, hf = float(x), float(y), float(w), float(h)

        n = 5 if self.has_alpha else 3
        n = max(self.lx, n)

        fx: List[float] = [0.0] * n
        for cx in range(n):
            fx[cx] = math.cos(math.pi / wf * (xf + 0.5) * float(cx))

        n = 5 if self.has_alpha else 3
        n = max(self.ly, n)

        fy: List[float] = [0.0] * n
        for cy in range(n):
            fy[cy] = math.cos(math.pi / hf * (yf + 0.5) * float(cy))

        return fx, fy
