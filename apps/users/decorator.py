
from rest_framework.response import Response

# def is_client_permission(function):
#     def wrapper(self,request,*args, **kwargs):
#         if request.user.is_trade:
#             return function(self,request, *args, **kwargs)
#         return Response({"status": "Sizda huquq yo'q "})
#     return wrapper

def is_user_permission(function):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_user_create:
            return function(self, request, *args, **kwargs)
        return Response({"status":"Sizda bunday huquq yo'q"})
    return wrapper