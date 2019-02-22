from simspider import Item, TextField


class GitHub(Item):
    username = TextField(
        css_select=('#js-repo-pjax-container > div.pagehead.repohead.inst'
                    'apaper_ignore.readability-menu.experiment-r'
                    'epo-nav > div > h1 > span.author'))


def test_item():
    data = GitHub.get(url='https://github.com/BUGLAN/simspider')
    assert data == {'username': 'BUGLAN'}
