#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-22 21:33:56
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import os
import csv
import random
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style='ticks',
        rc={
            'figure.figsize': [12, 7],
            'text.color': 'white',
            'font.family': ['SimHei', 'STXihei'],
            'axes.labelcolor': 'white',
            'axes.edgecolor': 'white',
            'xtick.color': 'white',
            'ytick.color': 'white',
            'axes.facecolor': '#443941',
            'figure.facecolor': '#443941'}
        )

def convert():
    '''take out the author and title information & save as txt'''
    if not os.path.exists('data_981.csv'):
        return
    title_list = []
    shop_list = []
    with open('data_981.csv', encoding='utf-8') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            title_list.append([row[0]])
            shop_list.append([row[3]])
    with open(f'title.txt', 'w', encoding='utf-8', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(title_list)
    with open(f'shop.txt', 'w', encoding='utf-8', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(shop_list)

def top1000():
    if not os.path.exists('top1000.csv'):
        return
    data = {
        '荣耀': 0,
        '苹果': 0,
        '华硕': 0,
        '华为': 0,
        '小米': 0,
        '戴尔': 0,
        '联想': 0,
        '惠普': 0,
        '微软': 0,
        '神舟': 0,
        '宏基': 0,
        '其他': 0
    }
    # 销量
    with open('top1000.csv', encoding='utf-8') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            find_one = False
            for k in data.keys():
                if row[0].find(k) >= 0:
                    data[k] += 1
                    find_one = True
                    break
            if not find_one:
                data['其他'] += 1

    # 好评率
    # with open('top_1000.csv', encoding='utf-8') as f:
    #     f_csv = csv.reader(f)
    #     for row in f_csv:
    #         find_one = False
    #         for k in data.keys():
    #             if row[0].find(k) >= 0:
    #                 data[k] += 1
    #                 find_one = True
    #                 break
    #         if not find_one:
    #             data['其他'] += 1
    print(data)

    plt.bar(range(len(data)), data.values(), tick_label=list(data.keys()), color="white")
    plt.show()


if __name__ == '__main__':
    top1000()