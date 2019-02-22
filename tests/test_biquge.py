from simspider import Item, TextField


class BiquegeItem(Item):
    chapters = TextField(css_select='#list > dl > dd > a')
    title = TextField(css_select='#info > h1')

    def _title(self, title):
        return 'this is ' + title


def test_biquge():
    datas = BiquegeItem.get(url='https://www.biquge5200.cc/75_75584/')
    assert len(datas) is not None
    assert 'this is' in datas['title']
    assert len(datas['chapters']) > 1
