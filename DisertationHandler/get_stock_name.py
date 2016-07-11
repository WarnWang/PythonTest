#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: get_stock_name
# Author: Mark Wang
# Date: 30/6/2016

import io
import re
import urllib
import urllib2

from BeautifulSoup import BeautifulSoup


def get_stock_symbol_name(symbol):
    url = 'http://finance.yahoo.com/q?s={}'.format(symbol)
    query = urllib2.Request(url)
    response = urllib2.urlopen(query)
    html = response.read()
    response.close()
    soup = BeautifulSoup(html)
    title = soup.title.text
    return re.findall(r'Summary for ([\w\W]+)- Yahoo', title)[0]


def http_get(url, data=None):
    if data is not None:
        url = '{}?{}'.format(url, urllib.urlencode(data))

    query = urllib2.Request(url)
    response = urllib2.urlopen(query)
    html = response.read()
    response.close()

    return html


def format_str(string_info):
    if string_info is None:
        return None
    if '&nbsp' in string_info:
        string_info = re.findall(r'([\s\S]+)&nbsp', string_info)[0]

    return string_info.replace('&', '\\&').strip()


class StockInformationGen(object):
    def __init__(self, stock_list=None):
        self._stock_list = stock_list

    def generate_latex_code(self, company_name, symbol, activities, industry, summary):
        code = r'''\section{%s}
\textbf{Symbol in Yahoo Finance}: %s\\
\textbf{Principal Activities}: %s\\
\textbf{Industry Classification}: %s
\paragraph{Summary}
%s''' % (company_name, symbol, activities, industry, summary)
        return code

    def get_summary_info(self, symbol):
        html = http_get('http://finance.yahoo.com/q', (('s', symbol),))
        soup = BeautifulSoup(html)
        summary = soup.find(id='yfi_business_summary').findAll('div')[1].text
        if 'View More' in summary:
            summary = re.findall(r'([\s\S]+)View More', summary)[0]

        if '...' in summary:
            summary = summary.replace('...', '.')

        summary = re.sub(r'&', r'\&', summary)

        summary = re.sub(ur'[^\x00-\x7F]', '\'', summary)

        return summary

    def get_other_info(self, symbol):
        html = http_get(
            'https://www.hkex.com.hk/eng/invest/company/profile_page_e.asp?WidCoID={}&WidCoAbbName=&Month=&langcode=e'.format(
                int(symbol[:-3])))
        soup = BeautifulSoup(html)
        table = None
        for table in soup.findAll('table'):
            if 'Company/Securities Name' in table.getText():
                break

        company_name = None
        activities = None
        industry = None

        if table is None:
            print 'can not get stock info of', symbol
        tr_list = table.findAll('tr')
        for tr in tr_list:
            td_list = tr.findAll('td')
            if len(td_list) != 2:
                continue

            elif 'Company/Securities Name' in td_list[0].text:
                company_name = td_list[1].text

            elif 'Principal Activities' in td_list[0].text:
                activities = td_list[1].text

            elif 'Industry Classification' in td_list[0].text:
                industry = td_list[1].text

            elif company_name is not None and activities is not None and industry is not None:
                break

        return format_str(company_name), format_str(activities), format_str(industry)

    def generate_stock_information(self):
        string_info = ""
        for symbol in self._stock_list:
            company_name, activities, industry = self.get_other_info(symbol)
            summary = self.get_summary_info(symbol)
            code = self.generate_latex_code(company_name, symbol, activities, industry, summary)
            string_info = u"{}\n\n\n{}".format(string_info, code)

        print string_info
        with io.open('stock_info.tex', 'w', encoding='utf8') as f:
            f.write(string_info)

    def get_stock_info_list(self):
        dict_list = []
        for symbol in self._stock_list:
            company_name, activities, industry = self.get_other_info(symbol)
            summary = self.get_summary_info(symbol)
            dict_list.append({u'Symbol': unicode(symbol),
                              u'Name': unicode(company_name),
                              u'Activities': unicode(activities),
                              u'Industry': unicode(industry),
                              u'Summary': unicode(summary)})

        headers = [u'Symbol', u'Name', u'Activities', u'Industry', u'Summary']
        with io.open('stock_info.csv', 'w', encoding='utf8') as f:
            # with open('stock_info.csv', 'w') as f:
            f.write(u'\t'.join(headers))
            f.write(u'\n')
            for info in dict_list:
                uni = []
                for head in headers:
                    uni.append(info[head])
                f.write(u'\t'.join(uni))
                f.write(u'\n')


if __name__ == '__main__':
    # file_path = '/Users/warn/Documents/Projects/stock_price/SmallAverage/all_info.xlsx'
    # wb = openpyxl.load_workbook(file_path)
    # ws = wb.active
    # for row in ws.rows:
    #     if len(row) > 0 and row[0].value.endswith('.HK'):
    #         stock_symbol = row[0].value
    #         print stock_symbol, get_stock_symbol_name(stock_symbol)
    # symbol_list = []
    # with open('symbol_list.csv') as f:
    #     reader = csv.DictReader(f)
    #     for line in reader:
    #         symbol_list.append(line['Stock Symbol'])

    symbol_list = ['0001.HK', '0002.HK', '0003.HK', '0004.HK', '0005.HK', '0006.HK', '0008.HK', '0009.HK', '0010.HK',
                   '0012.HK', '0014.HK', '0016.HK', '0023.HK', '0030.HK', '0032.HK', '0027.HK', '2282.HK',
                   '0120.HK', '6823.HK', '0038.HK']

    symbol_list.sort()

    test = StockInformationGen(symbol_list)
    # s = test.get_summary_info('0745.HK')
    # print s
    # print re.sub(ur'[^\x00-\x7F]', '\'', s)
    test.generate_stock_information()
