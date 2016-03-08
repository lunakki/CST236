"""
:mod:`source.source1` -- Example source code
============================================

The following example code determines if a set of 3 sides of a triangle
is equilateral, scalene or iscoceles
"""

def get_triangle_type(side_a=0, side_b=0, side_c=0):
    """
    Determine if the given triangle is equilateral, scalene or Isosceles

    :param side_a: line a
    :type side_a: float or int or tuple or list or dict

    :param side_b: line b
    :type side_b: float

    :param side_c: line c
    :type side_c: float

    :return: "equilateral", "isosceles", "scalene" or "invalid"
    :rtype: str
    """

    if isinstance(side_a, (tuple, list)) and len(side_a) == 3:
        side_c = side_a[2]
        side_b = side_a[1]
        side_a = side_a[0]

    # pylint: disable=no-member
    # am making sure it's the correct object type
    if isinstance(side_a, dict) and len(side_a.keys()) == 3:
        values = []
        # pylint: disable=no-member
        # am making sure it's the correct object type
        for value in side_a.values():
            values.append(value)
        side_a = values[0]
        side_b = values[1]
        side_c = values[2]

    if not (isinstance(side_a, (int, float)) and isinstance(side_b, (int, float)) and
            isinstance(side_c, (int, float))):
        return "invalid"

    if side_a <= 0 or side_b <= 0 or side_c <= 0:
        return "invalid"

    if side_a == side_b and side_b == side_c:
        return "equilateral"

    elif side_a == side_b or side_a == side_c or side_b == side_c:
        return "isosceles"
    else:
        return "scalene"

def get_rectangle_type(side_a=0, side_b=0, side_c=0, side_d=0):
    """
    Determine if the given quadrilateral is a square or rectangle

    :param side_a: line a
    :type side_a: float or int or tuple or list (no dict because order matters)

    :param side_b: line b
    :type side_b: float or int

    :param side_c: line c (opposite line a)
    :type side_c: float or int

    :param side_d: line d (opposite line b)
    :type side_d: float or int

    :return: "rectangle", "square", "quadrilateral", "unknown", "invalid"
    :rtype: str
    """
    if isinstance(side_a, (tuple, list)) and len(side_a) == 4:
        side_d = side_a[3]
        side_c = side_a[2]
        side_b = side_a[1]
        side_a = side_a[0]

    if not (isinstance(side_a, (int, float)) and isinstance(side_b, (int, float)) and
            isinstance(side_c, (int, float)) and isinstance(side_d, (int, float))):
        return "invalid"

    if side_a <= 0 or side_b <= 0 or side_c <= 0 or side_d <= 0:
        return "invalid"

    if side_a == side_b and side_b == side_c and side_c == side_d:
        return "square"

    elif side_a == side_c and side_b == side_d:
        return "rectangle"
    else:
        return "unknown"

# pylint: disable=too-many-arguments
# I could redo this so it only takes arrays or something but I want it
# to be the same style as the others, and it *can* take arrays instead
def get_quad_type(side_a=0, side_b=0, side_c=0, side_d=0, corner_a=0, corner_b=0, corner_c=0,
                  corner_d=0):
    """
    Determine if the given quadrilateral is square, rectangle, rhombus, or disconnected

    :param side_a: line a
    :type side_a: float or int or tuple or list (no dict because order matters)

    :param side_b: line b
    :type side_b: float or int

    :param side_c: line c (opposite a)
    :type side_c: float or int

    :param side_d: line d (opposite b)
    :type side_d: float or int

    :param corner_a: corner a in degrees
    :type corner_a: float or int

    :param corner_b: corner b in degrees
    :type corner_b: float or int

    :param corner_c: corner c  in degrees (opposite a)
    :type corner_c: float or int

    :param corner_d: corner d  in degrees (opposite b)
    :type corner_d: float or int

    :return: "rectangle", "square", "rhombus", "disconnected", "unknown", "invalid"
    :rtype: str
    """

    if isinstance(side_a, (tuple, list)) and len(side_a) == 8:
        corner_d = side_a[7]
        corner_c = side_a[6]
        corner_b = side_a[5]
        corner_a = side_a[4]
        side_d = side_a[3]
        side_c = side_a[2]
        side_b = side_a[1]
        side_a = side_a[0]

    shape_type = ""
    # Check for invalid parameters
    if not (isinstance(side_a, (int, float)) and isinstance(side_b, (int, float)) and
            isinstance(side_c, (int, float)) and isinstance(side_d, (int, float))):
        shape_type = "invalid"

    if not (isinstance(corner_a, (int, float)) and isinstance(corner_b, (int, float)) and
            isinstance(corner_c, (int, float)) and isinstance(corner_d, (int, float))):
        shape_type = "invalid"

    if side_a <= 0 or side_b <= 0 or side_c <= 0 or side_d <= 0:
        shape_type = "invalid"
    if corner_a <= 0 or corner_b <= 0 or corner_c <= 0 or corner_d <= 0:
        shape_type = "invalid"

    if shape_type == "invalid":
        return shape_type

    # Check what type the shape is
    # pylint: disable=too-many-boolean-expressions
    # Only way around it is to nest them and that'd be worse
    if (side_a == side_b and side_b == side_c and side_c == side_d and
            corner_a == 90 and corner_b == 90 and corner_c == 90 and corner_d == 90):
        shape_type = "square"
    # pylint: disable=too-many-boolean-expressions
    # Only way around it is to nest them and that'd be worse
    elif side_a == side_c and side_b == side_d and corner_a == 90 and corner_b == 90 and \
            corner_c == 90 and corner_d == 90:
        shape_type = "rectangle"
    elif side_a == side_c and side_b == side_d and corner_a == corner_c and \
            corner_b == corner_d and corner_a + corner_b == 180:
        shape_type = "rhombus"
    elif corner_a + corner_b + corner_c + corner_d != 360:
        shape_type = "disconnected"
    else:
        shape_type = "unknown"

    return shape_type

