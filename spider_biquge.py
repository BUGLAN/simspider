from pprint import pprint

from simspider import Item, Request, Spider, TextField

a = 0


class BiquegeItem(Item):
    title = TextField(
        css_select='#wrapper > div.content_read > div > div.bookname > h1')
    content = TextField(css_select='#content')


class BiquegeSpider(Spider):
    start_urls = ['https://www.biquge5200.cc/75_75584/']

    def parse(self, res):
        # 将html转化为etree
        etree = self.e_html(res.html)
        pages = [i.get('href') for i in etree.cssselect('#list > dl > dd > a')]
        for page in pages:
            yield Request(url=page, callback=self.parse_item)

    def parse_item(self, res):
        with open('a.txt', 'a+') as f:
            f.write(res.html)


if __name__ == "__main__":
    BiquegeSpider.start()
