from pprint import pprint

from simspider import Item, TextField, AttrField


class BiqugeSpider(Item):
    """Biquge spider"""
    title = TextField(css_select='#info > h1')
    info = TextField(css_select='#intro')
    cover = AttrField(css_select='#fmimg > img', attr='sr')

    def _title(self, title):
        return title


if __name__ == "__main__":
    data = BiqugeSpider.get_item(url='https://www.biquge5200.cc/75_75584/')
    data2 = BiqugeSpider.get_item(url='https://www.biquge5200.cc/86_86700/')
    pprint(data)
    pprint(data2)
