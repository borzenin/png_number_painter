from unittest import TestCase

from image import ImageShape, ImageSize, RGBColor
from painter import NumberPainter


class TestPNGCreation(TestCase):
    def test_create_data_chunk(self):
        pixels = [[RGBColor(1, 2, 3)]]
        result = ImageShape(ImageSize(3, 4), scale=2)._create_data_chunk(pixels,
                                                                         filter_type=1)
        expected = b'\x00\x00\x00\x0fIDATx\x9ccddb\x06!\x08\x05\x00\x00\xc3\x00\x1b\xa9\x15\x94S'
        self.assertEqual(result, expected)


class TestNumberPainter(TestCase):
    def test_draw_column(self):
        number_painter = NumberPainter()
        number_painter.canvas_height = 10
        number_painter.scale = 2
        number_painter.bg_color = RGBColor(0, 0, 0)
        number_painter.color = RGBColor(1, 1, 1)
        number_painter.padding_y = 1 * number_painter.scale

        column = [1, 2]
        number_painter._draw_column(column)
        last_column = number_painter.canvas[-1]
        expected_last_column = [RGBColor(red=0, green=0, blue=0),
                                RGBColor(red=0, green=0, blue=0),
                                RGBColor(red=0, green=0, blue=0),
                                RGBColor(red=0, green=0, blue=0),
                                RGBColor(red=1, green=1, blue=1),
                                RGBColor(red=1, green=1, blue=1),
                                RGBColor(red=1, green=1, blue=1),
                                RGBColor(red=1, green=1, blue=1),
                                RGBColor(red=0, green=0, blue=0),
                                RGBColor(red=0, green=0, blue=0)]

        self.assertEqual(last_column, expected_last_column)

    def test_canvas_width(self):
        number_painter = NumberPainter()
        number_painter.padding_x = 2
        number_painter._draw_column([])
        self.assertEqual(number_painter.canvas_width, 5)
