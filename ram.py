#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-08 17:09:49
# @Author  : Lewis Tian (chasetichlewis@gmail.com)
# @GitHub  : https://github.com/LewisTian
# @Version : Python3.5

'''
MySQL table `ram`
collum : id(auto_increment), name, price, shop, comments, href
'''

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import pymysql.cursors
from time import sleep

try:
    conn = pymysql.connect( host='localhost',
                            user=$user,
                            password=$psw,
                            db=$db,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
except Exception as e:
    raise e

class JD():
    def __init__(self, kw, page):
        self.kw = kw
        self.page = page
        self.result = set()
        self.headers = {
            'X-Requested-With':'XMLHttpRequest',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
            }

    # 按销量排行
    def run(self):
        ref = 'https://search.jd.com/Search?keyword={0}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&click=0'
        referer = ref.format(self.kw) # 如果不进行url编码这里会报错，所以直接在main()创建spider时就进行编码
        self.headers['Referer'] = referer
        
        # 每页前30个商品
        base_url = '''https://search.jd.com/s_new.php?keyword=''' + self.kw + '''
            &enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&page={p}&s={count}&click=0'''
        # 每页后30个商品
        ajax_url = '''https://search.jd.com/s_new.php?keyword=''' + self.kw + '''
            &enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&page={p}&s=31&scrolling=y
            &log_id=1507459781.34746&tpl=1_M'''
        
        i = 1
        while i < self.page*2 + 1:
            print(i)
            url = base_url.format(p = i, count = (i-1)*60+1)
            r = requests.get(url, headers = self.headers).text
            self.parse(r)
            i = i + 1
            url = ajax_url.format(p = i)
            r = requests.get(url, headers = self.headers).text
            self.parse(r)
            i = i + 1
            sleep(3)

    def parse(self, html):
        bs = BeautifulSoup(html, 'html5lib').find_all('li', {'class', 'gl-item'})
        sql = "insert into ram (name, price, shop, comments, href) values ('%s', '%s', '%s', '%s', '%s');"
        global count
        for b in bs:
            try:
                name = b.find('div', {'class', 'p-name'}).a.em.text # 名字
                price = b.find('div', {'class', 'p-price'}).strong.i.text # 价格
                cmts = b.find('div', {'class', 'p-commit'}).strong.a.text # 评论数
                href = 'https:' + b.find('div', {'class', 'p-img'}).a['href'] # 链接
                shop = b.find('div', {'class', 'p-shop'}).span.a.text # 店铺
                # p_id = b['data-sku'] # 商品的id
                # print(name, price, shop, cmts, href)
            except:
                pass
            try:
                cur.execute(sql % (name or '', price  or '', shop or '', cmts or '', href or ''))
            except:
                pass
        conn.commit()

if __name__ == "__main__":
    spider = JD(quote("笔记本内存条"), 41)
    spider.run()
    cur.close()
    conn.close()

