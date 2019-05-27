# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib
import copy
import time
import scrapy
import pymysql
import logging

from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from jd.items import GoodsItem
from jd.items import GoodsListItem

from jd.items import ImagesDownloadItem


def toQSLtxt(txt):
    # // 转为SQL字符串
    txt = txt.replace("\\", "\\\\")  # 此项必须潜在最前 否则会破坏后面的
    txt = txt.replace("\n", "\\n")
    txt = txt.replace("\r", "\\r")
    txt = txt.replace("'", "\\'")
    return txt


# class JdPipeline(object):
#     def process_item(self, item, spider):
#         return item


class GoodsPipelines(object):
    def __init__(self):
        print('初始化管道')
        # 链接数据库
        self.connect = pymysql.connect(host='localhost',
                                  user='root',
                                  passwd='abc+ABC+123+root',
                                  db='spider',
                                  charset='utf8',  # 注意这里charset属性为 ‘utf8’，中间没有-
                                  )
        # 获取操作指针
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if not isinstance(item, CategoryListItem):
            return item  # 不是对应的 item

        try:
            # 插入数据库
            self.cursor.execute('''insert into `jd_goods`(`goods_id`,`name`,`img1`)
              value(%s,%s,%s)
            ''', (item['goods_id'], item['name'], item['img1']))
            self.connect.commit()  # 提交SQL语句

        except Exception as error:
            print('异常：',error)
            # spider.logger.error(error)
        except:
            print('----------------------------------------//')

        print('已保存！',item['goods_id'])
        return item


class GoodsListPipelines(object):
    '''
    批量提交商品入库
    '''
    def __init__(self):
        print('初始化管道')
        # 链接数据库
        self.connect = pymysql.connect(host='localhost',
                                  user='root',
                                  passwd='abc+ABC+123+root',
                                  db='spider',
                                  charset='utf8',  # 注意这里charset属性为 ‘utf8’，中间没有-
                                  )
        # 获取操作指针
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if not isinstance(item, GoodsListItem):
            return item  # 不是对应的 item

        sql = "insert into `jd_goods`(`goods_id`,`name`,`img1`)\n  value"
        values = ''
        for one in item['list']:
            # values += "(%s,'%s','%s'),\n" % (toQSLtxt(one['goods_id']), one['name'], one['img1'])
            values += "(%s,'%s','%s'),\n"%(toQSLtxt(str(one['goods_id'])), toQSLtxt(one['name']), toQSLtxt(one['img1']))

        values = values[0:-2]  # 去掉最后一个逗号
        sql += values + ' on duplicate key update goods_id=values(goods_id);'  # 组合字符串,如果有重复id则保持不变 ,name=values(name)
        print(sql)
        re = self.cursor.execute(sql)
        print(re)

        try:
            # 插入数据库
            pass
            # print(item)

            # values = []
            # for one in item['list']:
            #     values.append((one['goods_id'], one['name'], one['img1']))
            #
            # # self.cursor.execute('''insert into `jd_goods`(`goods_id`,`name`,`img1`)
            # self.cursor.executemany('''insert into `jd_goods`(`goods_id`,`name`,`img1`)
            #   value(%s,%s,%s)
            # ''', values)
            # self.connect.commit()  # 提交SQL语句

        except Exception as error:
            print('异常：', error)
            # spider.logger.error(error)
        except:
            print('----------------------------------------//')

        print('已保存！')
        # print('已保存！',item['goods_id'])
        return item

class ImagesDownloadPipeline(ImagesPipeline):
    '''
    下载图片管道
    '''
    def get_media_requests(self,item,info):
        o = copy.deepcopy(item)  # 深度复制，是为了防止请求过快，造成后面的item数据覆盖前面的数据item
        # print(o)
        # print(info)
        yield scrapy.Request(url=o['src'], meta={'name': o['name'], 'referer': o['referer']})

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



