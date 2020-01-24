import string
import sys

from image import ImageShape, ImageSize, RGBColor
from painter import NumberPainter

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: create_png.py <number>')
        sys.exit(1)

    number = sys.argv[1]
    symbols = {*string.digits, '.', '-'}
    unknown_symbols = set(number) - symbols
    if unknown_symbols:
        print(f'Unknown symbols: {unknown_symbols}')
        sys.exit(1)

    painter = NumberPainter(color=RGBColor(0, 0, 0))
    pixels = painter.draw_number(number).get_pixels()
    size = ImageSize(painter.canvas_height, painter.canvas_width)
    png = ImageShape(size, scale=15).create_png(pixels)
    with open('out.png', 'wb') as file:
        file.write(png)
