#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: generate_command
# Author: Mark Wang
# Date: 13/8/2016

import re

with open('error_packages') as f:
    s = f.read()
    package_name = re.findall(r"package '([\w\W]+?)' missing;", s)

print package_name
commands = map(lambda x: "sudo apt-get install --reinstall {}\n".format(x), package_name)
with open('reinstall_command.txt', 'w') as f:
    f.writelines(commands)
