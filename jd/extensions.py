# -*- coding: utf-8 -*-
# Define here the models for your scraped Extensions

import time
import logging
import inspect
from scrapy import signals
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)

class SpiderIdleTimeoutExensions(object):
   '''
   TODO: 空闲超时扩展 / 控制scrapy空跑问题
   '''
   def __init__(self, idle_timeout, crawler):
      self.crawler = crawler

      # self.idle_timeout = crawler.settings.getint('IDLE_TIMEOUT')  # 空闲超时
      self.idle_timeout = idle_timeout  # 空闲超时

      self.idle_time_start = time.time()  # 空闲起始时间戳
      self.idle_timeA = time.time()  # 上一次调用spider_idle(*)触发时间点
      self.idle_timeB = time.time()  #  本次调用spider_idle(*)触发时间点
      self.idle_count = 0

   @classmethod
   def from_crawler(cls, crawler):
      # first check if the extension should be enabled and raise
      # NotConfigured otherwise


      if 'idle_timeout' in crawler.spidercls.__dict__.keys():
         # 爬虫里的数据成员变量 idle_timeout有优先权
         idle_timeout = crawler.spidercls.idle_timeout  # 爬虫里的数据
         # print('爬虫里的数据=', idle_timeout)
      else:
         # 爬虫没有定义 idle_timeout 则使用setting数据
         idle_timeout = crawler.settings.getint('IDLE_TIMEOUT', 0)  # 配置里的数据
         # print('配置里的数据=', idle_timeout)

      if idle_timeout < 6:
         # 参数无效
         raise NotConfigured  # 禁用扩展

      # if not 'redis_key' in crawler.spidercls.__dict__.keys():
      #     raise NotConfigured('Only supports RedisSpider')

      # instantiate the extension object
      # TODO：实例化扩展对象 把参数传给 def __init__(self, idle_timeout, crawler)
      ext = cls(idle_timeout, crawler)  # 把参数传给 def __init__(self, idle_timeout, crawler)

      # connect the extension object to signals
      # 将扩展对象连接到信号，如何： 将signals.spider_idle 与 spider_idle() 方法关联起来。
      crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
      crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
      crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)

      return ext

   def spider_opened(self, spider):
      # spider.logger.info("开始")
      pass

   def spider_closed(self, spider):
      # spider.logger.info("closed spider")
      pass

   def spider_idle(self, spider):
      # 程序启动的时候会调用这个方法一次，之后如果队列处于空闲状态时，每隔5秒就会再调用一次
      # print('now=>',self.__class__.__name__,inspect.stack()[0][3])
      idle_time = 0  # 总空闲时间
      self.idle_timeB = time.time()  # 本次调用时间戳
      AB = round(self.idle_timeB - self.idle_timeA)  # 时间间隔

      # 判断 当前触发时间与上次触发时间 之间的间隔是否大于5秒，如果大于5秒，说明 scrapy有活干，非空闲状态
      if AB > (5+1):  #  5是底线，+1 是宽限时间
         # 中间有活干，非空闲
         self.idle_start = time.time()
         self.idle_count = 0  # 重新计数
      else:
         # 空闲状态
         idle_time = int(time.time() - self.idle_time_start)

      if idle_time > self.idle_timeout:
         logger.info('空闲超时关闭scrapy')
         self.crawler.engine.close_spider(spider, __name__ + '=>空闲超时关闭scrapy')  # 执行关闭爬虫操作

      self.idle_timeA = time.time()  # 为下一次准备
      # print('时间=',self.idle_timeout)
      # print(spider.redis_key,'扩展idle_count=>', self.idle_count,'[',AB,'总=',idle_time)
      info = '空闲超时扩展=>timeout=%d,AB(巡逻间隔)=%d,总空闲=%d'%(self.idle_timeout, AB, idle_time)
      logger.info(info)

