from elasticsearch_dsl import DocType, Keyword, Text
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'])

class Jianshu(DocType):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    content = Text(analyzer='snowball')
    url = Keyword()


    class Meta:
        index = 'jianshu'


if __name__ == '__main__':
    Jianshu.init()