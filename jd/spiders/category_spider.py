# -*- coding:utf-8 -*-

import scrapy
# from scrapy import Request

class MySpider(scrapy.Spider):
    name = 'category_list' # 蜘蛛名称

    def start_requests(self):
        self.logger.info('开始爬url')
        # url = 'http://www.abc.com/'
        url = 'https://www.xinli001.com/info/100388065'
        yield scrapy.Request(url=url, callback=self.parse_start)

    def parse_start(self, response):
        url = response.url
        print('解析函数url=', url)
        t = response.xpath('//title/text()').extract()[0]
        print('标题：', t)
        # print('正文内容', response.text)
