from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, resolve_url
from ilo_status.script import get_ilo_status


def index(request):
    return render(request, 'index.html')


def test(request):
    if request.method == 'POST':
        # 从请求数据中获取server_name的值
        server_ip = request.POST.get('server_ip')

        host_status_data = get_ilo_status.get_ilo_status(server_ip)

        if host_status_data:
            # 返回一个JSON响应，告诉客户端请求成功，并提供一些信息
            data = {'status': True, 'data': host_status_data}
        else:
            data = {'status': False, 'error': 'No data found for ' + server_ip}

        return JsonResponse(data)

