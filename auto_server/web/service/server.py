import json
from repository import models
from utils.page import Pagination
from ..table_config import server as server_conf
from .base import BaseService


class ServerService(BaseService):

    def __init__(self,request):
        self.request = request
        self.table_config = server_conf.table_config
        self.search_config = server_conf.search_config

    def fetch(self):

        current_page = self.request.GET.get('pageNum')
        total_item_count = models.Server.objects.filter(self.condition()).count()

        page_obj = Pagination(current_page, total_item_count, per_page_count=2)

        server_list = models.Server.objects.filter(self.condition()).values(*self.values())[page_obj.start:page_obj.end]

        response = {
            'search_config': server_conf.search_config,
            'data_list': list(server_list),
            'table_config': server_conf.table_config,
            'global_choices_dict': {
                'status_choices': models.Server.server_status_choices
            },
            'page_html': page_obj.page_html_js()
        }
        return response

    def delete(self):
        id_list = json.loads(self.request.body.decode('utf-8'))
        # str(request.body,encoding='utf-8')
        # bytes(v,encoding='utf-8')

        # models.Server.objects.filter(id__in=id_list).delete()
        # for nid in id_list:
        #     try:
        #         models.Server.objects.filter(id=nid).delete()
        #     except Exception as e:
        #         pass
        response = {'status': True, 'msg': None}
        try:
            # models.Server.objects.filter(id__in=id_list).delete()
            pass
        except Exception as e:
            response['status'] = False
            response['msg'] = str(e)

        return response

    def save(self):
        response = {'status': True, 'msg': None}

        update_list = json.loads(self.request.body.decode('utf-8'))
        for row in update_list:
            # {'nid':1, 'hostname': 'c1.com'},
            nid = row.pop('nid')
            models.Server.objects.filter(id=nid).update(**row)

        return response