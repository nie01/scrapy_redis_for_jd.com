# -*- coding:utf-8 -*-

import hashlib
import re
# import scrapy
from scrapy import Request
from scrapy_redis.spiders import RedisSpider

from jd.items import ImagesDownloadItem


class MySpider(RedisSpider):
    name = 'image_download'  # 蜘蛛名称
    # idle_timeout = 30  # 空闲超时，定义此数值值将会让setting里的参数失效。idle_timeout必须>5 否则空闲不受限制
    redis_key = 'jd:img_start_url'
    requests_key = 'jd:img_requests'  # 队列的redis.key

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

    def parse(self, response):
        url = response.url
        print('parse解析函数url=', url)
        # t = response.xpath('//title/text()').extract()[0]
        # print('标题：', t)
        # print('正文内容', response.text)

    def parse_img(self, response):
        print(response.meta)
        # print('parse_img 解析函数url=', response.url)
        fileName = self.meke_file_name(response)
        path = 'imgs/%s'%fileName
        print(path)
        with open(path, 'wb') as f:
            f.write(response.body)

    def meke_file_name(self, response):
        '''
        生成文件名
        :param response:
        :return:
        '''
        urlmd5 = hashlib.md5(response.body).hexdigest()
        name = response.url.split('/')[-1]   # 完整文件名称
        name1 = name.split('.')[0]  # 不含扩展名
        name2 = name.split('.')[-1]  # 扩展名
        if len(name2) > 5 or len(name2)<1:
            # 没有正常的扩展名 所有统一 使用jpg作为扩展名
            name2 = 'jpg'

        file_name = 'urlmd5_%s.%s'%(urlmd5, name2)
        # n = response.meta['name']
        # file_name = '%s.%s'%(n, name2)

        # 规范文件名
        file_name = re.sub('[*?"<>|]]', '-',file_name)  # 去掉文件名中的非法字符
        file_name = file_name.replace('\\','/')
        file_name = re.sub('/{2,}','/',file_name)

        return file_name
