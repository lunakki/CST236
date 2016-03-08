"""
Test for quadrilaterals in source.shape_checker
"""
from unittest import TestCase
from source.shape_checker import get_quad_type
from tests.plugins.ReqTracer import requirements


# pylint: disable=too-many-public-methods
# I already separated them as much as I can
class TestQuadrilateralType(TestCase):
    """quadrilateral tests"""
    @requirements(['#0003', '#0004', '#0005'])
    def test_square_all_int(self):
        """Quad test"""
        result = get_quad_type(1, 1, 1, 1, 90, 90, 90, 90)
        self.assertEqual(result, 'square')

    @requirements(['#0003', '#0004', '#0005'])
    def test_rect_all_int(self):
        """Quad test"""
        result = get_quad_type(1, 2, 1, 2, 90, 90, 90, 90)
        self.assertEqual(result, 'rectangle')

    @requirements(['#0003', '#0004', '#0005'])
    def test_rhombus_all_int(self):
        """Quad test"""
        result = get_quad_type(1, 2, 1, 2, 30, 150, 30, 150)
        self.assertEqual(result, 'rhombus')

    @requirements(['#0003', '#0004', '#0005'])
    def test_unknown_all_int_0(self):
        """Quad test"""
        result = get_quad_type(1, 2, 3, 4, 90, 90, 90, 90)
        self.assertEqual(result, 'unknown')

    @requirements(['#0003', '#0004', '#0005'])
    def test_unknown_all_int_1(self):
        """Quad test"""
        result = get_quad_type(1, 1, 1, 1, 30, 150, 140, 40)
        self.assertEqual(result, 'unknown')

    @requirements(['#0003', '#0004', '#0005'])
    def test_disconnected_all_int(self):
        """Quad test"""
        result = get_quad_type(1, 1, 1, 1, 10, 10, 10, 10)
        self.assertEqual(result, 'disconnected')

    @requirements(['#0003', '#0004', '#0005'])
    def test_square_all_float(self):
        """Quad test"""
        result = get_quad_type(1.1, 1.1, 1.1, 1.1, 90.0, 90.0, 90.0, 90.0)
        self.assertEqual(result, 'square')

    @requirements(['#0003', '#0004', '#0005'])
    def test_rect_all_float(self):
        """Quad test"""
        result = get_quad_type(1.1, 1.2, 1.1, 1.2, 90.0, 90.0, 90.0, 90.0)
        self.assertEqual(result, 'rectangle')

    @requirements(['#0003', '#0004', '#0005'])
    def test_square_int_and_float(self):
        """Quad test"""
        result = get_quad_type(1, 1.0, 1.0, 1, 90, 90.0, 90, 90.0)
        self.assertEqual(result, 'square')

    def test_square_tuple(self):
        """Quad test"""
        result = get_quad_type((1, 1, 1, 1, 90, 90, 90, 90))
        self.assertEqual(result, 'square')

    def test_rectangle_list(self):
        """Quad test"""
        result = get_quad_type([1, 1.1, 1, 1.1, 90, 90.0, 90, 90.0])
        self.assertEqual(result, 'rectangle')

    def test_dict(self):
        """Quad test"""
        result = get_quad_type({'side0': 1, 'side1': 1, 'side2': 1, 'side3': 1,
                                'corner0': 90, 'corner1': 90, 'corner2': 90, 'corner3': 90})
        self.assertEqual(result, 'invalid')

    def test_square_string_first(self):
        """Quad test"""
        result = get_quad_type("1", 1, 1, 1, 90, 90, 90, 90)
        self.assertEqual(result, 'invalid')

    def test_square_string_second(self):
        """Quad test"""
        result = get_quad_type(1, "1", 1, 1, 90, 90, 90, 90)
        self.assertEqual(result, 'invalid')

    def test_square_string_third(self):
        """Quad test"""
        result = get_quad_type(1, 1, "1", 1, 90, 90, 90, 90)
        self.assertEqual(result, 'invalid')

    def test_square_string_fourth(self):
        """Quad test"""
        result = get_quad_type(1, 1, 1, "1", 90, 90, 90, 90)
        self.assertEqual(result, 'invalid')

    def test_square_string_fifth(self):
        """Quad test"""
        result = get_quad_type(1, 1, 1, 1, "90", 90, 90, 90)
        self.assertEqual(result, 'invalid')

    def test_square_string_sixth(self):
        """Quad test"""
        result = get_quad_type(1, 1, 1, 1, 90, "90", 90, 90)
        self.assertEqual(result, 'invalid')

    def test_square_string_seventh(self):
        """Quad test"""
        result = get_quad_type(1, 1, 1, 1, 90, 90, "90", 90)
        self.assertEqual(result, 'invalid')

    def test_square_string_eighth(self):
        """Quad test"""
        result = get_quad_type(1, 1, 1, "1", 90, 90, 90, "90")
        self.assertEqual(result, 'invalid')

    @requirements(['#0003'])
    def test_tuple_too_long(self):
        """Quad test"""
        result = get_quad_type((1, 1, 1, 1, 1, 1, 1, 1, 1))
        self.assertEqual(result, 'invalid')

    @requirements(['#0003'])
    def test_list_too_long(self):
        """Quad test"""
        result = get_quad_type([1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(result, 'invalid')

    @requirements(['#0003'])
    def test_tuple_too_short(self):
        """Quad test"""
        result = get_quad_type((1, 1, 1, 1, 90, 90, 90))
        self.assertEqual(result, 'invalid')

    @requirements(['#0003'])
    def test_list_too_short(self):
        """Quad test"""
        result = get_quad_type([1, 1, 1, 1, 90, 90, 90])
        self.assertEqual(result, 'invalid')

    def test_large_num(self):
        """Technically this should return quadrilateral but oh well"""
        result = get_quad_type(100000000000, 100000000000, 100000000000)
        self.assertEqual(result, 'invalid')

    def test_negative(self):
        """Quad test"""
        result = get_quad_type(-1, -1, -1)
        self.assertEqual(result, 'invalid')
