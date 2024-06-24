from django.apps import AppConfig


# class ProductsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'apps.products'
#
#     def ready(self):
#         import apps.products.signals


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.products'
    def ready(self):
        import apps.products.signals