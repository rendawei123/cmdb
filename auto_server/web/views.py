import json
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from repository import models
from utils.page import Pagination
from .table_config import server as server_conf
from .service.server import ServerService
from .service.disk import DiskService

def server(request):
    return render(request,'server.html')

def server_json(request):
    service = ServerService(request)

    if request.method == "GET":
        response = service.fetch()
        return JsonResponse(response)

    elif request.method == "DELETE":
        response = service.delete()
        return JsonResponse(response)

    elif request.method == "PUT":
        response = service.save()
        return HttpResponse(json.dumps(response))



def disk(request):
    return render(request,'disk.html')

def disk_json(request):
    service = DiskService(request)

    if request.method == "GET":
        response = service.fetch()
        return HttpResponse(json.dumps(response))







def xxxxx(server_list):
    # [{},{}]
    for row in server_list:
        for item in models.Server.server_status_choices:
            if item[0] ==  row['server_status_id']:
                row['server_status_id_name'] = item[1]
                break
        yield row


def test(request):
    """
    赠送，模板语言显示choice
    :param request:
    :return:
    """
    # server_list = models.Server.objects.all()
    # for row in server_list:
    #     print(row.id,row.hostname,row.business_unit.name,"===",row.server_status_id,row.get_server_status_id_display() )

    # server_list = models.Server.objects.all().values('hostname','server_status_id')
    # for row in server_list:
    #     for item in models.Server.server_status_choices:
    #         if item[0] ==  row['server_status_id']:
    #             row['server_status_id_name'] = item[1]
    #             break

    data_list = models.Server.objects.all().values('hostname', 'server_status_id')

    return render(request,'test.html',{'server_list':xxxxx(data_list)})


def test_ajax(request):
    print(request.GET)
    return HttpResponse('...')