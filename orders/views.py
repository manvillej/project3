# TODO: module docstring

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.template import loader
from .forms import UserForm, BasicFoodForm, CheckoutForm, OneToppingFoodForm
from .models import ItemType, Item, Cart, OrderedItem, Size, new, ordered, complete, OrderedTopping

# Create your views here.
def index(request):
    # TODO: index docstring
    template = loader.get_template("orders/index.html")

    # context for passing user and cart info.
    current_user = request.user
    cart = Cart.objects.filter(customer=current_user, state=new).first()
    context = {
        'current_user':request.user,
        'cart':cart,
        }
    return HttpResponse(template.render(context, request))


def menu(request):
    # TODO: menu docstring
    template = loader.get_template("orders/menu.html")
    current_user = request.user
    cart = Cart.objects.filter(customer=current_user, state=new).first()
    context = {
        'current_user':request.user,
        'cart':cart,
        "item_type":ItemType.objects.all(),
        "Items":Item,
    }
    return HttpResponse(template.render(context, request))


class UserFormView(View):
    """"""
    # TODO: UserFormView class docstring
    form_class = UserForm
    template_name = "orders/registration_form.html"

    def get(self, request):
        """display a blank form"""
        # TODO: UserFormView.get docstring
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Process form data"""
        # TODO: UserFormView.post docstring
        form = self.form_class(request.POST)

        if(form.is_valid()):
            user = form.save(commit=False)

            # cleaned normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            user.username = username
            user.email = email

            # hash the password
            user.set_password(password)
            user.save()

            # create new cart for future orders
            cart = Cart(customer=user, state=new)
            cart.save()

            # returns user object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                 if user.is_active:
                     login(request, user)
                     return redirect('index')

        return render(request, self.template_name, {'form': form})


class BasicFoodFormView(View):
    """"""
    # TODO: UserFormView class docstring
    form_class = BasicFoodForm
    template_name = "orders/item_form.html"

    def get(self, request, item_id):
        """display a blank form"""
        # TODO: UserFormView.get docstring

        form = self.form_class(item_id=item_id)
        if(item_id==2):
            form = OneToppingFoodForm(item_id=item_id)


        current_user = request.user

        # get current cart
        cart = Cart.objects.filter(customer=current_user, state=new).first()

        context = {
            'current_user':request.user,
            'cart':cart,
            'form': form,
        }
        return render(request, self.template_name, context)


    def post(self, request, item_id):
        """Process form data"""
        # TODO: UserFormView.post docstring
        if(item_id==2):
            form = OneToppingFoodForm(request.POST, item_id=item_id)
        else:
            form = self.form_class(request.POST, item_id=item_id)

        if(form.is_valid()):

            # cleaned normalized data
            item = form.cleaned_data['item']
            size = form.cleaned_data['size']

            current_user = request.user

            cart = Cart.objects.filter(customer=current_user, state=new).first()

            ordered_item = OrderedItem(cart=cart, item=item, size=size)
            ordered_item.save()

            if(item_id==2):
                topping = form.cleaned_data['topping']
                ordered_topping = OrderedTopping(ordered_item=ordered_item, topping=topping)
                ordered_topping.save()

            return redirect('menu')

        return render(request, self.template_name, {'form': form})


class CheckOutFormView(View):
    """"""
    # TODO: UserFormView class docstring
    form_class = CheckoutForm
    template_name = "orders/checkout_form.html"

    def get(self, request):
        """display a blank form"""
        # TODO: UserFormView.get docstring
        form = self.form_class()

        current_user = request.user
        cart = Cart.objects.filter(customer=current_user, state=new).first()
        context = {
            'current_user':request.user,
            'cart':cart,
            "item_type":ItemType.objects.all(),
            "Items":Item,
            'form': form,
        }
        return render(request, self.template_name, context)


    def post(self, request):
        """Process form data"""
        # TODO: UserFormView.post docstring
        form = self.form_class(request.POST)

        if(form.is_valid()):
            current_user = request.user

            # get current cart
            cart = Cart.objects.filter(customer=current_user, state=new).first()

            # submit current cart
            cart.state = ordered
            cart.save()

            # create new cart for future orders
            cart = Cart(customer=current_user, state=new)
            cart.save()

            return redirect('menu')

        return render(request, self.template_name, {'form': form})
