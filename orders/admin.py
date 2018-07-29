from django.contrib import admin

from .models import ItemType, Item, Size, Topping

# Register your models here.
admin.site.register(ItemType)
admin.site.register(Item)
admin.site.register(Size)
admin.site.register(Topping)
