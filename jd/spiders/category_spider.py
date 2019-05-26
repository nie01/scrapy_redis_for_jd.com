# -*- coding:utf-8 -*-

# import scrapy
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
# from jd.items import ImagesDownloadItem
from jd.items import CategoryListItem

class MySpider(RedisSpider):
    name = 'category_list'  # 蜘蛛名称
    # idle_timeout = 30  # 空闲超时，定义此数值值将会让setting里的参数失效。idle_timeout必须>5 否则空闲不受限制
    redis_key = 'jd:category_list_start_urls'
    # requests_key = 'jd:detail_requests'  # 队列的redis.key

    # 要接收的状态码（200默认接收），与setting中的 HTTPERROR_ALLOWED_CODES 相同功能相似
    # handle_httpstatus_list = [301, 302, 403, 404, 408, 500, 502, 503, 504, 522, 524]
    # handle_httpstatus_list = [403, 404, 408, 500, 502, 503, 504, 522, 524]

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

    # 测试状态码函数
    # def parse2(self, response):
    #     codes = ['301','302','403','404','500','502']
    #     for code in codes:
    #         url = 'http://www.abc.com/code.php?code='+code
    #         yield Request(url=url, callback=self.parse_detail, dont_filter=True)

    # 测试管道处理
    counting = 0
    def parse3(self, response):
        print('>>>>>>解析：',response.url)
        self.counting += 1
        for i in range(10):
            goods_item = CategoryListItem()
            goods_item['goods_id'] = 'id-%d_%d' % (self.counting, i)
            goods_item['name'] = 'name-%d_%d' % (self.counting, i)
            goods_item['img1'] = 'src-%d_%d' % (self.counting, i)
            print('添加item=>', goods_item['goods_id'])
            yield goods_item

        if self.counting < 5:
            for i in range(10):
                url = 'http://www.abc.com/code.php?code=200&c=%d&i=%d'%(self.counting,i)
                yield Request(url=url, callback=self.parse, dont_filter=True)
        else:
            print('/////////////////////////////////////////////////')


    def parse(self, response):
        url = response.url
        # print('parse解析函数url=', url)
        t = response.xpath('//title/text()').extract()[0]
        # print('标题：', t)
        # print('正文内容', response.text)

        # 解析列表
        list = response.xpath('//li[@class="gl-item"]')
        print('商品个数=',len(list))
        count = 0
        goods_list = []
        front_img_list = []

        for item in list:
            count += 1
            goods = {}
            t = item.xpath('.//div[@class="gl-i-wrap j-sku-item"]/@data-sku').extract()
            # goods['goods_id'] = t[0] if len(t) else None
            if len(t):
                goods['goods_id'] = t[0]
            else:
                continue

            t = item.xpath('.//img/@src').extract()
            if len(t):
                goods['img1'] = t[0]
            else:
                t = item.xpath('.//img/@data-lazy-img').extract()
                # goods['img1'] = t[0] if len(t) else None
                if len(t):
                    goods['img1'] = t[0]
                else:
                    continue

            if goods['img1']:
                goods['img1'] = response.urljoin(goods['img1'])

            t = item.xpath('.//div[@class="p-name"]//em//text()').extract()
            # goods['name'] = t[0].strip() if len(t) else None
            if len(t):
                goods['name'] = t[0].strip()
            else:
                continue

            # print(goods)

            # meta = {}
            # meta = {'requests_key': 'jd:img_requests'}
            # meta['referer'] = response.url
            # meta['name'] = goods['name']
            # meta['src'] = goods['img1']
            # yield Request(url=goods['img1'], callback=self.parse_img, headers={'Referer': meta['referer']}, meta=meta)

            goods_item = CategoryListItem()
            goods_item['goods_id'] = goods['goods_id']
            goods_item['name'] = goods['name']
            goods_item['img1'] = goods['img1']
            yield goods_item
            # break

            # imgItem = ImagesDownloadItem()
            # imgItem['referer'] = response.url
            # imgItem['name'] = goods['name']
            # imgItem['src'] = goods['img1']
            # yield imgItem

        # imgItem = ImagesDownloadItem()
        # imgItem['referer'] = url
        # imgItem['name'] = '百度logo'
        # imgItem['src'] = 'https://www.baidu.com/img/baidu_jgylogo3.gif'
        # yield imgItem

        # # url = 'https://www.xinli001.com/info/100388065'
        # # # url = 'http://www.abc.com/?n=1'
        # meta = {'requests_key': 'jd:detail_requests'}
        # # yield Request(url=url, callback=self.parse_detail, meta=meta)
        # url =  'https://www.baidu.com/img/baidu_jgylogo3.gif'
        # # url =  'https://www.abc.com/?t=2'
        # # yield Request(url=url, callback=self.parse_img)

    def parse_img(self, response):
        url = response.url
        print(response.meta)
        print('parse_img 解析函数url=', url)
        with open('b.gif','wb') as f:
            f.write(response.body)


    def parse_detail(self, response):
        url = response.url
        print(response.status, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', url, response.meta, response.text)
        # print('parse_detail解析函数url=', url)
        # 这里只是为了传递回调函数实例化，然后队列已交由 detail 爬虫处理
        pass