from typing import Iterable, Tuple

from image import RGBColor

DIGIT_HEIGHT = 7
DEFAULT_COLOR = RGBColor(0, 0, 0)
DEFAULT_BG_COLOR = RGBColor(255, 255, 255)
COLORED_POINTS = {
    '0': ((1, 2, 3, 4, 5), (0, 6), (0, 6), (1, 2, 3, 4, 5)),
    '1': ((2,), (1, 6), (0, 1, 2, 3, 4, 5, 6), (6,)),
    '2': ((1, 5, 6), (0, 4, 6), (0, 3, 6), (1, 2, 6)),
    '3': ((1, 5), (0, 3, 6), (0, 3, 6), (1, 2, 4, 5)),
    '4': ((0, 1, 2), (3,), (3,), (0, 1, 2, 3, 4, 5, 6)),
    '5': ((0, 1, 2, 5), (0, 2, 6), (0, 2, 6), (0, 3, 4, 5)),
    '6': ((1, 2, 3, 4, 5), (0, 3, 6), (0, 3, 6), (1, 4, 5)),
    '7': ((0,), (0, 5, 6), (0, 3, 4), (0, 1, 2)),
    '8': ((1, 2, 4, 5), (0, 3, 6), (0, 3, 6), (1, 2, 4, 5)),
    '9': ((1, 2, 5), (0, 3, 6), (0, 3, 6), (1, 2, 3, 4, 5)),
    '.': ((6,),),
    '-': ((3,), (3,), (3,)),
}


class NumberPainter:
    def __init__(self,
                 color: RGBColor = None,
                 bg_color: RGBColor = None,
                 scale=1,
                 padding_x=1,
                 padding_y=1,
                 interval=1):

        self.color = color or DEFAULT_COLOR
        self.bg_color = bg_color or DEFAULT_BG_COLOR
        self.scale = scale
        self.padding_y = padding_y * scale
        self.padding_x = padding_x * scale
        self.interval = interval * scale
        self.canvas_height = DIGIT_HEIGHT * self.scale + self.padding_y * 2
        self.canvas = []

    @property
    def canvas_width(self) -> int:
        return len(self.canvas) + self.padding_x * 2

    def get_pixels(self) -> Tuple[Tuple[RGBColor]]:
        padding = [(self.bg_color,) * self.canvas_height for _ in range(self.padding_x)]
        return tuple(zip(*padding, *self.canvas, *padding))

    def draw_number(self, number: str):
        for ch in number[:-1]:
            self._draw_char(ch)
            self._draw_interval()

        self._draw_char(number[-1])
        return self

    def _draw_char(self, char: str):
        for column in COLORED_POINTS[char]:
            for _ in range(self.scale):
                self._draw_column(column)

    def _draw_interval(self):
        for _ in range(self.interval):
            self._draw_column([])

    def _draw_column(self, column: Iterable[int]):
        handled_column = [self.bg_color] * self.canvas_height
        for colored_point in column:
            position = colored_point * self.scale + self.padding_y
            handled_column[position: position + self.scale] = [self.color] * self.scale

        self.canvas.append(handled_column)
