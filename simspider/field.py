class BaseField:
    def __init__(self, css_select=None):
        self.css_select = css_select


class TextField(BaseField):

    def __init__(self, css_select=None):
        super(TextField, self).__init__(css_select)

    def extract_value(self, html):
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
