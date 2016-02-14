#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: heap_sort
# Author: warn
# Date: 14/2/2016 16:34


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


if __name__ == "__main__":
    print heap_sort([4, 23, 4, 51, 23, 5, 1])
