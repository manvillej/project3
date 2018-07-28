# TODO: module docstring

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    # TODO: index docstring

    return HttpResponse("Project 3: Index TODO")


def register(request):
    # TODO: register docstring
    return HttpResponse("Project 3: Register TODO")


def login(request):
    # TODO: login docstring
    return HttpResponse("Project 3: Login TODO")


def logout(request):
    # TODO: logout docstring
    return HttpResponse("Project 3: Logout TODO")


def menu(request):
    # TODO: menu docstring
    return HttpResponse("Project 3: Menu TODO")

