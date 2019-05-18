# -*- coding:utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import redis

def add_start_url(redis_key, urls):
    '''
    添加起始位置到redis数据库
    :param redis_key:
    :param urls:
    :return:
    '''
    pool = redis.ConnectionPool(host='127.0.0.1',port=6379,db=0,password='abc+ABC+123+root')
    red = redis.Redis(connection_pool=pool)
    if 'str' == type(urls).__name__:
        red.lpush(redis_key,urls)
    elif 'list' == type(urls).__name__:
        for url in urls:
            red.lpush(redis_key,url)



if __name__ == '__main__':
    urls = ['http://www.abc.com','https://www.xinli001.com/info/100388065']
    add_start_url(redis_key='category_list:start_urls', urls=urls)
    # exit()
    process = CrawlerProcess(get_project_settings())
    process.crawl('category_list')
    process.start()


