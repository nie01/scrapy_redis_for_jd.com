# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib
import copy

import scrapy
from scrapy.pipelines.images import ImagesPipeline

from jd.items import ImagesDownloadItem


class JdPipeline(object):
    def process_item(self, item, spider):
        return item


class ImagesDownloadPipeline(ImagesPipeline):
    '''
    下载图片管道
    '''
    def get_media_requests(self,item,info):
        o = copy.deepcopy(item)  # 深度复制，是为了防止请求过快，造成后面的item数据覆盖前面的数据item
        # print(o)
        # print(info)
        yield scrapy.Request(url=o['src'],meta={'name':o['name'],'referer':o['referer']})

        # # 测试
        # for i in range(1000):
        #     url = 'http:www.abc.com/?t=%d.jpg'%i
        #     print('yield=>',url)
        #     yield scrapy.Request(url=url,meta={'name': 'name-%d'%i,'referer': o['referer']})

    def file_path(self,request,response=None,info=None):
        '''
        自定义 图片文件名称
        :param request:
        :param response:
        :param info:
        :return:
        '''
        if request.meta['referer']:
            # request.headers['Referer'] = request.meta['referer']
            request.headers.setdefault('Referer', request.meta['referer'])

        url = request.url
        urlmd5 = hashlib.md5(url.encode('utf-8')).hexdigest()
        # name = url.split('/')[-1]  # 完整文件名称
        name2 = url.split('.')[-1]  # 扩展名
        if not name2:
            name2 = 'jpg'

        file_name = 'urlmd5_%s.%s'%(urlmd5, name2)
        # print(request.meta)
        print(file_name)
        # a = 1/0
        return file_name



