#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: get_stock_price
# Author: warn
# Date: 23/12/2015 20:00

import urllib
import urllib2
import pprint
import pickle
import re
from HTMLParser import HTMLParser

import pandas as pd
import BeautifulSoup
from pandas.tseries.offsets import BDay

DATA_URL = "http://real-chart.finance.yahoo.com/table.csv"
SINA_DATA_URL = "http://stock.finance.sina.com.cn/hkstock/history"


def get(url, data=None):
    if data is not None:
        url_values = urllib.urlencode(data)
        url = "%s?%s" % (url, url_values)

    # print url
    # return '1\n1'
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
    except Exception, err:
        print url
        raise Exception(err)
    return response.read()


def post(url, data):
    data = urllib.urlencode(data)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req, data)
    content = response.read()
    return content


def get_price_data(code, start_date="2014-08-29", end_date="2015-01-01"):
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


def get_close_price(code, end_date="2015-01-01", days=90):
    end_date_info = [int(i) for i in end_date.split('-')]
    end_date = pd.datetime(end_date_info[0], end_date_info[1], end_date_info[2])
    start_date = end_date - BDay(days)
    time_info = [("s", code),
                 ("a", "%02d" % (start_date.month - 1)),
                 ("b", str(start_date.day)),
                 ("c", str(start_date.year)),
                 ("d", "%02d" % (end_date.month - 1)),
                 ("e", str(end_date.day)),
                 ("f", str(end_date.year)),
                 ("g", "d"),
                 ("ignore", ".csv")]

    price_info = get(DATA_URL, time_info).split('\n')[1:-1]
    price_list = [float(i.split(',')[4]) for i in price_info]
    price_list = list(reversed(price_list))
    return price_list


def get_close_price_from_sina(code, year=2014, season=4):
    url = "%s/0%s.html" % (SINA_DATA_URL, code)
    data = {"year": year,
            "season": season}
    result = post(url, data)
    close_price_list = get_historical_close_price_from_sina_history(result)
    high_price_list = get_historical_high_price_from_sina_history(result)
    low_price_list = get_historical_low_price_from_sina_history(result)
    return {"close_price": close_price_list,
            "high_price": high_price_list,
            "low_price": low_price_list}


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


def prepare_stock_info():
    stock_info = {}
    stock_file = open('stock_list')
    for i in stock_file:
        # print i
        stock_info['0%s' % i.strip('\n')] = get_close_price_from_sina(i.strip('\n'), year=2015, season=1)
        print "get price of %s ok" % i.strip('\n')
    stock_file.close()
    return stock_info


def get_historical_close_price_from_sina_history(html_info):
    soup = BeautifulSoup.BeautifulSoup(html_info)
    data = soup.findAll('tr')[1:]
    price_list = [float(i.findAll('td')[1].text) for i in data]
    return list(reversed(price_list))


def get_historical_high_price_from_sina_history(html_info):
    soup = BeautifulSoup.BeautifulSoup(html_info)
    data = soup.findAll('tr')[1:]
    price_list = [float(i.findAll('td')[7].text) for i in data]
    return list(reversed(price_list))


def get_historical_low_price_from_sina_history(html_info):
    soup = BeautifulSoup.BeautifulSoup(html_info)
    data = soup.findAll('tr')[1:]
    price_list = [float(i.findAll('td')[8].text) for i in data]
    return list(reversed(price_list))


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._tr_count = 0
        self._tr_flag = False
        self.data = []

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._tr_count += 1
            self._tr_flag = True

    def handle_endtag(self, tag):
        if tag == 'tr':
            self._tr_flag = False

    def handle_data(self, data):
        if self._tr_flag:
            if len(self.data) < self._tr_count:
                self.data.append([])

            if re.findall(r'[\.\d]+', data):
                self.data[self._tr_count - 1].append(data)


def test_html_parser():
    my_html_parser = MyHTMLParser()
    f = open('test.html')
    my_html_parser.feed(f.read())
    f.close()
    print my_html_parser.data


if __name__ == "__main__":
    # test_html_parser()
    # print get_close_price_from_sina(code="0027", year=2015, season=1)
    # get_a_stock_list(16)
    # get_given_stock_price(
    # get_price_data("0066.HK", start_date='2014-10-09', end_date='2015-03-31')
    price_dict = prepare_stock_info()
    # pprint.pprint(price_dict)
    f = open("stock_price_2015_s1.txt", "w")
    # f.write('{')
    # for i in price_dict:
    #     write_string = '\"%s\": [%s' % (i, price_dict[i][0])
    #     for j in price_dict[i][1:]:
    #         write_string = "%s, %s" % (write_string, j)
    #
    #     write_string = "%s],\n" % write_string
    #
    #     f.write(write_string)
    # f.write('}\n')
    # f.write(pprint.pformat(price_dict, width=800))
    # f.close()
    # price_dict = eval(f.read())
    # f.close()

    # f = open('stock_price', 'w')
    pickle.dump(price_dict, f)
    f.close()
    # f = open('stock_price')
    # price_dict = pickle.load(f)
    # f.close()
    #
    # for i in price_dict:
    #     for j, k in enumerate(price_dict[i]):
    #         price_dict[i][j] = round(k, 2)
    #
    # f = open('complete_stock_price', 'w')
    # pickle.dump(price_dict, f)
    # f.close()
    # f = open("pformat_stock_price.txt", 'w')
    # f.write(pprint.pformat(price_dict, width=800))
    # f.close()
