from django.contrib.auth.models import User
from .models import ItemType, Item, Cart, OrderedItem, Size, Topping
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class BasicFoodForm(forms.ModelForm):
    class Meta:
        model = OrderedItem
        fields = ['item', 'size']

    def __init__(self, *args, **kwargs):
        item_id = kwargs.pop('item_id')

        super(BasicFoodForm, self).__init__(*args, **kwargs)

        item_set = Item.objects.filter(id=item_id)

        self.fields['item'].queryset = item_set
        self.fields['size'].queryset = Size.objects.filter(item=item_set[0])

class OneToppingFoodForm(forms.ModelForm):
    topping = forms.ModelChoiceField(queryset=Topping.objects.all())

    class Meta:
        model = OrderedItem
        fields = ['item', 'size']

    def __init__(self, *args, **kwargs):
        item_id = kwargs.pop('item_id')

        super(OneToppingFoodForm, self).__init__(*args, **kwargs)

        item_set = Item.objects.filter(id=item_id)

        self.fields['item'].queryset = item_set
        self.fields['size'].queryset = Size.objects.filter(item=item_set[0])

class CheckoutForm(forms.Form):
    pass
