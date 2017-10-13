import elasticsearch

es = elasticsearch.Elasticsearch('http://localhost:9200/', sniff_on_start=True,
                                 sniff_on_connection_fail=True,
                                 sniffer_timeout=600)

class JianshuPipeline():

    @classmethod
    def item_handle(cls,item):
        es.index(index="jianshu", doc_type="ldap",
                 body={"title": item.title.get(), "content": item.content.get(), "url": item.url.get()})