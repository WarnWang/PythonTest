import math


def get_yield_from_discount_rate(discount_rate, days_to_maturity, act_days=365):
    return discount_rate / (1 - discount_rate * float(days_to_maturity) / act_days)


def get_discount_price(discount_rate, days_to_maturity, act_days=365):
    return 1 - discount_rate * float(days_to_maturity) / act_days


if __name__ == "__main__":
    discount_rate = 0.02
    days_to_maturity = 50
    print get_yield_from_discount_rate(discount_rate, days_to_maturity)
    print 1000000 * get_discount_price(discount_rate, days_to_maturity, 360)
