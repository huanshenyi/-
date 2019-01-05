from lxml import html
from lxml import etree
from typing import NamedTuple

import requests

HEADERS = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}
class BootEntity(NamedTuple):
    """ 本のデータ"""
    title: str
    price: float
    link: str
    store: str
    def __str__(self):
        return "値段:{self.price} ;タイトル:{self.title} ; リンク:{self.link} ; 店舗:{self.store}".format(self=self)

class MySpider(object):

    def __init__(self, sn):
        self.sn = sn
        """全ての書籍データを保存"""
        self.book_list = []

    def dangdang(self):
        """dangdangデータ"""
        url = "http://search.dangdang.com/?key={sn}&act=input".format(sn=self.sn)
        html_data = requests.get(url).text
        # etree.HTML
        selector = html.fromstring(html_data)
        ul_list = selector.xpath('//div[@id="search_nature_rg"]/ul/li')

        for li in ul_list:
            title = li.xpath('a/@title')
            print(title[0].strip())
            link = li.xpath('a/@href')
            print(link[0])
            price = li.xpath("p[@class='price']/span[@class='search_now_price']/text()")
            print(price[0].replace("¥", ""))
            store = li.xpath("p[@class='search_shangjia']/a/text()")
            store = ('自営店舗' if store == [] else store[0])
            print(store)
            book = BootEntity(
                title=title[0],
                price=price[0].replace("¥", ""),
                link=link[0],
                store=store
            )
            print(book)
            self.book_list.append(book)

    def jd(self):
        url = "http://search.jd.com/Search?keyword={sn}".format(sn=self.sn)
        html_doc = requests.get(url, headers=HEADERS).content.decode("utf-8")
        selector = etree.HTML(html_doc)
        ul_list = selector.xpath("//div[@id='J_goodsList']/ul/li")
        for li in ul_list:
            title = li.xpath("div/div[@class='p-name']/a/@title")
            print(title[0])
            link = li.xpath("div/div[@class='p-name']/a/@href")
            print(link[0])
            price = li.xpath('div/div[@class="p-price"]/strong/i/text()')
            print(price[0])
            # store=li.xpath("div/div[@class='p-shopnum']/a/@title")
            store = li.xpath("div//a[@class='curr-shop']/@title")
            print('自営店舗' if store == [] else store[0])
            book = BootEntity(
                title=title[0],
                price=price[0],
                link='https:' + link[0],
                store=store
            )
            self.book_list.append(book)

    def yhd(self):
        return []

    def taobao(self):
        return []

    def spider(self):
        """並び替え"""
        self.dangdang()
        self.jd()

        book_list = sorted(self.book_list, key=lambda item: float(item.price), reverse=True)
        for book in book_list:
            print(book)

if __name__ == '__main__':
    client = MySpider("9787115428028")
    client.spider()