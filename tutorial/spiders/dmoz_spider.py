from scrapy.spider import Spider
from scrapy.selector import Selector
import os, re
import random
import urllib.request
from db.mongodb import mongodb


class DmozSpider(Spider):
    name = "juejin"
    allowed_domains = ["juejin.im"]
    start_urls = [
        "https://juejin.im/zhuanlan/frontend"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)
        sel = Selector(response)
        sites = sel.xpath('//ul/li[@class="item"]')
        saveFile = open("e:\\temp\img\\save.txt", 'w', encoding="utf8")
        articles = mongodb.initCollection('articles')
        for site in sites:
            title = site.xpath('div/div/a[@class="title"]/text()').extract()
            link = site.xpath('div/div/a[@class="title"]/@href').extract()
            desc = site.xpath('div/div/a[contains(@class,"abstract")]/text()').extract()
            if len(title) > 0:
                saveFile.write(self.allowed_domains[0] +"----"+ title[0] + " +++ " + link[0] + " +++ " + desc[0] + "\n")
                articles.insert({"columnid": "BJcTbyZoW", "brief": desc[0], "title": title[0], "link": "http://"+self.allowed_domains[0]+link[0]})
        saveFile.close()


class ImgSpider(Spider):
    name = "img"
    allowed_domains = ["th7.cn"]
    start_urls = [
        "http://www.xiaohuar.com/list-1-1.html"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)
        sel = Selector(response)
        sites = sel.xpath('//img')
        for site in sites:
            src = site.xpath('@src').extract()
            alt = site.xpath('@alt').extract()
            if src:

                imgUrl = "http://www.xiaohuar.com/" + src[0]
                if imgUrl.rfind("http://") == 0:
                    img_path = os.path.join("E:/temp/img", str(random.randint(100, 999)) + ".jpg")
                    urllib.request.urlretrieve(imgUrl, filename=img_path)

            print(site)
            print(src)
            print(alt)
            print("  ")
