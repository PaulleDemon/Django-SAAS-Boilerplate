import math
from decimal import Decimal

#NOTE: never use floating points to represent money
def dollar_to_cents(dollar: Decimal):

    integer = int(dollar)
    decimal = int((dollar % 1)*100)

    return (integer * 100) + decimal


def cents_to_dollar(cent: int):
    
    return cent/100