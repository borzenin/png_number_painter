from unittest import TestCase

from image import ImageShape, ImageSize, RGBColor


class TestPNGCreation(TestCase):
    def test_create_data_chunk(self):
        pixels = [[RGBColor(1, 2, 3)]]
        result = ImageShape(ImageSize(3, 4), scale=2)._create_data_chunk(pixels,
                                                                         filter_type=1)
        expected = b'\x00\x00\x00\x0fIDATx\x9ccddb\x06!\x08\x05\x00\x00\xc3\x00\x1b\xa9\x15\x94S'
        self.assertEqual(result, expected)
