from django.contrib import admin

from .models import ItemType, Item

# Register your models here.
admin.site.register(ItemType)
admin.site.register(Item)
