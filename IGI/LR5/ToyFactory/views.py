from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def index(request):
    return render(
        request,
        'index.html',
        context={}
    )

def profile(request):
    form = UserUpdateForm(instance=request.user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        form.save()
        return redirect('index')
    
    context = {'form': form}
    return render(request, 'registration/profile.html', context=context)

def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        user = form.save()
        login(request, user)
        return redirect('index')
    context = {'form': form}
    return render(request, 'registration/register.html', context=context)

