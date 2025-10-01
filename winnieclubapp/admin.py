from django.contrib import admin
from .models import Member, Event ,Worker, StockItem

admin.site.register(Member)
admin.site.register(Event)
admin.site.register(Worker)




@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity')
    search_fields = ('name',)
