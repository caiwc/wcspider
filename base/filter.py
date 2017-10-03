class BaseFilter(object):
    def __init__(self):
        self.seen_url = set()

    def add(self,url):
        if url not in self.seen_url:
            self.seen_url.add(url)
            return True
        else:
            return False