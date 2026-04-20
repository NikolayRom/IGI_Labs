from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

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

class EmployeeAdminForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Employee\'s email')

    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = getattr(self.instance, 'user', None)
        if user and self.instance.pk:
            self.fields['email'].initial = user.email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        user = cleaned_data.get('user') or getattr(self.instance, 'user', None)

        if email and user:
            if CustomUser.objects.filter(email__iexact=email).exclude(pk__exact=user.pk).exists():
                self.add_error('email', 'This email is already exists')
            user.email = email
        return cleaned_data

    def save(self, commit=True):
        employee = super().save(commit=False)
        user = self.cleaned_data.get('user') or getattr(self.instance, 'user', None)
        if user:
            user.email = self.cleaned_data.get('email')
            user.save()
            employee.user = user
        
        if commit:
            employee.save()
        return employee

class ClientRegistrationForm(CustomUserCreationForm):
    company_name = forms.CharField(max_length=100, help_text='Client\'s company name')
    phone = forms.CharField(max_length=19, help_text='Phone number of client (+375 (29) 000-00-00)')
    address = forms.CharField(max_length=100, help_text='Client\'s address')

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label='City'
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('birth_date', 'company_name', 'address', 'phone', 'city')

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
            phone=phone,
            city=self.cleaned_data.get('city'),
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

class ClientUpdateForm(forms.ModelForm):
    
    company_name = forms.CharField(
        max_length=100,
        help_text='Client\'s company name',
        label='Company name'
    )
    phone = forms.CharField(
        max_length=19,
        help_text='(+375 (29) XXX-XX-XX)',
        label='Phone'
    )
    address = forms.CharField(
        max_length=100,
        help_text='Client\'s address',
        label='Address'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.phone:
            self.fields['phone'].initial = self.instance.phone.phone

    def clean_phone(self):
        phone_data = self.cleaned_data.get('phone')
        
        if not re.match(r'^\+375\s?\(?29\)?\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}$', phone_data):
            raise forms.ValidationError('Phone number must be in format: +375 (29) XXX-XX-XX')
        
        if Phone.objects.filter(phone__iexact=phone_data).exclude(pk__exact=self.instance.phone.pk).exists():
            raise forms.ValidationError('This phone already exist')
            
        return phone_data

    def save(self, commit=True):
        client = super().save(commit=False)
        phone_obj = client.phone
        phone_obj.phone = self.cleaned_data.get('phone')
        phone_obj.save()
        if commit:
            client.save()
        return client

    class Meta:
        model = Client
        fields = ['company_name', 'address', 'city']

class EmployeeUpdateForm(forms.ModelForm):
    
    info = forms.CharField(
        max_length=100,
        label='Info'
    )

    phone = forms.CharField(
        max_length=19,
        help_text='(+375 (29) XXX-XX-XX)',
        label='Phone'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.phone:
            self.fields['phone'].initial = self.instance.phone.phone

    def clean_phone(self):
        phone_data = self.cleaned_data.get('phone')
        
        if not re.match(r'^\+375\s?\(?29\)?\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}$', phone_data):
            raise forms.ValidationError('Phone number must be in format: +375 (29) XXX-XX-XX')
        
        if Phone.objects.filter(phone__iexact=phone_data).exclude(pk__exact=self.instance.phone.pk).exists():
            raise forms.ValidationError('This phone already exist')
            
        return phone_data

    def save(self, commit=True):
        employee = super().save(commit=False)
        phone_obj = employee.phone
        phone_obj.phone = self.cleaned_data.get('phone')
        phone_obj.save()
        if commit:
            employee.save()
        return employee

    class Meta:
        model = Employee
        fields = ['info', 'image']

class ReviewForm(forms.ModelForm):
    
    review = forms.CharField(
        max_length=200,
        label='Review',
        help_text='User\'s review'
    )
    
    grade = forms.IntegerField(
        min_value=1,
        max_value=5,
        help_text='Grade for review',
        required=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        label='Grade'
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ReviewForm, self).__init__(*args, **kwargs)

    def clean_grade(self):
        grade_data = self.cleaned_data.get('grade')
        
        if grade_data < 1 or grade_data > 5:
            raise forms.ValidationError('Grade must be in range from 1 to 5') 
        
        return grade_data

    def save(self, commit=True):
        review = Review.objects.create(
            review=self.cleaned_data.get('review'),
            grade=self.cleaned_data.get('grade'),
            user=self.user
        )
        if commit:
            review.save()
        return review

    class Meta:
        model = Review
        fields = ['review', 'grade']

class OrderCreateForm(forms.ModelForm):

    promo = forms.ModelChoiceField(
        queryset=Promo.objects.none(),
        required=False,
        label='Promo'
    )

    pick_up_point = forms.ModelChoiceField(
        queryset=PickUpPoint.objects.none(),
        label='Pick-up point'
    )

    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        super(OrderCreateForm, self).__init__(*args, **kwargs)

        self.fields['promo'].queryset = Promo.objects.filter(end_date__gte=date.today())
        self.fields['pick_up_point'].queryset = PickUpPoint.objects.filter(city__exact=self.client.city)

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        promo = cleaned_data.get('promo')
        if promo and product:
            if promo.product != product:
                raise forms.ValidationError({
                    'promo': 'This promo is for another product'
                })
        return cleaned_data

    def save(self, commit=True):
        order = Order.objects.create(
            product=self.cleaned_data.get('product'),
            product_amount=self.cleaned_data.get('product_amount'),
            client=self.client,
            date_order_create=timezone.now(),
            promo=self.cleaned_data.get('promo'),
            pick_up_point=self.cleaned_data.get('pick_up_point')
        )
        if commit:
            order.save()
        return order

    class Meta:
        model = Order
        fields = ['product', 'product_amount', 'pick_up_point', 'promo']

