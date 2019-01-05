from lxml import etree
from typing import NamedTuple

import requests
#9784873117782
#4873117380
class BootEntity(NamedTuple):
    """ 本のデータ"""
    price: int
    postage: int
    link: str
    store: str
    condition: str
    def __str__(self):
        return "値段:{self.price} ;送料:{self.postage} ; 状態:{self.condition}; リンク:{self.link} ; 店舗:{self.store}".format(self=self)

class MySpider(object):

    def __init__(self, sn):
        self.sn = sn
        """全ての書籍データを保存"""
        self.book_list = []

    def amazon(self):
        url = 'https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Dstripbooks&field-keywords={sn}'.format(sn=self.sn)

        html_data = requests.get(url).text
        book_list = etree.HTML(html_data)
        list = book_list.xpath("//div[@id='atfResults']//a[@class='a-size-small a-link-normal a-text-normal']/@href")
        """本のタイトルを表示する"""
        main_title = book_list.xpath( "//div[@class='a-row a-spacing-none']/a[@class='a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal']/@title")
        print(main_title)
        second_url = list[0]
        syousai = requests.get(second_url).text
        book_list2 = etree.HTML(syousai)
        books = book_list2.xpath("//div[@class='a-row a-spacing-mini olpOffer']")
        for book in books:
            # 値段
            prices = (book.xpath(".//span[@class='a-size-large a-color-price olpOfferPrice a-text-bold']/text()"))[
                0].strip().replace("￥ ", "").replace(",", "")
            #print(prices)
            # 送料
            postage = (book.xpath(".//span[@class='olpShippingPrice']/text()"))
            postages = ('送料無料' if postage == [] else postage[0].replace("￥ ", ""))
            #print(postages)
            # 状態
            conditions = book.xpath(".//div[@class='collapsedNote']/text()")
            condition = ('新品' if conditions == [] else conditions[0]).strip()
            #print(condition)
            # 出品者
            stores = book.xpath(".//span[@class='a-size-medium a-text-bold']/a/text()")
            #print(stores)
            store = ('Amazon' if stores == [] else stores[0])
            # 連絡先link リストする前にこのurlheaderと合併
            urlheader = "https://www.amazon.co.jp"
            links = book.xpath(".//span[@class='a-size-medium a-text-bold']/a/@href")
            link = ("Amazon" if links == [] else links[0])
            #print(links)
            book = BootEntity(
                price=prices,
                postage=postages,
                condition=condition,
                link=urlheader+link,
                store=store
            )
            #print(book)
            self.book_list.append(book)


    def rakuten(self):
        book_lists = []
        url = "https://search.rakuten.co.jp/search/mall/{sn}/?l-id=s_search&l2-id=shop_header_search".format(sn=self.sn)
        respons = requests.get(url).text
        html = etree.HTML(respons)
        shop_urls = html.xpath("//div[@class='dui-cards searchresultitems']//div[@class='extra content']/a/@href")
        shop_url = shop_urls[0]
        #print(shop_url)
        books = requests.get(shop_url).text
        booklist_html = etree.HTML(books)
        booklists = booklist_html.xpath("//div[@id='quickViewScope']/table//tr[@valign='top']")
        #print(len(booklists))
        for  book in booklists:
            """値段"""
            prices = book.xpath(".//span[@class='UsedTxet01 itemPrice3']/text()")

            for pe in prices:
                price = pe.replace(",", "")
            """送料"""
            postages = book.xpath(".//span[@class='shipfree']/text()")

            for po in postages:
                postage = po
            """店舗"""
            stores = book.xpath(".//div[@class='shop_link']/a/text()")
            """リンク"""
            links = book.xpath(".//div[@class='shop_link']/a/@href")

            """状態"""
            conditions = book.xpath(".//td[@style='font-size:80%;']/text()")
            condition = ("新品" if conditions == [] else conditions[0])

            for p, po, s, l, c in zip(prices, postages, stores, links, condition):
                price = p.replace(",", "")
                postage = po
                store = s
                link = l
                condition = c

                book = BootEntity(
                    price=price,
                    postage=postage,
                    condition=condition+"品",
                    link=link,
                    store=store
                )
                #print(book)
                self.book_list.append(book)

    def spider(self):
       self.rakuten()
       self.amazon()
       book_list = sorted(self.book_list, key=lambda item: float(item.price), reverse=True)
       for book in book_list:
           print(book)

if __name__ == "__main__":
    sn = input("探したい本のISBNコードを入力してください:")
    client = MySpider(sn)
    client.spider()