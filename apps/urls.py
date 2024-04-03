from django.urls import path, include

urlpatterns = [
    path('', include('apps.app.urls')),
    path('', include('apps.finance.urls')),
    path('', include('apps.products.urls')),
    path('', include('apps.trade.urls')),
]
