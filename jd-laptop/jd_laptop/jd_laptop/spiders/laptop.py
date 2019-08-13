#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-22 13:16:41
# @Author  : Lewis Tian (chtian@hust.edu.cn)
# @Link    : https://lewistian.github.io
# @Version : Python3.7

import os
import csv
import json
import scrapy
import jd_laptop.settings as settings

PROPERTY = ['title',
            'product_id',
            'price',
            'shop_name',
            'shop_id',
            'comment',
            'good_comment',
            'good_rate',
            'poor_comment',
            'poor_rate'
            ]

PROPERTY_LEN = len(PROPERTY)

# 0: json 1: csv
SAVE_DATA_TYPE = 1

class LaptopSpider(scrapy.Spider):
    name = 'laptop'
    start_urls = ['https://list.jd.com/list.html?cat=670,671,672']
    page = 1
    max_page = -1
    has_more = True
    products = {}
    '''
    products: {
        id1 : {product1},
        id2 : {product2},
    }
    ---
    product: {
        title： ${title}
        product_id： ${product_id}
        price： ${price}
        shop_name： ${shop_name}
        shop_id： ${shop_id}
        comment_count： ${comment_count}
        good_comment： ${good_comment}
        good_rate： ${good_rate}
        poor_comment： ${poor_comment}
        poor_rate： ${poor_rate}
    }
    '''

    def __init__(self, *args, **kwargs):
        super(LaptopSpider, self).__init__(*args, **kwargs)

        if not os.path.exists(settings.DATA_PATH):
            os.mkdir(settings.DATA_PATH)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(LaptopSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=scrapy.signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        # https://stackoverflow.com/questions/31320470/scrapy-spider-destructor-del-never-executed
        print(f'page: {self.page}, step into spider_closed...')
        self.save_products()

    def parse(self, response):
        print(f'step into parse {self.page}...')
        # path = settings.DATA_PATH
        # with open(f'{path}/laptop_{self.page}.html', 'w', encoding='utf-8') as f:
        #     f.write(response.text)

        if self.max_page == -1:
            self.max_page = int(response.xpath('//span[@class="fp-text"]/i/text()').get())

        if self.page == self.max_page:
            self.has_more = False

        items = response.xpath('//li[@class="gl-item"]')
        reference_ids = []
        for item in items:
            title = item.xpath('div/div[@class="p-name"]/a/em/text()').get().strip()
            product_id = item.xpath('div/div[@class="p-name"]/a/@href').get().split('/')[-1].split('.')[0]
            reference_ids.append(product_id)

            product = {}
            product['product_id'] = product_id
            product['title'] = title
            self.products[product_id] = product

            # print(product_id, title)

        req = []
        # comments request, 2 steps, 1: 0-30 2: 30-60
        # shop request, same as comments request
        # price request, same as comments request
        if len(reference_ids) <= 30:
            comment_url = (f'https://club.jd.com/comment/productCommentSummaries.action?'
                           f'my=pinglun&referenceIds={",".join(reference_ids)}&callback=')
            r = scrapy.Request(comment_url, callback=self.parse_comment)
            req.append(r)

            shop_url = (f'https://chat1.jd.com/api/checkChat?my=list&pidList'
                        f'={",".join(reference_ids)}&callback=')
            r = scrapy.Request(shop_url, callback=self.parse_shop)
            req.append(r)


            price_url = (f'https://p.3.cn/prices/mgets?callback=&ext=&pin=&type=1&area='
                         f'&skuIds={",".join([f"J_{x}" for x in reference_ids])}&pdbp=0'
                         f'&pdtk=&pdpin=&pduid=&source=list_pc_front')
            r = scrapy.Request(price_url, callback=self.parse_price)
            req.append(r)
        else:
            comment_url = (f'https://club.jd.com/comment/productCommentSummaries.action?'
                           f'my=pinglun&referenceIds={",".join(reference_ids[:30])}&callback=')
            r = scrapy.Request(comment_url, callback=self.parse_comment)
            req.append(r)
            comment_url = (f'https://club.jd.com/comment/productCommentSummaries.action?'
                           f'my=pinglun&referenceIds={",".join(reference_ids[30:])}&callback=')
            r = scrapy.Request(comment_url, callback=self.parse_comment)
            req.append(r)

            shop_url = (f'https://chat1.jd.com/api/checkChat?my=list&pidList='
                        f'{",".join(reference_ids[:30])}&callback=')
            r = scrapy.Request(shop_url, callback=self.parse_shop)
            req.append(r)
            shop_url = (f'https://chat1.jd.com/api/checkChat?my=list&pidList='
                        f'{",".join(reference_ids[30:])}&callback=')
            r = scrapy.Request(shop_url, callback=self.parse_shop)
            req.append(r)

            price_url = (f'https://p.3.cn/prices/mgets?callback=&ext=&pin=&type=1&area=&skuIds='
                         f'{",".join([f"J_{x}" for x in reference_ids[:30]])}&pdbp=0&pdtk=&pdpin='
                         f'&pduid=&source=list_pc_front')
            r = scrapy.Request(price_url, callback=self.parse_price)
            req.append(r)
            price_url = (f'https://p.3.cn/prices/mgets?callback=&ext=&pin=&type=1&area=&skuIds='
                         f'{",".join([f"J_{x}" for x in reference_ids[30:]])}&pdbp=0&pdtk=&pdpin='
                         f'&pduid=&source=list_pc_front')
            r = scrapy.Request(price_url, callback=self.parse_price)
            req.append(r)

        if self.has_more:
            self.page += 1
            next_url = f'https://list.jd.com/list.html?cat=670,671,672&page={self.page}'
            r = scrapy.Request(next_url, callback=self.parse)
            req.append(r)

        return req

    def parse_comment(self, response):
        # print('step into parse_comment...')
        try:
            comments = json.loads(response.text)['CommentsCount']
        except Exception as e:
            print(e)
            return
        for comt in comments:
            product_id = str(comt['ProductId'])
            comment = comt['CommentCountStr']
            good_comment = comt['GoodCountStr']
            good_rate = comt['GoodRate']
            poor_comment = comt['PoorCountStr']
            poor_rate = comt['PoorRate']

            if not product_id in self.products:
                product = {}
                product['product_id'] = product_id
                self.products[product_id] = product
            self.products[product_id]['comment'] = comment
            self.products[product_id]['good_comment'] = good_comment
            self.products[product_id]['good_rate'] = good_rate
            self.products[product_id]['poor_comment'] = poor_comment
            self.products[product_id]['poor_rate'] = poor_rate

            # print(comment, good_rate, poor_rate)

    def parse_shop(self, response):
        print('step into parse_shop...')
        try:
            shops = json.loads(response.text[1:-2])
        except Exception as e:
            print(e)
            return
        for shop in shops:
            shop_name = shop['seller']
            product_id = str(shop['pid'])
            shop_id = shop['shopId']

            if not product_id in self.products:
                product = {}
                product['product_id'] = product_id
                self.products[product_id] = product
            self.products[product_id]['shop_name'] = shop_name
            self.products[product_id]['shop_id'] = shop_id

            # print(shop_name, product_id)

    def parse_price(self, response):
        print('step into parse_price...')
        try:
            prices = json.loads(response.text[1:-3])
        except Exception as e:
            print(e)
            return
        for p in prices:
            product_id = p['id'].split('_')[-1]
            price = p['p']
            price_m = p['m']
            price_op = p['op']

            if not product_id in self.products:
                product = {}
                product['product_id'] = product_id
                self.products[product_id] = product
            self.products[product_id]['price'] = price

            # print(product_id, price, price_m, price_op)

    def save_products(self):
        if not self.products:
            return

        if SAVE_DATA_TYPE:
            self.save_as_csv()
        else:
            self.save_as_json()

    def save_as_csv(self):
        products = [PROPERTY]
        try:
            products += [[x[PROPERTY[i]] for i in range(PROPERTY_LEN)] for x in self.products.values()]
        except Exception as e:
            print(e)
            return save_as_json()

        path = settings.DATA_PATH
        with open(f'{path}/data_{self.page}.csv', 'w', encoding='utf-8', newline='') as f:
            csv_f = csv.writer(f)
            csv_f.writerows(products)

    def save_as_json(self):
        products = [product for product in self.products.values()]
        
        path = settings.DATA_PATH
        with open(f'{path}/data_{self.page}.json', 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
