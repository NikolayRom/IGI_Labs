from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

class CustomUserCreationForm(UserCreationForm):
    
    birth_date = forms.DateField(
        label='Date of birth',
        required=True,
        input_formats=['%d.%m.%Y'],
        help_text='Enter date: dd.mm.YYYY'
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('birth_date',)

class UserUpdateForm(forms.ModelForm):
    
    username = forms.CharField(
        max_length=20,
        label='Username'
    )
    
    first_name = forms.CharField(
        max_length=20,
        label='First Name',
        required=False
    )

    last_name = forms.CharField(
        max_length=20,
        label='Last Name',
        required=False
    )

    email = forms.EmailField(
        label='Email',
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']


