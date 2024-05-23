from rest_framework.response import Response

def is_storage_permission(function):
    def wrapper(self,request,*args, **kwargs):
        if request.user.is_storage:
            return function(self,request, *args, **kwargs)
        return Response({"status": "Sizda huquq yo'q "})
    return wrapper


def is_product_permission(function):
    def wrapper(self, request, *agrs, **kwargs):
        if request.user.is_product:
            return function(self, request, *agrs, **kwargs)
        return Response({"status":"Sizda huquq yo'q"})
    return wrapper