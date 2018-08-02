# TODO: module docstring

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.template import loader
from .forms import UserForm, BasicFoodForm, CheckoutForm, OneToppingFoodForm, TwoToppingFoodForm, ThreeToppingFoodForm, FiveToppingFoodForm
from .models import ItemType, Item, Cart, OrderedItem, Size, new, ordered, complete, OrderedTopping
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def index(request):
    # TODO: index docstring
    template = loader.get_template("orders/index.html")
    context = {}

    # context for passing user and cart info.
    current_user = request.user
    # db operations crash is user isnt logged in
    if(current_user.is_authenticated):
        cart = Cart.objects.filter(customer=current_user, state=new).first()
        context['current_user'] = request.user
        context['cart'] = cart

    return HttpResponse(template.render(context, request))


def menu(request):
    # TODO: menu docstring
    template = loader.get_template("orders/menu.html")
    context = {
            "item_type":ItemType.objects.all(),
            "Items":Item,
        }

    # context for passing user and cart info.
    current_user = request.user
    # db operations crash is user isnt logged in
    if(current_user.is_authenticated):
        cart = Cart.objects.filter(customer=current_user, state=new).first()
        context['current_user'] = request.user
        context['cart'] = cart

    return HttpResponse(template.render(context, request))


def carts(request):
    # TODO: docstring

    # non staff shouldn't access this page
    current_user = request.user
    if(not current_user.is_staff):
        return redirect('menu')

    template = loader.get_template("orders/carts.html")
    current_user = request.user
    carts = Cart.objects.filter(state=ordered)
    context = {
        'carts':carts,
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


class BasicFoodFormView(LoginRequiredMixin, View):
    """"""
    # TODO: UserFormView class docstring
    form_class = BasicFoodForm
    template_name = "orders/item_form.html"

    def get(self, request, item_id):
        """display a blank form"""
        # TODO: UserFormView.get docstring

        # set the current form to be no toppings
        form = self.form_class(item_id=item_id)

        # get current item
        item = Item.objects.get(id=item_id)
        # override form if item's num_toppings is 1,2,3, or 5
        if(item.num_toppings==1):
            form = OneToppingFoodForm(item_id=item_id)
        if(item.num_toppings==2):
            form = TwoToppingFoodForm(item_id=item_id)
        if(item.num_toppings==3):
            form = ThreeToppingFoodForm(item_id=item_id)
        if(item.num_toppings==5):
            form = FiveToppingFoodForm(item_id=item_id)


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

        # get current item
        item = Item.objects.get(id=item_id)
        # override form if item's num_toppings is 1,2,3, or 5
        if(item.num_toppings==1):
            form = OneToppingFoodForm(request.POST, item_id=item_id)
        if(item.num_toppings==2):
            form = TwoToppingFoodForm(request.POST, item_id=item_id)
        if(item.num_toppings==3):
            form = ThreeToppingFoodForm(request.POST, item_id=item_id)
        if(item.num_toppings==5):
            form = FiveToppingFoodForm(request.POST, item_id=item_id)
        else:
            form = self.form_class(request.POST, item_id=item_id)

        if(form.is_valid()):

            # cleaned normalized data
            item = form.cleaned_data.pop('item')
            size = form.cleaned_data.pop('size')

            current_user = request.user

            cart = Cart.objects.filter(customer=current_user, state=new).first()

            ordered_item = OrderedItem(cart=cart, item=item, size=size)
            ordered_item.save()

            # loop through all the toppings
            for key in form.cleaned_data:
                topping = form.cleaned_data[key]
                # if the field is not filled out, do not add it as an topping
                if(topping):
                    ordered_topping = OrderedTopping(ordered_item=ordered_item, topping=topping)
                    ordered_topping.save()

            return redirect('menu')

        return render(request, self.template_name, {'form': form})

class OrderedCartView(LoginRequiredMixin, View):
    form_class = CheckoutForm
    template_name = "orders/checkout_form.html"

    def get(self, request, cart_id):
        """display a blank form"""
        # TODO: UserFormView.get docstring

        # non staff shouldn't access this page
        current_user = request.user
        if(not current_user.is_staff):
            return redirect('menu')


        form = self.form_class()

        cart = Cart.objects.get(id=cart_id)
        context = {
            'cart':cart,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, cart_id):
        """Process form data"""
        # TODO: UserFormView.post docstring

        # non staff shouldn't access this page
        current_user = request.user
        if(not current_user.is_staff):
            return redirect('menu')

        form = self.form_class(request.POST)

        if(form.is_valid()):

            # get cart
            cart = Cart.objects.get(id=cart_id)

            # complete cart
            cart.state = complete
            cart.save()

            return redirect('carts')

        return render(request, self.template_name, {'form': form})


class CheckOutFormView(LoginRequiredMixin, View):
    """"""
    # TODO: UserFormView class docstring
    form_class = CheckoutForm
    template_name = "orders/checkout_form.html"

    def get(self, request):
        """display a blank form"""
        # TODO: UserFormView.get docstring
        form = self.form_class()

        current_user = request.user

        # need customer's current cart
        cart = Cart.objects.filter(customer=current_user, state=new).first()

        # redirect to menu if cart is empty
        if(not cart.ordered_items.all()):
            return redirect('menu')

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
        current_user = request.user

        # get current cart
        cart = Cart.objects.filter(customer=current_user, state=new).first()

        # redirect to menu if cart is empty
        if(not cart.ordered_items.all()):
            return redirect('menu')

        if(form.is_valid()):
            # submit current cart
            cart.state = ordered
            cart.save()

            # create new cart for future orders
            cart = Cart(customer=current_user, state=new)
            cart.save()

            return redirect('menu')

        return render(request, self.template_name, {'form': form})


