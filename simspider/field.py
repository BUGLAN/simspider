class BaseField:
    def __init__(self, css_select=None):
        self.css_select = css_select


class TextField(BaseField):
    def __init__(self, css_select=None):
        super().__init__(css_select=css_select)

    def extract(self, html):
        value = ''
        if self.css_select:
            value = html.cssselect(self.css_select)
        else:
            raise ValueError('{} field: css_select is expected'.format(
                self.__class__.__name__))
        text = ''
        for node in value[0].itertext():
            text += node.strip()
        value = text
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
                raise ValueError(
                    '{}: "{}" is not validable attribute'.format(
                        self.__class__.__name__, self.attr))
        else:
            raise ValueError('{} field: css_select is expected'.format(
                self.__class__.__name__))
        return value
