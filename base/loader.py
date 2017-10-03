from bs4 import BeautifulSoup


class ItemLoader(object):
    def __init__(self, item, html, parser='html.parser'):
        self.soup = BeautifulSoup(html, parser)
        self.item = item

    def get_item(self, name):
        try:
            item = getattr(self.item, name)
        except:
            raise ValueError
        return item

    def add_soup(self, name, data, default=None):
        item = self.get_item(name)
        if data:
            item.set(data)
        else:
            item.set(default)


