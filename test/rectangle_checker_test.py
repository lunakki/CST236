"""
Test for triangles in source.shape_checker
"""
from unittest import TestCase
from source.shape_checker import get_rectangle_type


class TestRectangleType(TestCase):
    """Rectangle tests"""
    def test_square_all_int(self):
        """Rectangle test"""
        result = get_rectangle_type(1, 1, 1, 1)
        self.assertEqual(result, 'square')

    def test_rect_all_int(self):
        """Rectangle test"""
        result = get_rectangle_type(1, 2, 1, 2)
        self.assertEqual(result, 'rectangle')

    def test_unknown_all_int(self):
        """Rectangle test"""
        result = get_rectangle_type(1, 2, 3, 4)
        self.assertEqual(result, 'unknown')

    def test_square_all_float(self):
        """Rectangle test"""
        result = get_rectangle_type(1.1, 1.1, 1.1, 1.1)
        self.assertEqual(result, 'square')

    def test_rect_all_float(self):
        """Rectangle test"""
        result = get_rectangle_type(1.1, 1.2, 1.1, 1.2)
        self.assertEqual(result, 'rectangle')

    def test_square_int_and_float(self):
        """Rectangle test"""
        result = get_rectangle_type(1, 1.0, 1.0, 1)
        self.assertEqual(result, 'square')

    def test_square_tuple(self):
        """Rectangle test"""
        result = get_rectangle_type((1, 1, 1, 1))
        self.assertEqual(result, 'square')

    def test_square_list(self):
        """Rectangle test"""
        result = get_rectangle_type([1, 1, 1, 1])
        self.assertEqual(result, 'square')

    def test_dict(self):
        """Rectangle test"""
        result = get_rectangle_type({'side0': 1, 'side1': 1, 'side2': 1, 'side3': 1})
        self.assertEqual(result, 'invalid')

    def test_square_string_first(self):
        """Rectangle test"""
        result = get_rectangle_type("1", 1, 1, 1)
        self.assertEqual(result, 'invalid')

    def test_square_string_second(self):
        """Rectangle test"""
        result = get_rectangle_type(1, "1", 1, 1)
        self.assertEqual(result, 'invalid')

    def test_square_string_third(self):
        """Rectangle test"""
        result = get_rectangle_type(1, 1, "1", 1)
        self.assertEqual(result, 'invalid')

    def test_square_string_fourth(self):
        """Rectangle test"""
        result = get_rectangle_type(1, 1, 1, "1")
        self.assertEqual(result, 'invalid')

    def test_tuple_too_long(self):
        """Rectangle test"""
        result = get_rectangle_type((1, 1, 1, 1, 1))
        self.assertEqual(result, 'invalid')

    def test_list_too_long(self):
        """Rectangle test"""
        result = get_rectangle_type([1, 1, 1, 1, 1])
        self.assertEqual(result, 'invalid')

    def test_tuple_too_short(self):
        """Rectangle test"""
        result = get_rectangle_type((1, 1, 1))
        self.assertEqual(result, 'invalid')

    def test_list_too_short(self):
        """Rectangle test"""
        result = get_rectangle_type([1, 1, 1])
        self.assertEqual(result, 'invalid')

    def test_large_num(self):
        """Rectangle test"""
        result = get_rectangle_type(100000000000, 100000000000, 100000000000)
        self.assertEqual(result, 'invalid')

    def test_negatives(self):
        """Rectangle test"""
        result = get_rectangle_type(-1, -1, -1, -1)
        self.assertEqual(result, 'invalid')
