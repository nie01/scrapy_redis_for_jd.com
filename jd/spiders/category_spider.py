# -*- coding:utf-8 -*-

# import scrapy
from scrapy import Request
from scrapy_redis.spiders import RedisSpider

from jd.items import ImagesDownloadItem


class MySpider(RedisSpider):
    name = 'category_list'  # 蜘蛛名称

    # 接收的状态码
    handle_httpstatus_list = [403,404,500]

    # 数据库参数设置
    custom_settings = {
        'REDIS_HOST': '',
        'REDIS_PORT': 6379,
        'REDIS_PARAMS': {
            'password': 'abc+ABC+123+root',
            'db': 0
        }
    }

    # def start_requests(self):
    #     self.logger.info('开始爬url')
    #     # url = 'http://www.abc.com/'
    #     url = 'https://www.xinli001.com/info/100388065'
    #     yield Request(url=url, callback=self.parse_start)

    # def parse_start(self, response):
    #     url = response.url
    #     print('解析函数url=', url)
    #     t = response.xpath('//title/text()').extract()[0]
    #     print('标题：', t)
    #     # print('正文内容', response.text)

    def parse(self, response):
        url = response.url
        print('parse解析函数url=', url)
        t = response.xpath('//title/text()').extract()[0]
        print('标题：', t)
        # print('正文内容', response.text)

        imgItem = ImagesDownloadItem()
        imgItem['referer'] = url
        imgItem['name'] = '百度logo'
        imgItem['src'] = 'https://www.baidu.com/img/baidu_jgylogo3.gif'
        yield imgItem

        # url = 'https://www.xinli001.com/info/100388065'
        # # url = 'http://www.abc.com/?n=1'
        # meta = {'requests_key': 'jd:detail_requests'}
        # yield Request(url=url, callback=self.parse_detail, meta=meta)

    def parse_detail(self, response):
        url = response.url
        print('parse_detail解析函数url=', url)
        # 这里只是为了传递回调函数实例化，然后队列已交由 detail 爬虫处理
        pass