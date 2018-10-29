# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import urllib
from PIL import Image
from douban.items import DoubanItem
class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['douban.com']
    start_urls = ['https://accounts.douban.com/login']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    item = DoubanItem()
    def start_requests(self):
        url = self.start_urls[0]
        yield Request(url = url,headers=self.headers, callback=self.parse_before_login)
    def parse_before_login(self,response):
        print("登陆前表单填充")

        captcha_id = response.xpath('//*[@id="lzform"]/div[6]/div/div/input[2]/@value').extract()
        captcha_image_url = response.xpath('//*[@id="captcha_image"]/@src').extract()
        print(type(captcha_image_url))
        print(captcha_image_url)
        print(captcha_id)
        print(None)
        if captcha_image_url is captcha_image_url:
            print("登录时无验证码")
            formdata = {
                "source":"index_nva",
                "form_email":"1033808656@qq.com",
                "form_password":"lxs1995104."
            }
            return scrapy.FormRequest.from_response(response, headers=self.headers, formdata=formdata,
                                                    callback=self.parse_after_login)

        else:
            print("登陆时有验证码")
            save_image_path = 'D:\python_project\douban\captcha.jpeg'
            urllib.request.urlretrieve(captcha_image_url[0],save_image_path)
            try:
                im = Image.open('D:\python_project\douban\captcha.jpeg')
                im.show()
            except:
                pass
            #手动输入验证码
            captcha_solution = input('按照打开的图片输入验证码:')
            formdata = {
                'source':'None',
                'redir':'https://www.douban.com',
                'form_email':'1033808656@qq.com',
                'form_password':'lxs1995104.',
                'captcha-solution':captcha_solution,
                'captcha-id':captcha_id,
                'login':'登陆'
            }
            print('loadding........')

            return scrapy.FormRequest.from_response(response, headers=self.headers, formdata=formdata, callback=self.parse_after_login)


    def parse_after_login(self,response):
        account = response.xpath('//a[@class="bn-more"]/span/text()').extract_first()
        if account is None:
            print("登录失败")
        else:
            print(u"登录成功,当前账户为 %s" % account)
        ids = [i*20 for i in range(0,28)]
        for id in ids:
            url = 'http://movie.douban.com/subject/26322774/reviews'+'?start={}'.format(id)
            print(url)
            yield Request(url=url,headers=self.headers,callback=self.parse,dont_filter=False)
    def parse(self, response):
        print(response.url)
        ids = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div/@data-cid').extract()
        #print(ids)
        for id in ids:
            url = 'https://movie.douban.com/review/'+id+'/'
            print(url)
            yield Request(url=url,headers=self.headers,method="GET",callback=self.parse_page,dont_filter=False)

    def parse_page(self,response):
        print(response.url)
        print(response.status)
        comments = response.xpath('//*[@id="link-report"]/div[1]/text()').extract()
        print(comments)
        self.item['comment'] = comments
        with open('a.txt','a+') as f:
            for file in self.item['comment']:
                f.write(file)
            f.close()