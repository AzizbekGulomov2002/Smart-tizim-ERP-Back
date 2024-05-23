from rest_framework.response import Response

def is_finance_permission(function):
    def wrapper(self, request ,*args, **kwargs):
        if request.user.is_finance:
            return function(self, request, *args, **kwargs)
        return Response({"status":"Sizda bunday huquq yo'q"})
    return wrapper
