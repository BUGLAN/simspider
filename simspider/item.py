import requests
from lxml import etree

from .field import BaseField


class ItemMeta(type):
    """ItemMeta metaclass"""

    def __new__(cls, name, bases, attrs):
        _fields = {
            field_name: attrs.pop(field_name)
            for field_name, obj in list(attrs.items())
            if isinstance(obj, BaseField)
        }

        attrs['_fields'] = _fields
        return type.__new__(cls, name, bases, attrs)


class Item(metaclass=ItemMeta):
    def __init__(self, html):
        if html is None or not isinstance(html, etree._Element):
            raise ValueError('etree._Element is expected')
        for field_name, field_value in self._fields.items():
            get_field = getattr(self, '_{}'.format(field_name), None)
            value = field_value.extract(html) if isinstance(
                field_value, BaseField) else field_value
            if get_field:
                value = get_field(value)
            setattr(self, field_name, value)

    @classmethod
    def _get_html(cls, html, url, **kwargs):
        if html:
            html = etree.HTML(html)
        elif url:
            # set requests random headers
            response = requests.get(url, **kwargs)
            text = response.content
            html = etree.HTML(text)
        else:
            raise ValueError('(url or html) is expected')
        return html

    @classmethod
    def get(cls, html='', url='', **kwargs):
        html = cls._get_html(html, url, **kwargs)
        item = {}
        ins_item = cls(html=html)
        for field_name in cls._fields.keys():
            item[field_name] = getattr(ins_item, field_name)
        return item
