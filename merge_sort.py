#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: merge_sort
# Author: warn
# Date: 29/2/2016 17:37


def merge_sort(s):
    n = len(s)
    if n <= 1:
        return s
    else:
        s1 = merge_sort(s[:n / 2])
        s2 = merge_sort(s[n / 2:])
        result = []
        while len(s1) != 0 and len(s2) != 0:
            if s1[0] < s2[0]:
                result.append(s1[0])
                s1.pop(0)
            else:
                result.append(s2[0])
                s2.pop(0)

        result.extend(s1)
        result.extend(s2)
        return result


if __name__ == "__main__":
    a = [6, 2, 4, 3, 1, -22]
    print merge_sort(a)
