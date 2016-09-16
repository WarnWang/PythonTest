#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: refresh_webpage
# Author: Mark Wang
# Date: 6/9/2016

import time

from selenium import webdriver

browser = webdriver.Chrome("/Users/warn/chromedriver")

browser.get('http://www.urbtix.hk')

while True:
    buttons = browser.find_elements_by_id('toMainButton')
    if buttons:
        buttons[0].click()
        time.sleep(1)
    else:
        break
