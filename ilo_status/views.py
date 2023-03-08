from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, resolve_url


def index(request):
    return render(request, 'index.html')


def test(request):
    if request.method == 'POST':
        # 从请求数据中获取server_name的值
        server_name = request.POST.get('server_name')
        print(server_name)

        # 返回一个JSON响应，告诉客户端请求成功，并提供一些信息
        data = {'status': 'success', 'message': 'The server name is ' + server_name}
        return JsonResponse(data)

    # 如果请求方法不是POST，则返回一个空白的响应
    return JsonResponse({})

