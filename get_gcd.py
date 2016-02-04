#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: get_gcd
# Author: warn
# Date: 3/2/2016 19:42

import random


def get_gcd(a, b):
    if not isinstance(a, int) or not isinstance(b, int):
        return 0

    res = 1
    n = a
    m = b
    while m != n:
        if m % 2 == 0 and n % 2 == 0:
            res *= 2
            m /= 2
            n /= 2

        elif m % 2 == 0:
            m /= 2

        elif n % 2 == 0:
            n /= 2

        elif m > n:
            m -= n

        else:
            n -= m

    return m * res


def get_prime(n=100):
    result = [2]
    for i in xrange(3, n):
        for j in result:
            if i % j == 0:
                break
        else:
            result.append(i)

    return result


def get_big_number(max_value=2147483647):
    prime_list = get_prime(30);
    i = 1
    j = 1
    a = set()
    temp = 0
    while i < max_value / 2:
        j = i
        if temp:
            a.add(temp)
        temp = prime_list[random.randint(0, len(prime_list) - 1)]
        i *= temp

    k = 1
    print a
    for m in a:
        k *= m

    return j, k


if __name__ == "__main__":
    # print get_gcd(198, 132)
    print get_big_number()
