from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

import logging
logger = logging.getLogger('ToyFactory')

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
                logger.error(f"email is already exist")
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
            logger.error(f"invalid phone format")
            raise forms.ValidationError('Phone number must be in format: +375 (29) XXX-XX-XX')
        
        if Phone.objects.filter(phone__iexact=phone_data).exists():
            logger.error(f"phone already exist")
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
            logger.error(f"invalid phone format")
            raise forms.ValidationError('Phone number must be in format: +375 (29) XXX-XX-XX')
        
        if Phone.objects.filter(phone__iexact=phone_data).exclude(pk__exact=self.instance.phone.pk).exists():
            logger.error(f"phone alredy exist")
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
            logger.error(f"invalid phone format")
            raise forms.ValidationError('Phone number must be in format: +375 (29) XXX-XX-XX')
        
        if Phone.objects.filter(phone__iexact=phone_data).exclude(pk__exact=self.instance.phone.pk).exists():
            logger.error(f"phone already exist")
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
        widget=forms.Textarea(
            attrs={'rows': 4, 'cols': 50, 'placeholder': 'Напишите ваш отзыв о продукции фабрики...'}),
        max_length=500,
        label='Текст отзыва',
        help_text='Поделитесь впечатлениями о качестве игрушек и сервисе'
    )

     
    GRADE_CHOICES = (
        (5, '★★★★★ (5 - Отлично)'),
        (4, '★★★★☆ (4 - Хорошо)'),
        (3, '★★★☆☆ (3 - Удовлетворительно)'),
        (2, '★★☆☆☆ (2 - Плохо)'),
        (1, '★☆☆☆☆ (1 - Ужасно)'),
    )

    grade = forms.ChoiceField(
        choices=GRADE_CHOICES,
        initial=5,
        label='Ваша оценка',
        help_text='Выберите оценку от 1 до 5'
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ReviewForm, self).__init__(*args, **kwargs)

    def clean_grade(self):
        grade_data = int(self.cleaned_data.get('grade'))
        if grade_data < 1 or grade_data > 5:
            logger.error("invalid value for grade")
            raise forms.ValidationError('Оценка должна быть от 1 до 5')
        return grade_data

    def save(self, commit=True):
        review = Review(
            review=self.cleaned_data.get('review'),
            grade=int(self.cleaned_data.get('grade')),
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

        if not self.instance.date_order_create:
            self.instance.date_order_create = timezone.now()

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        promo = cleaned_data.get('promo')
        if promo and product:
            if promo.product != product:
                logger.error(f"wrong product for promo")
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


class PaymentForm(forms.Form):
    PAYMENT_METHODS = (
        ('card', 'Банковская корпоративная карта'),
        ('invoice', 'Безналичный расчет (по счету-фактуре)')
    )

    pay_method = forms.ChoiceField(
        choices=PAYMENT_METHODS,
        initial='card',
        widget=forms.RadioSelect
    )
    card_number = forms.CharField(
        max_length=19,
        label='Номер карты',
        widget=forms.TextInput(attrs={'placeholder': 'XXXX XXXX XXXX XXXX'})
    )
    card_holder = forms.CharField(
        max_length=50,
        label='Владелец карты',
        widget=forms.TextInput(attrs={'placeholder': 'IVAN IVANOV'})
    )
    card_expiry = forms.CharField(
        max_length=5,
        label='Срок действия (ММ/ГГ)',
        widget=forms.TextInput(attrs={'placeholder': 'ММ/ГГ'})
    )
    card_cvc = forms.CharField(
        max_length=3,
        label='CVC/CVV',
        widget=forms.PasswordInput(attrs={'placeholder': '•••'})
    )

    def clean_card_number(self):
         
        card_num = self.cleaned_data.get('card_number', '').replace(' ', '').replace('-', '')
        if not card_num.isdigit() or len(card_num) < 16 or len(card_num) > 19:
            raise forms.ValidationError('Номер карты должен содержать от 16 до 19 цифр!')
        return card_num

    def clean_card_expiry(self):
        expiry = self.cleaned_data.get('card_expiry', '').strip()
        if not re.match(r'^(0[1-9]|1[0-2])\/(\d{2})$', expiry):
            raise forms.ValidationError('Формат срока действия должен быть строго ММ/ГГ (например, 12/26)!')

        month, year = expiry.split('/')
        exp_month = int(month)
        exp_year = int("20" + year)   

        now = timezone.now()
        current_year = now.year
        current_month = now.month

         
        if (exp_year < current_year) or (exp_year == current_year and exp_month < current_month):
            raise forms.ValidationError(f'Срок действия карты истек ({expiry}). Карта не может быть принята!')

         
        if exp_year > current_year + 10:
            raise forms.ValidationError('Некорректный год окончания действия карты!')

        return expiry

    def clean_card_cvc(self):
        cvc = self.cleaned_data.get('card_cvc', '').strip()
        if not cvc.isdigit() or len(cvc) != 3:
            raise forms.ValidationError('CVC/CVV код должен состоять строго из 3 цифр!')
        return cvc