from django.contrib import admin
from apps.app.models import Worker, Position
# Register your models here.

class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

admin.site.register(Position, PositionAdmin)

class WorkerAdmin(admin.ModelAdmin):
    list_display = ('position','name', 'phone', 'added',)
    search_fields = ['name', 'phone']
    date_hierarchy = 'added'
admin.site.register(Worker, WorkerAdmin)