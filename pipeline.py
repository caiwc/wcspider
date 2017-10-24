from elasticsearch_dsl.connections import connections
from es_model import Jianshu

connections.create_connection(hosts=['localhost'])


class JianshuPipeline():

    @classmethod
    def item_handle(cls,item):
        js = Jianshu(title=item.title.get(),content=item.content.get(),url=item.url.get())
        js.save()