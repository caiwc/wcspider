from elasticsearch_dsl import DocType, Keyword, Text,Date,Integer
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.faceted_search import FacetedSearch,TermsFacet

connections.create_connection(hosts=['localhost'])

class Jianshu(DocType):
    title = Text(analyzer='ik_max_word', fields={'raw': Keyword()},)
    content = Text(analyzer='ik_max_word')
    url = Keyword()
    like = Integer()
    view = Integer()
    comment = Integer()
    wordage = Integer()
    ctime = Date()


    class Meta:
        index = 'jianshu2',
        doc_type = 'article2'


class JianshuSearch(FacetedSearch):
    doc_types = ['jianshu','python']
    fields = ['title','content']


if __name__ == '__main__':
    Jianshu.init()

    # jss = JianshuSearch("python")
    # s = jss.build_search()
    # response = s.execute()
    # for hit in response:
    #     print(hit.meta.score, hit.title)
