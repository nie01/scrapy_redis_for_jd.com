# -*- coding: utf-8 -*-

# Scrapy settings for jd project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'jd'

SPIDER_MODULES = ['jd.spiders']
NEWSPIDER_MODULE = 'jd.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jd (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False    # 设置是否遵守reboots协议 开关

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'jd.middlewares.JdSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'jd.middlewares.JdDownloaderMiddleware': 543,
   # 'jd.middlewares.UserAgentMiddleware':300, # 300是必须， (动态)修改User-Agent 下载中间件
   'jd.middlewares.ProxyMiddleware': 543,  # (动态)修改代理IP下载中间件
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'jd.pipelines.JdPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'



# scrapy-redis 配置 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  自定义改造部分 配置

# redis 数据库参数
# REDIS_HOST = '127.0.0.1'  # redis地址
# REDIS_HOST = 6379  #
# REDIS_PARAMS = {'password': 'abc+ABC+123+root',
#                 'db': 0  # 哪个？数据库
# }

# 过滤器的redis_key 的优先级： Request参数meta['queue_key'] > settings中的QUEUQ_PUBLIC_KEY > 默认的key
DUPEFILTER_PUBLIC_KEY = 'jd:public_dupefilter'  # 公共过滤器的redis_key

# scrapy-redis 配置 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 1.(*必须加*)。使用scrapy_redis.duperfilter.REPDupeFilter的去重组件，在redis数据库里做去重。
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 2.（*必须加*）。使用了scrapy_redis的调度器，在redis里面分配请求。
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 3.（*必须加*）。在redis queues 允许暂停和暂停后恢复，也就是不清理redis queues
SCHEDULER_PERSIST = True

# 4.管道（*必须加*）。通过RedisPipeline将item写入key为 spider.name: items的redis的list中，供后面的分布式处理item。
ITEM_PIPELINES = {
   'scrapy_redis.pipelines.RedisPipeline': 100,  # scrapy-redis的（*必须加*）
    'jd.pipelines.ImagesDownloadPipeline': 300  # 下载图片管道
    # 格式为：'项目名.文件名.类名'：优先级（越小越大）
   # 'jd.pipelines.jd_category_list_pipelines':300,
   # 'jd.pipelines.jd_detail':300,
}






#  以下是自定义  -——————————————————————————————————————————————————————————

# 日志设置
# LOG_LEVEL = 'INFO'
LOG_LEVEL = 'WARNING'
# LOG_FILE = 'spider.log'
# LOG_ENABLE = False  # 显示日志 开关

# 下载速度控制
CONCURRENT_REQUESTS = 1  # 线程数量 / 也是每次从redis读取url的数量
DOWNLOAD_DELAY = 2  # 下载器在同一个网站下一个页面前需要等待的时间

COOKIES_ENABLED = False  # cookies开关

# 设置http请求头信息 固定的，需要随机改变的话 在中间件里添加  'caiji.middlewares.UserAgentMiddleware': 300,  # 300是必须 随机更换 User-Agent
#  模拟 谷歌的请求头
DEFAULT_REQUEST_HEADERS = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
   'Accept-Encoding': 'gzip, deflate',
   'Accept-Language': 'zh-CN,zh;q=0.9',
   'Cache-Control': 'max-age=0',
   'Connection': 'keep-alive',
   'DNT': '1',
   # 'Upgrade-Insecure-Requests': '1',
}

# 保存图片的目录路径
IMAGES_STORE = 'imgs'




# 扩展——————————————

# IDLE_EXT_ENABLED = True  # 控制开关@空闲超时扩展
# 空闲超时扩展 / 控制scrapy空跑问题  IDLE_TIMEOUT 必须>5 否则空闲不受限制
IDLE_TIMEOUT = 15  # 空闲超时/允许的空闲时长(单位：秒，整数)IDLE_TIMEOUT必须大于5否则无效 ，超时后scrapy将关闭

# 扩展Enable or disable extensions
EXTENSIONS = {
   'jd.extensions.SpiderIdleTimeoutExensions': 500,  # 空闲超时扩展 / 控制scrapy空跑问题
}




