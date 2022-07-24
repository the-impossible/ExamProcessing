# My django imports
from django.contrib.auth.models import AnonymousUser
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages

# My app imports

def is_admin(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return func(request, *args, **kwargs)
            else:
                messages.warning(request, 'You are not authorized to view that page')
                return redirect('sims_admin:dashboard')
    return wrapper_func

def is_staff(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return func(request, *args, **kwargs)
            else:
                messages.warning(request, 'You are not authorized to view that page')
                return redirect('sims_admin:dashboard')
    return wrapper_func