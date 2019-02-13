from pprint import pprint

from simspider import Item, TextField


class BiqugeSpider(Item):
    """Biquge spider"""
    title = TextField(css_select='#info > h1')

    def _title(self, title):
        return title


if __name__ == "__main__":
    data = BiqugeSpider.get_item(url='https://www.biquge5200.cc/75_75584/')
    pprint(data)
