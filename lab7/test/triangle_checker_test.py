"""
Test for triangles in source.shape_checker
"""
from unittest import TestCase
from source.shape_checker import get_triangle_type
from tests.plugins.ReqTracer import requirements


# pylint: disable=too-many-public-methods
# I already separated them as much as I can; I'm only 1 over now
class TestTriangleType(TestCase):
    """Triangle tests"""

    @requirements(['#0001', '#0002'])
    def test_equilateral_all_int(self):
        """Triangle test"""
        result = get_triangle_type(1, 1, 1)
        self.assertEqual(result, 'equilateral')

    @requirements(['#0001', '#0002'])
    def test_scalene_all_int(self):
        """Triangle test"""
        result = get_triangle_type(1, 2, 3)
        self.assertEqual(result, 'scalene')

    @requirements(['#0001', '#0002'])
    def test_isosceles_all_int_0(self):
        """Triangle test"""
        result = get_triangle_type(1, 1, 3)
        self.assertEqual(result, 'isosceles')

    @requirements(['#0001', '#0002'])
    def test_isosceles_all_int_1(self):
        """Triangle test"""
        result = get_triangle_type(1, 3, 1)
        self.assertEqual(result, 'isosceles')

    @requirements(['#0001', '#0002'])
    def test_isosceles_all_int_2(self):
        """Triangle test"""
        result = get_triangle_type(3, 1, 1)
        self.assertEqual(result, 'isosceles')

    def test_first_string(self):
        """Triangle test"""
        result = get_triangle_type("1", 1, 1)
        self.assertEqual(result, 'invalid')

    def test_second_string(self):
        """Triangle test"""
        result = get_triangle_type(1, "1", 1)
        self.assertEqual(result, 'invalid')

    def test_third_string(self):
        """Triangle test"""
        result = get_triangle_type(1, 1, "1")
        self.assertEqual(result, 'invalid')

    @requirements(['#0001', '#0002'])
    def test_equilateral_all_float(self):
        """Triangle test"""
        result = get_triangle_type(1.1, 1.1, 1.1)
        self.assertEqual(result, 'equilateral')

    @requirements(['#0001', '#0002'])
    def test_equilateral_float_and_int(self):
        """Triangle test"""
        result = get_triangle_type(1, 1.0, 1)
        self.assertEqual(result, 'equilateral')

    def test_equilateral_tuple(self):
        """Triangle test"""
        result = get_triangle_type((1, 1, 1))
        self.assertEqual(result, 'equilateral')

    def test_equilateral_list(self):
        """Triangle test"""
        result = get_triangle_type([1, 1, 1])
        self.assertEqual(result, 'equilateral')

    def test_equilateral_dict(self):
        """Triangle test"""
        result = get_triangle_type({'side0': 1, 'side1': 1, 'side2': 1})
        self.assertEqual(result, 'equilateral')

    def test_tuple_too_long(self):
        """Triangle test"""
        result = get_triangle_type((1, 1, 1, 1))
        self.assertEqual(result, 'invalid')

    def test_list_too_long(self):
        """Triangle test"""
        result = get_triangle_type([1, 1, 1, 1])
        self.assertEqual(result, 'invalid')

    def test_dict_too_long(self):
        """Triangle test"""
        result = get_triangle_type({'side0': 1, 'side1': 1, 'side2': 1, 'side3': 1})
        self.assertEqual(result, 'invalid')

    def test_tuple_too_short(self):
        """Triangle test"""
        result = get_triangle_type((1, 1))
        self.assertEqual(result, 'invalid')

    def test_list_too_short(self):
        """Triangle test"""
        result = get_triangle_type([1, 1])
        self.assertEqual(result, 'invalid')

    def test_dict_too_short(self):
        """Triangle test"""
        result = get_triangle_type({'side0': 1, 'side1': 1})
        self.assertEqual(result, 'invalid')

    def test_equilateral_large_num(self):
        """Triangle test"""
        result = get_triangle_type(1000000000000, 1000000000000, 1000000000000)
        self.assertEqual(result, 'invalid')

    def test_negative_num(self):
        """Triangle test"""
        result = get_triangle_type(-1, -1, -1)
        self.assertEqual(result, 'invalid')
