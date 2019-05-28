# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class GoodsItem(scrapy.Item):
    goods_id = scrapy.Field()
    name = scrapy.Field()
    img1 = scrapy.Field()

class GoodsList_id_name_img1_Item(scrapy.Item):
    '''
    商品基本列表 id,name,img1
    '''
    list = scrapy.Field()

class GoodsList_priceItem(scrapy.Item):
    '''
    价格列表
    '''
    list = scrapy.Field()

class GoodsList_comment_countItem(scrapy.Item):
    '''
    评论数量列表
    '''
    list = scrapy.Field()

class GoodsList_shop_idItem(scrapy.Item):
    '''
    商品店铺归属列表
    '''
    list = scrapy.Field()

class ImagesDownloadItem(scrapy.Item):
    '''
    下载图片元素
    '''
    name = scrapy.Field()
    src = scrapy.Field()  # 图片url地址
    referer = scrapy.Field()  # 来源