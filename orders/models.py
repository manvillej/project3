from django.db import models
import uuid

# Create your models here.
class ItemType(models.Model):
    # TODO: itemtype docstring
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Item(models.Model):
    # TODO: item docstring
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE, related_name="ItemTypes")
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=400)

    def __str__(self):
        return f'{self.item_type}:{self.name}'


