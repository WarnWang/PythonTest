#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: QuickSort
# Author: warn
# Date: 25/1/2016 15:57


def quick_sort(list_to_sort):
    if len(list_to_sort) < 2:
        return list_to_sort
    n = list_to_sort[len(list_to_sort) / 2]
    first_part = []
    second_part = []
    middle_part = []
    for i in list_to_sort:
        if i == n:
            middle_part.append(i)
        elif i > n:
            second_part.append(i)
        else:
            first_part.append(i)

    second_part = quick_sort(second_part)
    first_part = quick_sort(first_part)
    result = first_part + middle_part + second_part
    return result


if __name__ == "__main__":
    a = [5, 3, 2, 1, 4, 5, 2, 3, 4, 6, 7, -1, 23, 5, 2, 7]
    print quick_sort(a)
