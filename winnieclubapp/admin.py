from django.contrib import admin
from .models import Member, Event, Worker, StockItem

admin.site.register(Member)
admin.site.register(Event)
admin.site.register(Worker)

from django.contrib import admin
from .models import StockItem

@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'min_stock_level', 'is_low_stock')

    def is_low_stock(self, obj):
        return obj.quantity <= obj.min_stock_level
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Low Stock'
