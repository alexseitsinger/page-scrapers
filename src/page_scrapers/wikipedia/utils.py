import sys

def int_to_roman(num):
    """
    https://stackoverflow.com/questions/42875103/integer-to-roman-number
    https://stackoverflow.com/questions/33486183/convert-from-numbers-to-roman-notation
    """
    conv = (
        ("M", 1000),
        ("CM", 900),
        ("D", 500),
        ("CD", 400),
        ("C", 100),
        ("XC", 90),
        ("L", 50),
        ("XL", 40),
        ("X", 10),
        ("IX", 9),
        ("V", 5),
        ("IV", 4),
        ("I", 1)
    )
    roman = ""
    i = 0
    while num > 0:
        while conv[i][1] > num:
            i += 1
        roman += conv[i][0]
        num -= conv[i][1]
    return roman


def roman_to_int(roman):
    """
    https://gist.github.com/kristopherjohnson/f4eca9018c5085fc736b2f29a202b8f8
    """
    vals = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }
    total = 0
    lastValue = sys.maxsize
    for char in list(roman):
        value = vals[char.upper()]
        if value > lastValue:
            total += value - 2 * lastValue
        else:
            total += value
        lastValue = value
    return total
