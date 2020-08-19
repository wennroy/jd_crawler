# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 09:07:36 2020

@author: lengwaifang
"""

import scrapy
from lenovo.items import LenovoItem
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import re
import datetime
import urllib
from lenovo.__init__ import *

class QuotesSpider(scrapy.Spider):
    search_name = urllib.parse.quote(Search_name)
    name = "lenovo"
    item_list = []
    show_item_id = []
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'referer': 'https://search.jd.com/Search?keyword=%E8%81%94%E6%83%B3&qrst=1&wq=%E8%81%94%E6%83%B3&ev=exbrand_%E8%81%94%E6%83%B3%EF%BC%88Lenovo%EF%BC%89%5E&page=1&s=1&click=0'
    }
    def start_requests(self):
        for x in range(total_page):
            item_num = 1 + x * 60
            page_num = 2 * x + 1  # 's_new.php?'
            url = 'https://search.jd.com/s_new.php?keyword=' + self.search_name + '&wq='+self.search_name + \
                  '&s=' + str(item_num) + '&page=' + \
                  str(page_num) + '&click=0'
            referer_url = 'https://search.jd.com/Search?keyword=' + self.search_name+ '&wq='+self.search_name + \
                          str(page_num) + '&s=' + str(item_num) + '&click=0'
            self.headers['referer'] = referer_url
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse, headers=self.headers,
                                 meta={'page': page_num, 'item': item_num, 'retry': 0})

    ## /div[@class='p-name p-name-type-2']/a/em
    ## /div[@class='p-name p-name-type-2']/a/em
    def parse(self, response):
        self.show_item_id = []
        retry = response.meta['retry']
        all_item = response.xpath("//div[@class='gl-i-wrap']")
        if len(all_item) == 0:
            retry += 1
            print(f'重试了{retry}次，警告：重试5次以上将会跳过第{response.meta["page"]}页的搜索。')
            if not retry >5:
                yield scrapy.Request(url=response.url, dont_filter=True, callback=self.parse, headers=self.headers,
                                     meta={'page': response.meta['page'], 'item': response.meta['item'], 'retry': retry})

        for content in all_item:
            num_str = content.xpath(".//div[@class='p-commit']/strong/a/@id").get()
            item_id = re.search(r"\d+", num_str).group(0)
            id_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=' + str(item_id)
            self.show_item_id.append(item_id)
            # if content.xpath(".//a[@class='curr-shop hd-shopname']/text()").get() == '立诗文二手笔记本专营店':
            #     print(content.xpath(".//div[@class='p-name p-name-type-2']/a/em/text()").get())
                ## '<em><font class="skcolor_ljg">联想</font>拯救者Y7000P 2020新品英特尔10代酷睿i7电竞屏吃鸡游戏本 15.6英高色域笔记本电脑 标配【i7-10875H 16G内存 512固态】 RTX2060/GTX1660Ti 6G钛晶灰</em>'
                ##<em><span class="p-tag" style="background-color:#c81623">京品电脑</span>\t\n<font class="skcolor_ljg">联想</font>小新Air14 2020锐龙版(全新7nm)六核金属超轻薄笔记本电脑 学生本商务设计游戏轻薄本 标配【R5 4600U 16G内存 512固态】灰</em>'
            item_name = ''
            for i in content.xpath(".//div[@class='p-name p-name-type-2']/a/em//text()").getall():
                item_name += i.strip()
            item_name = item_name.strip()
            # item_name.replace('<em><font class="skcolor_ljg">联想</font>','联想')
            # item_name.replace('</em>','')
            if re.findall(r'[\u4E00-\u9FA5A-Za-z0-9_]+', item_name) == []:
                item_name = content.xpath(".//div[@class='p-name p-name-type-2']/a/em").get()
                item_name = item_name[item_name.find('</font>') + 7:-5]
            item_name = item_name.strip()
            temp_dict = {'price': content.xpath(".//div[@class='p-price']//i/text()").get(),
                         'name': item_name,
                         'shopname': content.xpath(".//a[@class='curr-shop hd-shopname']/text()").get(),
                         'item_id': item_id}
            yield scrapy.Request(id_url, dont_filter=True, meta=temp_dict, callback=self.parse_2)

        print(self.show_item_id)
        if response.url.find('show_items') == -1:
            page_num = 1 + response.meta['page']
            item_num = 30 + response.meta['item']
            show_item_str = ''
            for x in self.show_item_id:
                show_item_str += str(x) + ','
            show_item_str = show_item_str[:-1]
            next_url = 'https://search.jd.com/s_new.php?keyword=' + self.search_name + '&wq=' + self.search_name + \
                  '&s=' + str(item_num) + '&page=' + \
                  str(page_num) + '&click=0' + '&show_items=' + show_item_str
            self.headers[
                'referer'] = 'https://search.jd.com/Search?keyword='+self.search_name+'&wq=' + self.search_name + \
                          str(page_num) + '&s=' + str(item_num) + '&click=0'
            yield scrapy.Request(next_url, dont_filter=True, callback=self.parse, headers=self.headers,
                                 meta={'page': page_num, 'item': item_num, 'retry': 0})

    def parse_2(self, response):
        import json
        comment_dict = json.loads(response.text)
        comment_num = comment_dict['CommentsCount'][0]['CommentCount']
        GoodRate = comment_dict['CommentsCount'][0]['GoodRate']
        DefaultGoodCount = comment_dict['CommentsCount'][0]['DefaultGoodCount']
        GoodCount = comment_dict['CommentsCount'][0]['GoodCount']
        PoorCount = comment_dict['CommentsCount'][0]['PoorCount']
        PoorRate = comment_dict['CommentsCount'][0]['PoorRate']

        item = LenovoItem()
        item['start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['name'] = response.meta['name']
        item['price'] = response.meta['price']
        item['shopname'] = response.meta['shopname']
        item['num_comment'] = comment_num
        item['item_id'] = response.meta['item_id']
        item['GoodRate'] = GoodRate
        item['GoodCount'] = GoodCount
        item['DefaultGoodCount'] = DefaultGoodCount
        item['PoorCount'] = PoorCount
        item['PoorRate'] = PoorRate
        yield item


if __name__ == "__main__":
    cp = CrawlerProcess(get_project_settings())
    cp.crawl(QuotesSpider)
    cp.start()
