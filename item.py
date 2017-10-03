from base.model import Field,Item

class TestItem(Item):
    name = Field()
    num = Field()
    url = Field()


class JianshuItem(Item):
    title = Field()
    content = Field()