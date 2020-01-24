import io
import struct
import zlib
from typing import Iterable, NamedTuple

PNG_SIGNATURE = b'\x89PNG\x0d\x0a\x1a\x0a'
COLOR_TYPE = 2
COLOR_DEPTH = 8
FILTER_TYPE = 0


class RGBColor(NamedTuple):
    red: int
    green: int
    blue: int


class ImageSize(NamedTuple):
    height: int
    width: int


class ImageShape:
    def __init__(self, size: ImageSize, scale=1):
        self.size = size
        self.scale = scale
        self.real_size = self.size._replace(height=self.size.height * self.scale,
                                            width=self.size.width * self.scale)

    def create_png(self, pixels: Iterable[Iterable[RGBColor]]) -> bytes:
        png_bytes = io.BytesIO()
        png_bytes.write(PNG_SIGNATURE)
        png_bytes.write(self._create_header_chunk())
        png_bytes.write(self._create_data_chunk(pixels))
        png_bytes.write(self._create_end_chunk())
        return png_bytes.getvalue()

    def _create_chunk(self, type_: bytes, data: bytes) -> bytes:
        chunk = io.BytesIO()
        chunk.write(struct.pack('!I', len(data)))
        chunk.write(type_)
        chunk.write(data)
        checksum = zlib.crc32(type_ + data)
        chunk.write(struct.pack('!I', checksum))
        return chunk.getvalue()

    def _create_header_chunk(self,
                             depth: int = COLOR_DEPTH,
                             color_type: int = COLOR_TYPE) -> bytes:

        chunk_data = struct.pack('!IIBBBBB', self.real_size.width, self.real_size.height,
                                 depth, color_type, 0, 0, 0)
        return self._create_chunk(b'IHDR', chunk_data)

    def _create_data_chunk(self,
                           pixels: Iterable[Iterable[RGBColor]],
                           filter_type: int = FILTER_TYPE) -> bytes:
        buffer = io.BytesIO()
        for line in pixels:
            for _ in range(self.scale):
                buffer.write(struct.pack('!B', filter_type))
                for color in line:
                    buffer.write(struct.pack('!BBB', *color) * self.scale)

        compressed_data = zlib.compress(buffer.getvalue())
        return self._create_chunk(b'IDAT', compressed_data)

    def _create_end_chunk(self) -> bytes:
        return self._create_chunk(b'IEND', b'')
