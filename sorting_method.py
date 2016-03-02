#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: sorting_method
# Author: warn
# Date: 1/3/2016 17:19

import time
import random


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


def heap_sort(s):
    n = len(s)
    for i in range(1, n):
        index = i
        while index:
            parent_index = (index - 1) / 2;
            if s[parent_index] < s[index]:
                s[parent_index], s[index] = s[index], s[parent_index]
                index = parent_index
            else:
                break

    for i in range(n):
        s[0], s[n - i - 1] = s[n - i - 1], s[0]
        index = 0
        while index < n - i - 1:
            left_son_index = 2 * index + 1
            right_son_index = 2 * index + 2
            if left_son_index > n - i - 2:
                break
            elif right_son_index > n - i - 2:
                son_index = left_son_index
            else:
                son_index = left_son_index if s[left_son_index] > s[right_son_index] else right_son_index

            if s[index] >= s[son_index]:
                break
            else:
                s[index], s[son_index] = s[son_index], s[index]
                index = son_index

    return s


def bubble_sort(s):
    min_value = max_value = None
    for i in s:
        if min_value is None or i < min_value:
            min_value = i

        if max_value is None or i > max_value:
            max_value = i

    bubble = [0] * (max_value - min_value + 1)
    for i in s:
        bubble[i - min_value] += 1

    s = []

    for i in range(len(bubble)):
        s.extend([i + min_value] * bubble[i])

    return s


def selection_sort(s):
    for i in range(len(s) - 1):
        for j in range(i + 1, len(s)):
            if s[j] < s[i]:
                s[j], s[i] = s[i], s[j]

    return s


def quick_select(s, k):
    if 1 == len(s):
        return s[0]
    x = s[0]
    l = []
    g = []
    e = []
    max_value = x
    for i in s:
        if i < x:
            l.append(i)
        elif i == x:
            e.append(i)
        else:
            g.append(i)

        if i > max_value:
            max_value = i

    if k > len(s):
        return max_value
    if k <= len(l):
        return quick_select(l, k)
    elif k <= len(l) + len(e):
        return x
    else:
        return quick_select(g, k - len(l) - len(e))


if __name__ == "__main__":
    s = []
    for i in range(120):
        s.append(random.randint(0, 5039))

    start_time = time.time()
    bubble_sort(s[:])
    print time.time() - start_time

    start_time = time.time()
    quick_sort(s[:])
    print time.time() - start_time

    start_time = time.time()
    heap_sort(s[:])
    print time.time() - start_time

    start_time = time.time()
    merge_sort(s[:])
    print time.time() - start_time

    start_time = time.time()
    b = selection_sort(s[:])
    print time.time() - start_time

    print s
    print quick_select(s, 55)
    print b
