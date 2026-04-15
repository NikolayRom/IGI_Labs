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

class ClientRegistrationForm(CustomUserCreationForm):
    company_name = forms.CharField(max_length=100, help_text='Client\'s company name')
    phone = forms.CharField(max_length=19, help_text='Phone number of client (+375 (29) 000-00-00)')
    address = forms.CharField(max_length=100, help_text='Client\'s address')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('birth_date', 'company_name', 'address', 'phone')

    def clean_phone(self):
        phone_data = self.cleaned_data.get('phone')
        
        if not re.match(r'^\+375\s?\(?29\)?\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}$', phone_data):
            raise forms.ValidationError('Phone number must be in format: +375 (29) XXX-XX-XX')
        
        if Phone.objects.filter(phone__iexact=phone_data).exists():
            raise forms.ValidationError('This phone already exist')
            
        return phone_data

    def save(self, commit=True):
        user = super().save(commit=commit)
        phone = Phone.objects.create(phone=self.cleaned_data['phone'])
        Client.objects.create(
            user=user,
            company_name=self.cleaned_data['company_name'],
            address=self.cleaned_data['address'],
            phone=phone
        )
        return user

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


