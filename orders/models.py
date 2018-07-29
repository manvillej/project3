from django.db import models
import uuid

# Create your models here.
class ItemType(models.Model):
    # TODO: ItemType docstring
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Item(models.Model):
    # TODO: Item docstring
    item_type = models.ForeignKey(
        ItemType,
        on_delete=models.CASCADE,
        related_name="items",
        )

    name = models.CharField(max_length=64)
    description = models.CharField(max_length=400)

    def __str__(self):
        return f'{self.item_type}:{self.name}'


class Topping(models.Model):
    # TODO: Topping docstring
    item_type = models.ForeignKey(
        ItemType,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="toppings",
        )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="toppings",
        )

    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        if(self.item):
            return f'{self.name} - {self.price} for {self.item}'
        elif(self.item_type):
            return f'{self.name} - ${self.price} for {self.item_type}'
        else:
            return 'Error, topping requires item or item_type'


class Size(models.Model):
    # TODO: Size docstring
    small = 'sm'
    regular = 'rg'
    large = 'lg'

    SIZES = (
        (small, 'Small'),
        (regular, 'Regular'),
        (large, 'Large'),
    )

    name = models.CharField(
        max_length=2,
        choices=SIZES,
        default=regular,
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="size")
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.item} - {self.name} - {self.price}'


