from elasticsearch_dsl.connections import connections
from es_model import Jianshu

connections.create_connection(hosts=['localhost'])


class JianshuPipeline():
    @classmethod
    def item_handle(cls, item):
        try:
            js = Jianshu(title=item.title.get(), content=item.content.get(), url=item.url.get(), ctime=item.ctime.get(),
                         like=item.like.get(),wordage=item.view.get(),
                         view=item.view.get(), comment=item.comment.get())
            js.save()
            print("save a item:{}".format(item.title.get()))
        except Exception as e:
            print(str(e))
