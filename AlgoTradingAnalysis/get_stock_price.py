#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: get_stock_price
# Author: warn
# Date: 23/12/2015 20:00

import urllib
import urllib2

DATA_URL = "http://real-chart.finance.yahoo.com/table.csv"


def get(url, data=None):
    if data is not None:
        url_values = urllib.urlencode(data)
        url = "%s?%s" % (url, url_values)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return response.read()


def get_price_data(code, start_date="2014-08-28", end_date="2015-01-01"):
    time_info = [("s", code)]
    data = start_date.split('-')
    time_info.append(("a", "%02d" % (int(data[1]) - 1)))
    time_info.append(("b", data[2]))
    time_info.append(("c", data[0]))

    data = end_date.split('-')
    time_info.append(("d", "%02d" % (int(data[1]) - 1)))
    time_info.append(("e", data[2]))
    time_info.append(("f", data[0]))

    time_info.append(("g", "d"))
    time_info.append(("ignore", ".csv"))

    f = open(r"./data/%s.csv" % code, "w")
    f.write(get(DATA_URL, time_info))
    f.close()


def get_given_stock_price():
    stock_file = open('stock_list')
    for i in stock_file:
        get_price_data("%s.HK" % i.strip('\n'), start_date="2015-01-01", end_date="2015-03-31")
    stock_file.close()


def get_a_stock_list(n=None):
    stock_file = open('stock_list')
    if n is None:
        n = 10
    for i, j in enumerate(stock_file):
        if i >= n:
            break
        else:
            print "DataSource_%s=SEHK" % (i + 1)
            print "ProductCode_%s=0%s" % (i + 1, j)
    stock_file.close()


if __name__ == "__main__":
    # get_a_stock_list(16)
    # get_given_stock_price(
    get_price_data("0066.HK")
