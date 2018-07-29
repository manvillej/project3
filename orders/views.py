# TODO: module docstring

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.template import loader
from .forms import UserForm

# Create your views here.
def index(request):
    # TODO: index docstring
    template = loader.get_template("orders/index.html")

    # context for passing user and cart info.
    context = {}
    return HttpResponse(template.render(context, request))


def menu(request):
    # TODO: menu docstring
    return HttpResponse("Project 3: Menu TODO")

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

            # returns user object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                 if user.is_active:
                     login(request, user)
                     return redirect('index')

        return render(request, self.template_name, {'form': form})




