from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
new = '01'
ordered = '02'
complete = '03'


class Cart(models.Model):
    # TODO: Cart Docstring
    customer =  models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE,
    )

    STATES = (
        (new, 'New'),
        (ordered, 'Ordered'),
        (complete, 'Complete'),
    )

    state = models.CharField(
        max_length=2,
        choices=STATES,
        default=new,
    )

    def __str__(self):
        return f'Customer={self.customer}, state={self.get_state_display()}'

    @property
    def price(self):
        total = 0
        for order in self.ordered_items.all():
            total = total + order.price
        return total


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

    CHOICES = (
        (0, 'None'),
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (5, 'Five'),
    )
    num_toppings =  models.IntegerField(choices=CHOICES)

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
        return f'{self.item} - {self.get_name_display()} - {self.price}'


class OrderedItem(models.Model):
    # TODO: OrderedItems Docstring
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="ordered_items",
        )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        )

    @property
    def price(self):
        """"""
        total = self.size.price
        for topping in self.toppings.all():
            total = total + topping.price
        return total

    def __str__(self):
        return f'{self.size.get_name_display()} {self.item.name} {self.item.item_type.name} - ${self.price}'


class OrderedTopping(models.Model):
    ordered_item = models.ForeignKey(
        OrderedItem,
        on_delete=models.CASCADE,
        related_name="toppings",
        )
    topping = models.ForeignKey(
        Topping,
        on_delete=models.CASCADE,
        )

    @property
    def price(self):
        return self.topping.price

    def __str__(self):
        return self.topping.name

