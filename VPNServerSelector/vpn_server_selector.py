#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: vpn_server_selector
# @Date: 3/6/2017
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function

import pandas as pd
import pyping

server_list = []
max_count_num = 10

for i in range(1, 8):
    server_list.append('us{}.x1g.site'.format(i))

server_list.append('jp1.x1g.site')

for i in range(1, 7):
    server_list.append('jp0{}.ipip.pm'.format(i))

    if i == 1:
        server_list.append('uk01.ipip.pm')
        server_list.append('ca01.ipip.pm')
        server_list.append('ru01.ipip.pm')

    if i < 3:
        server_list.append('tw0{}.ipip.pm'.format(i))
        server_list.append('kr0{}.ipip.pm'.format(i))

    if i < 4:
        server_list.append('us0{}.ipip.pm'.format(i))
        server_list.append('sg0{}.ipip.pm'.format(i))

    if i < 5:
        server_list.append('hk0{}.ipip.pm'.format(i))

result_df = pd.DataFrame(columns=['avg_time', 'lost'])

index = 0


def get_server_info(address, count=max_count_num, timeout=300):
    r = pyping.ping(address, count=count, packet_size=100, timeout=timeout, udp=True)

    avg_time = r.avg_rtt
    lost = r.packet_lost

    return avg_time, lost


for i in server_list:
    print('Start to test {}'.format(i))
    try:
        av, loss = get_server_info(i)
        if loss == max_count_num:
            continue
        result_dict = {'avg_time': float(av),
                       'lost': int(loss)}
        result_df.loc[i] = result_dict
        print('average return time is {}, lost is {}'.format(av, loss))

    except Exception as e:
        print(e)

server_to_select = None
for i in range(max_count_num):
    server_to_select = result_df[result_df['lost'] == i]
    if not server_to_select.empty:
        selected_server = server_to_select.sort_values(by='avg_time', ascending=True).index[0]
        if 'ipip' in selected_server:
            print()
            print('Server: {}'.format(selected_server))
            print('Password: 328912')
            print('Port number: 48328')
            print('Encryption type: rc4-md5')

        else:
            print('Server: {}'.format(selected_server))
            print('Password: 71qKwjbT57')
            print('Port number: 10580')
            print('Encryption type: AES-256-CFB')

        break

else:
    print("No such server")
