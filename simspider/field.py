import re

from lxml import etree


class BaseField:
    def __init__(self, css_select=None, xpath_select=None, default=None):
        self.css_select = css_select
        self.xpath_select = xpath_select
        self.default = default


class TextField(BaseField):
    def __init__(self,
                 css_select=None,
                 xpath_select=None,
                 re_select=None,
                 default=None):
        super().__init__(css_select, xpath_select, default)
        self.re_select = re_select

    def _parse_from_css_or_xpath(self, value):
        if len(value) == 0:
            return None
        elif len(value) == 1:
            text = ''
            for node in value[0].itertext():
                text += node.strip()
            value = text
        if not value and self.default:
            value = self.default
        return value

    def extract(self, html):
        value = ''
        if self.css_select:
            value = html.cssselect(self.css_select)
        elif self.xpath_select:
            value = html.xpath(self.xpath_select)
        elif self.re_select:
            real_html = etree.tostring(html, encoding='unicode', method='html')
            compiler = re.compile(self.re_select)
            items = compiler.findall(real_html)
            if len(items) == 0:
                return None
            elif len(items) == 1:
                return items[0]
            return items
        else:
            raise ValueError('{} field: css_select is expected'.format(
                self.__class__.__name__))
        if len(value) == 0:
            return None
        elif len(value) == 1:
            text = ''
            for node in value[0].itertext():
                text += node.strip()
            value = text
        else:
            for index, item in enumerate(value[:]):
                text = ''
                for node in item.itertext():
                    text += node.strip()
                value[index] = text
        return value


class AttrField(BaseField):
    def __init__(self, attr, css_select=None):
        super().__init__(css_select=css_select)
        self.attr = attr

    def extract(self, html):
        value = ''
        if self.css_select:
            value = html.cssselect(self.css_select)
            value = value[0].get(self.attr, None) if len(value) == 1 else value
            if not value:
                raise ValueError('{}: "{}" is not validable attribute'.format(
                    self.__class__.__name__, self.attr))
        else:
            raise ValueError('{} field: css_select is expected'.format(
                self.__class__.__name__))
        return value


class Attribute(BaseField):
    def __init__(self, css_select=None, xpath_select=None, default=None):
        super().__init__(css_select, xpath_select, default)
