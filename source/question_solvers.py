"""Helper functions for questions in main.py"""
import time
import decimal
import datetime
import random
import math


def get_fibonacci_number(nth_value):
    """Return the nth value in the Fibonacci sequence (starts with 0,1)"""
    first = 0
    second = 1
    temp = 0
    current = 2

    if nth_value == 1:
        return "0"

    while current < nth_value:
        temp = second
        second = first + second
        first = temp
        current = current + 1

    return str(second)


def get_date_time():
    """Return the current date and time"""
    return time.strftime("%d/%m/%Y %H:%M")


def get_pi_digit(nth_value):
    """Return nth digit of pi after the decimal point up to 1,000"""
    pi_digits = ("14159265358979323846264338327950288419716939937510582097494459230" +
                 "7816406286208998628034825342117067982148086513282306647093844609550" +
                 "5822317253594081284811174502841027019385211055596446229489549303819" +
                 "64428810975665933446128475648233786783165271201909145648566923460348" +
                 "61045432664821339360726024914127372458700660631558817488152092096282" +
                 "9254091715364367892590360011330530548820466521384146951941511609433057" +
                 "270365759591953092186117381932611793105118548074462379962749567351885752" +
                 "724891227938183011949129833673362440656643086021394946395224737190702179860" +
                 "943702770539217176293176752384674818467669405132000568127145263560827785771" +
                 "342757789609173637178721468440901224953430146549585371050792279689258923542" +
                 "019956112129021960864034418159813629774771309960518707211349999998372978049" +
                 "951059731732816096318595024459455346908302642522308253344685035261931188171" +
                 "010003137838752886587533208381420617177669147303598253490428755468731159562" +
                 "8638823537875937519577818577805321712268066130019278766111959092164201989")
    return pi_digits[int(nth_value) - 1]


# conversion functions
# All return a string with the value to two decimal places followed by the unit
def convert_inches_to_feet(num_to_convert):
    """Convert inches to feet"""
    return c(num_to_convert / 12) + " feet"


def convert_feet_to_inches(num_to_convert):
    """Convert feet to inches"""
    return c(num_to_convert * 12) + " inches"


def convert_gallons_to_liters(num_to_convert):
    """Convert gallons to liters"""
    return c(num_to_convert * 3.785) + " liters"


def convert_liters_to_gallons(num_to_convert):
    """Convert liters to gallons"""
    return c((num_to_convert * 0.264)) + " gallons"


def convert_cups_to_teaspons(num_to_convert):
    """Convert cups to teaspoons"""
    return c(num_to_convert * 48) + " teaspoons"


def convert_teaspoons_to_cups(num_to_convert):
    """Convert teaspoons to cups"""
    return c((num_to_convert * 0.0208)) + " cups"


def convert_miles_to_km(num_to_convert):
    """Convert miles to km"""
    return c(num_to_convert * 1.60934) + " km"


def convert_km_to_miles(num_to_convert):
    """Convert km to miles"""
    return c((num_to_convert * 0.621)) + " miles"


def convert_acres_to_sqfeet(num_to_convert):
    """Convert acres to sqfeet"""
    return c(num_to_convert * 43560) + " square feet"


def convert_sqfeet_to_acres(num_to_convert):
    """Convert sqfeet to acres"""
    return c((num_to_convert / 43560)) + " acres"


# pylint: disable=too-many-branches
# there's probably an easier way but this is still easy to read
def get_rgb_hex(color):
    """Return the RGB hex value for a given color name"""
    hex_code = "unknown"
    if color == "red":
        hex_code = "#FF0000"
    elif color == "blue":
        hex_code = "#0000FF"
    elif color == "green":
        hex_code = "#00FF00"
    elif color == "darkred":
        hex_code = "#990000"
    elif color == "darkblue":
        hex_code = "#000088"
    elif color == "darkgreen":
        hex_code = "#008800"
    elif color == "yellow":
        hex_code = "#FFFF00"
    elif color == "pink":
        hex_code = "#FF0088"
    elif color == "purple":
        hex_code = "#880088"
    elif color == "cyan":
        hex_code = "#00FFFF"
    elif color == "orange":
        hex_code = "#FF8800"
    elif color == "white":
        hex_code = "#FFFFFF"
    elif color == "black":
        hex_code = "#000000"
    elif color == "lightgrey":
        hex_code = "#DDDDDD"
    elif color == "grey":
        hex_code = "#888888"
    return hex_code


def get_is_divisible(num1, num2):
    """Return "yes" if the first number is divisible by the second; no otherwise"""
    if num1 % num2 == 0:
        return "Yes"
    return "No"


def get_days_until_date(month, day):
    """Return the number of dates between now and the given date"""
    today = datetime.date.today()
    until_date = datetime.date(int(today.strftime("%Y")), int(month), int(day))

    if until_date - today < datetime.timedelta(days=0):
        until_date = datetime.date(int(today.strftime("%Y")) + 1, int(month), int(day))

    return str((until_date - today).days)


def get_lotto_numbers(limit=99):
    """Return five random lottery numbers with values up to the given limit"""
    count = 1
    nums = []
    while count < 6:
        rand = random.randrange(1, limit)
        if rand not in nums:
            nums.append(rand)
            count += 1

    return str(nums[0]) + " " + str(nums[1]) + " " + str(nums[2]) + " " +\
           str(nums[3]) + " " + str(nums[4])


def get_exponent_result(base, exponent):
    """Return a number raised to another number"""
    return str(int(math.pow(base, exponent)))


def get_age(month, day, year):
    """Return the age of the person born on the given date"""
    today = datetime.date.today()
    birthday = datetime.date(int(year), int(month), int(day))
    return str(int((today - birthday).days/365))


# pylint: disable=invalid-name
# this is purposely short so it can be used elsewhere without causing disruption
def c(num):
    """Convert numbers to a string with two decimal places"""
    return str(decimal.Decimal(num).quantize(decimal.Decimal('0.01')))
