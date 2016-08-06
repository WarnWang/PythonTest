#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: get_hsi_list
# Author: Mark Wang
# Date: 21/7/2016


from BeautifulSoup import BeautifulSoup

soup = None

with open('hsi_stock_list.htm') as f:
    soup = BeautifulSoup(f.read())

if soup is None:
    print 'read file failed'

stock_table = soup.find(id='DivContentLeft')
stock_list = stock_table.findAll('div')[1].findAll('table')[2].findAll('tr')

hsi_stock_list = map(lambda x: '{}.HK'.format(x.find('td').text[1:]), stock_list[1:])

print hsi_stock_list
