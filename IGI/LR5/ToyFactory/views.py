from django.shortcuts import render
from django.views import generic
from .models import *

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def index(request):
    #some analyze
    return render(
        request,
        'index.html',
        context={}
    )


