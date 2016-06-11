#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: layton_148
# Author: Mark Wang
# Date: 11/6/2016


def find_solution():
    possible_number = range(1, 9)
    current_list = [0] * 8
    find_all_solution(current_list, possible_number, 0)


def find_all_solution(current_list, possible_number, index):
    if index == 8:
        if calculated(current_list):
            print current_list
        return
    for num in possible_number:
        current_list[index] = num
        new_possible = possible_number[:]
        new_possible.remove(num)
        find_all_solution(current_list, new_possible, index + 1)


def calculated(current_list):
    num1 = 0
    for i in range(3):
        num1 = num1 * 10 + current_list[i]

    num2 = current_list[3]

    num3 = 0
    for i in range(4, 8):
        num3 = num3 * 10 + current_list[i]

    return num1 * num2 == num3


if __name__ == "__main__":
    find_solution()
