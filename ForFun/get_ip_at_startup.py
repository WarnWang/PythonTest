#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: get_ip_at_startup
# Author: Mark Wang
# Date: 6/8/2016

import os
import smtplib
import time
import urllib2
from email import MIMEMultipart
from email import MIMEText


def send_email_through_gmail(subject, msg_body, to_addr='wangyouan@gmail.com'):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('wangyouan@gmail.com', '')

    msg = MIMEMultipart.MIMEMultipart()
    msg['From'] = 'wangyouan@gmail.com'
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText.MIMEText(msg_body, 'plain'))
    text = msg.as_string()
    server.sendmail('wangyouan@gmail.com', to_addr, text)
    server.close()


def get_ip_address(ifname):
    ipv4 = os.popen(
        'ip addr show %s | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'' % (
            ifname)).read().strip()
    return ipv4


def internet_on():
    try:
        response = urllib2.urlopen('http://74.125.204.105', timeout=1)
        return True
    except urllib2.URLError as err:
        pass
    return False


ip = get_ip_address('eth0')
print ip
while not ip.startswith('147'):
    time.sleep(5)
    ip = get_ip_address('eth0')
    print ip

while not internet_on():
    time.sleep(5)
    
send_email_through_gmail(subject="ip address of {}".format(os.uname()[1]), msg_body=ip)
