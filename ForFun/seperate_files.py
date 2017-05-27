#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: seperate_files
# @Date: 27/5/2017
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import shutil

root_path = '/Users/warn/Pictures/本子/人类恶/3_books'

dir_list = []
for i in range(1, 5):
    cur_path = os.path.join(root_path, str(i))
    if not os.path.isdir(i):
        os.makedirs(cur_path)

    dir_list.append(cur_path)

file_list = os.listdir(root_path)

for f in file_list:
    if not f.endswith('.jpg'):
        continue
    if '_1' in f:
        save_path = dir_list[0]
    elif len(f) == 7:
        save_path = dir_list[1]
    elif len(f) < 7:
        save_path = dir_list[2]
    else:
        save_path = dir_list[3]

    shutil.move(os.path.join(root_path, f), os.path.join(save_path, f))
