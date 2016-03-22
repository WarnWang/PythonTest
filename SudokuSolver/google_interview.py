#!/usr/bin/python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: google_interview
# Author: Mark Wang
# Date: 22/3/2016


def calculate_nodes(root):
    k = 0
    temp = root
    while temp is not None:
        k += 1
        temp = temp.left
    if k == 0:
        return 0

    height = k
    temp = root
    while temp is not None:
        k -= 1
        temp = temp.right

    if k == 0:
        return 2 ** height - 1

    left_n = calculate_nodes(root.left)
    full_left_n = 2 ** (height - 1) - 1
    if left_n < full_left_n:
        return left_n + 2 ** (height - 2)

    else:
        return left_n + 1 + calculate_nodes(root.right)


def restore_queue(queue_info):
    people_num = len(queue_info)
    restored_queue = [-1] * people_num
    height_list = []
    for height in queue_info:
        height_list.append(int(height))

    height_list.sort()
    while height_list:
        current_height = height_list.pop()
        index = queue_info[str(current_height)]
        temp = 0
        while temp < index and index < people_num:
            if current_height > restored_queue[temp] >= 0:
                index += 1
            temp += 1

        while restored_queue[index] > 0:
            index += 1
        restored_queue[index] = current_height
    return restored_queue


if __name__ == "__main__":
    queue_info = {'5': 0,
                  '3': 1,
                  "1": 2,
                  "4": 1,
                  "2": 3}

    print restore_queue(queue_info)
