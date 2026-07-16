from django.contrib import admin
from .models import *


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    filter_horizontal = ['item_category']
    fields = ['item_name','gender','item_category','item_image','price','is_sold','inventory','description']
admin.site.register(Category)
admin.site.register(Review)