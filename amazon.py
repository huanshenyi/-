import requests
from lxml import etree

#ある本の各販売店舗urlを取得
def geturls(sn):

    url ='https://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Dstripbooks&field-keywords={sn}'.format(sn=sn)

    html_data = requests.get(url).text
    book_list = etree.HTML(html_data)
    list = book_list.xpath("//div[@id='atfResults']//a[@class='a-size-small a-link-normal a-text-normal']/@href")
    second_url = list[0]
    syousai = requests.get(second_url).text
    book_list2 = etree.HTML(syousai)
    books = book_list2.xpath("//div[@class='a-row a-spacing-mini olpOffer']")
    for book in books:
        #値段
        prices = (book.xpath(".//span[@class='a-size-large a-color-price olpOfferPrice a-text-bold']/text()"))[0].strip().replace("￥ ", "").replace(",", "")
        print(prices)
        #送料
        postage = (book.xpath(".//span[@class='olpShippingPrice']/text()"))
        postages=('送料無料'if postage == [] else postage[0].replace("￥ ", ""))
        print(postages)
        #状態
        conditions = book.xpath(".//div[@class='collapsedNote']/text()")
        condition=('新品' if conditions == [] else conditions[0]).strip()
        print(condition)
        #出品者
        #stores=



if __name__ == "__main__":
    #bookcodeを取得
    BOOKCODE = input("探したい本のIDを入力してください:")
    bookurl = geturls(BOOKCODE)


