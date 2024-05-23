
from rest_framework.response import Response

def is_client_permission(function):
    def wrapper(self,request,*args, **kwargs):
        print(request.user.username)
        print(request.user.is_client)
        if request.user.is_client:
            return function(self,request, *args, **kwargs)
        return Response({"status": "Sizda huquq yo'q "})
    return wrapper


def is_trade_permission(function):
    def wrapper(self,request,*args, **kwargs):
        if request.user.is_trade:
            return function(self,request, *args, **kwargs)
        return Response({"status": "Sizda huquq yo'q "})
    return wrapper