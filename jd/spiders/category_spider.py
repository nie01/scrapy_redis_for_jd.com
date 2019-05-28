# -*- coding:utf-8 -*-

import json
# import scrapy
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
# from jd.items import ImagesDownloadItem
from jd.items import GoodsItem
from jd.items import GoodsList_id_name_img1_Item
from jd.items import GoodsList_priceItem
from jd.items import GoodsList_comment_countItem
from jd.items import GoodsList_shop_idItem

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
            goods_item = GoodsItem()
            goods_item['GoodsList_id'] = 'id-%d_%d' % (self.counting, i)
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
        print('商品个数=', len(list))
        count = 0
        goods_list = []
        ids = []  # id数组
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
            goods_list.append(goods)
            ids.append(goods['goods_id'])

            # 下载封面图片
            # meta = {}
            # meta = {'requests_key': 'jd:img_requests'}
            # meta['referer'] = response.url
            # meta['name'] = goods['name']
            # meta['src'] = goods['img1']
            # yield Request(url=goods['img1'], callback=self.parse_img, headers={'Referer': meta['referer']}, meta=meta)

            # 提交单个商品入库
            # goods_item = CategoryListItem()
            # goods_item['goods_id'] = goods['goods_id']
            # goods_item['name'] = goods['name']
            # goods_item['img1'] = goods['img1']
            # yield goods_item
            # break

            # 使用图片管道下载封面图
            # imgItem = ImagesDownloadItem()
            # imgItem['referer'] = response.url
            # imgItem['name'] = goods['name']
            # imgItem['src'] = goods['img1']
            # yield imgItem

        # // for --------------------------------------


        #  数据传入管道
        list_item = GoodsList_id_name_img1_Item()
        list_item['list'] = goods_list
        yield list_item

        # print(goods_list)
        # print(goods_list.keys())
        # 制作 url 进行获取 价格，评论数据，所属店铺id
        idsA = '%2CJ_'.join(ids)
        idsB = ','.join(ids)
        price_url = 'https://p.3.cn/prices/mgets?callback=jQuery1437983&ext=11101100&pin=&type=1&area=1_72_4137_0&' \
                    'skuIds=%(ids)s&pdbp=0&pdtk=&pdpin=&pduid=15589488338381674727958&source=list_pc_front&_=1558950242108'%{'ids': idsA}  # 获取价格URL
        comment_url = 'https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds=%(ids)s&callback=jQuery1933531&_=1558948833411'%{'ids': idsB}  # 获取评论数量

        # 获取店铺id 必须有 'Referer': 'https://list.jd.com/list.html'  # 必须有
        shop_id_url = 'https://chat1.jd.com/api/checkChat?my=list&pidList=%(ids)s&callback=jQuery6698397&_=1558948833428'%{'ids': idsB}  # 获取店铺ID

        print(price_url)
        print(comment_url)
        print(shop_id_url)
        # meta = {'goods_list': goods_list}
        yield Request(url=price_url, callback=self.parse_price_jsonp, dont_filter=True)
        yield Request(url=comment_url, callback=self.parse_comment_jsonp, dont_filter=True)
        yield Request(url=shop_id_url, callback=self.parse_shop_id_jsonp, dont_filter=True)  # 默认传递当前url为referer

        '''
        获取价格
        https://p.3.cn/prices/mgets?callback=jQuery1437983&ext=11101100&pin=&type=1&area=1_72_4137_0&skuIds=J_100002928171%2CJ_100005114598%2CJ_100002892925%2CJ_100002928091%2CJ_100000769466%2CJ_5225346%2CJ_100004364088%2CJ_100004742560%2CJ_8461498%2CJ_100004668548%2CJ_100002368328%2CJ_100002942749%2CJ_7765111%2CJ_100000679465%2CJ_100000769432%2CJ_6076609%2CJ_100003671694%2CJ_100003052985%2CJ_100003052761%2CJ_6072622%2CJ_100005114580%2CJ_100003671692%2CJ_7629588%2CJ_100003092148%2CJ_100000612187%2CJ_100004270636%2CJ_6072614%2CJ_7649997%2CJ_100005322602%2CJ_7555189&pdbp=0&pdtk=&pdpin=&pduid=15589488338381674727958&source=list_pc_front&_=1558950242108

        *获取评论数量的数据
        https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds=100002928171,100005114598,100002892925,100002928091,100000769466,5225346,100004364088,100004742560,8461498,100004668548,100002368328,100002942749,7765111,100000679465,100000769432,6076609,100003671694,100003052985,100003052761,6072622,100005114580,100003671692,7629588,100003092148,100000612187,100004270636,6072614,7649997,100005322602,7555189&callback=jQuery1933531&_=1558948833411

        *获取店铺信息
        必须    
        # headers_chrome_win10['Referer'] = 'https://list.jd.com/list.html?cat=670%2C671%2C672&go=0'  # 必须有
        headers_chrome_win10['Referer'] = 'https://list.jd.com/list.html'  # 必须有
        https://chat1.jd.com/api/checkChat?my=list&pidList=100002928171,100005114598,100002892925,100002928091,100000769466,5225346,100004364088,100004742560,8461498,100004668548,100002368328,100002942749,7765111,100000679465,100000769432,6076609,100003671694,100003052985,100003052761,6072622,100005114580,100003671692,7629588,100003092148,100000612187,100004270636,6072614,7649997,100005322602,7555189&callback=jQuery6698397&_=1558948833428

        '''
    def parse_price_jsonp(self, response):
        '''
        价格的jsonp
        :param response:
        :return:
        '''
        # print(response.meta)
        jsonp = response.text
        # goods_list = response.meta.get('goods_list')
        # 提取回调函数中的json部分的字符串
        A = jsonp.find('(')
        if(A==-1 or A>20):
            return

        B = jsonp.rfind(')')
        jsonStr = jsonp[A+1:B]
        jsonObj = json.loads(jsonStr)
        # print(jsonObj)
        '''
            {
                "cbf": "0",
                "id": "J_100000769466",
                "m": "10999.00",
                "op": "5999.00",  // 原价
                "p": "5299.00"  // 折后价
                },
        '''
        price_list = []
        for one in jsonObj:
            price = {}
            price['goods_id'] = one['id'][2:]  # 去掉 J_
            price['o_price'] = one['op']  # 原价
            price['price'] = one['p']  # 折后价
            price_list.append(price)

        print(len(jsonObj),'价格=>', price_list)
        listItem = GoodsList_priceItem()
        listItem['list'] = price_list
        yield listItem

    def parse_comment_jsonp(self, response):
        '''
        评论数量的jsonp
        :param response:
        :return:
        '''
        jsonp = response.text
        # 提取回调函数中的json部分的字符串
        A = jsonp.find('(')
        if(A==-1 or A>20):
            return

        B = jsonp.rfind(')')
        jsonStr = jsonp[A+1:B]
        jsonObj = json.loads(jsonStr)
        # print(jsonObj)
        '''{
            AfterCount: 2900
            AfterCountStr: "2900+"
            AverageScore: 5
            CommentCount: 240000
            CommentCountStr: "24万+"
            DefaultGoodCount: 170000
            DefaultGoodCountStr: "17万+"
            GeneralCount: 1500
            GeneralCountStr: "1500+"
            GeneralRate: 0.008
            GeneralRateShow: 1
            GeneralRateStyle: 1
            GoodCount: 180000
            GoodCountStr: "18万+"
            GoodRate: 0.98
            GoodRateShow: 98
            GoodRateStyle: 147
            OneYear: 0
            PoorCount: 2100
            PoorCountStr: "2100+"
            PoorRate: 0.012
            PoorRateShow: 1
            PoorRateStyle: 2
            ProductId: 100002928171
            SensitiveBook: 0
            ShowCount: 19000
            ShowCountStr: "1.9万+"
            SkuId: 100002928171
            VideoCount: 3600
            VideoCountStr: "3600+"
        }
        '''
        comment_list = []
        for one in jsonObj['CommentsCount']:
            comment = {}
            comment['goods_id'] = one['ProductId']
            comment['comment_count'] = one['CommentCount']  # 评论数量
            comment_list.append(comment)

        print(len(jsonObj['CommentsCount']), '评论数量=>', comment_list)
        listItem = GoodsList_comment_countItem()
        listItem['list'] = comment_list
        yield listItem

    def parse_shop_id_jsonp(self, response):
        '''
        店铺归属的jsonp
        :param response:
        :return:
        '''
        # print(response.meta)
        jsonp = response.text
        # goods_list = response.meta.get('goods_list')
        # 提取回调函数中的json部分的字符串
        A = jsonp.find('(')
        if (A == -1 or A > 20):
            return

        B = jsonp.rfind(')')
        jsonStr = jsonp[A + 1:B]
        jsonObj = json.loads(jsonStr)
        # print(jsonObj)
        '''
        {
            chatDomain: "chat.jd.com"
            chatUrl: "https://chat.jd.com/index.action?_t=&pid=100004668548"
            code: 1
            pid: 100004668548
            rank3: 672
            seller: "荣耀京东自营旗舰店"
            shopId: 1000000904
            venderId: 1000000904
        }
        '''
        shop_list = []
        for one in jsonObj:
            shop = {}
            shop['goods_id'] = one['pid']
            shop['shop_id'] = one['shopId']  # 店铺id
            shop['shop_name'] = one['seller']  # 店铺名称
            shop_list.append(shop)

        print(len(jsonObj),'店铺归属=>', shop_list)
        listItem = GoodsList_shop_idItem()
        listItem['list'] = shop_list
        yield listItem


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