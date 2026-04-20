from django.db import models
import uuid  
from datetime import date 
import datetime
import re
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, Permission
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

class BaseDateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated date")

    class Meta:
        abstract = True

class CustomUser(AbstractUser, BaseDateModel):
    birth_date = models.DateField(help_text='Date of birth')

    REQUIRED_FIELDS = ['birth_date']

    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None
    
    def clean(self):
        super().clean()

        if self.is_superuser:
            return

        if not self.birth_date:
            raise ValidationError({'birth_date': 'Age must be initialize!'})

        if self.email and CustomUser.objects.filter(email__iexact=self.email).exclude(pk=self.pk):
            raise ValidationError({'email': 'This email already exist!'})

        if self.age < 18:
            raise ValidationError({'birth_date': 'Age must be 18 or older'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return AbstractUser.__str__(self)

class Product(BaseDateModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, help_text="Unique ID for product")
    name = models.CharField(max_length=100, default='product-'+str(uuid.uuid4()), help_text='Name for product')
    product_type = models.ManyToManyField('ProductType', help_text='Type for product')
    product_model = models.ForeignKey('ProductModel', on_delete=models.CASCADE, help_text='Model for product')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Price for product',
        validators=[
            MinValueValidator(0.01)
        ]
    )

    PRODUCT_STATUS = (
        ('a', 'Available'),
        ('d', 'Discontinued')
    )

    status = models.CharField(
        max_length=1,
        choices=PRODUCT_STATUS,
        default='a',
        help_text='Product availability')
    
    def display_product_type(self):
        return ', '.join(str(product_type) for product_type in self.product_type.all()[:3])
    display_product_type.short_description = 'Type'
        
    def clean(self):
        super().clean()
        if not self.name.strip():
            raise ValidationError({'name': 'Name must be initialize'})
        elif self.price <= 0:
            raise ValidationError({'price': 'Price must be positive'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_model} ({self.display_product_type()}): {self.name}"
    
    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])

    class Meta:
        ordering = ['status', 'price', 'product_model', 'name']
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='product_name_case_insensitive_unique',
                violation_error_message = "Name already exists (case insensitive match)"
            ),
        ]

class ProductType(BaseDateModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, help_text="Unique ID for product type")
    name = models.CharField(max_length=100, help_text='Product type name')

    def clean(self):
        super().clean()
        if not self.name.strip():
            raise ValidationError({'name': 'Name must be initialize'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('productType-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='product_type_name_case_insensitive_unique',
                violation_error_message = "Name already exists (case insensitive match)"
            ),
        ]

class ProductModel(BaseDateModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, help_text="Unique ID for product model")
    name = models.CharField(max_length=100, help_text='Product model name')

    def clean(self):
        super().clean()
        if not self.name.strip():
            raise ValidationError({'name': 'Name must be initialize'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('productModel-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='product_model_name_case_insensitive_unique',
                violation_error_message = "Name already exists (case insensitive match)"
            ),
        ]

class Employee(BaseDateModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, help_text='Employee\'s unique ID')
    info = models.CharField(
        max_length=100,
        help_text='Info about employee\'s tasks',
        default='Employee of Toy Factory',
        blank=True
    )
    phone = models.OneToOneField(
        'Phone',
        on_delete=models.CASCADE,
        help_text='Employee\'s phone',
    )
    image = models.ImageField(
        help_text='Image for Employee\'s profile',
        blank=True,
    )

    @property
    def get_avatar_url(self):
        if self.image:
            return self.image.url
    
        seed = self.id.int if hasattr(self.id, 'int') else self.id
        random_id = (seed % 121) + 1
        return f"https://randomfox.ca/images/{random_id}.jpg"

    def display_email(self):
        return self.user.email
    display_email.short_description = 'Email'

    def display_username(self):
        return self.user.username
    display_username.short_description = 'Username'
    
    def clean(self):
        super().clean()
        if Client.objects.filter(user__exact=self.user).exists() or self.user.is_superuser:
            raise ValidationError('This user is not available!')
        elif not self.user.email or CustomUser.objects.filter(email__iexact=self.user.email).exclude(pk=self.user.pk):
            raise ValidationError('Employee must have his own email!')
        
    def save(self, *args, **kwargs):
        self.full_clean()
        self.user.user_permissions.add(Permission.objects.get(codename='employee_perm'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Employee: {self.display_username()}"
    
    def get_absolute_url(self):
        return reverse('contacts-detail', args=[str(self.id)])

class Client(BaseDateModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile',
    )
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, help_text="Client\'s unique ID")
    company_name = models.CharField(max_length=100, help_text='Client\'s company name')
    phone = models.OneToOneField('Phone', on_delete=models.CASCADE, help_text='Client\'s phone')
    address = models.CharField(max_length=100, help_text='Client\'s address')
    city = models.ForeignKey('City', on_delete=models.CASCADE, help_text='Clients\'s city')

    def clean(self):
        super().clean()
        if self.user.is_superuser or Employee.objects.filter(user__exact=self.user).exists():
            raise ValidationError('This user is not available!')
        elif not self.company_name.strip():
            raise ValidationError({'company_name': 'Company name must be initialize'})
        elif not self.address.strip():
            raise ValidationError({'address': 'Address must be initialize'})

    def display_username(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.full_clean()
        self.user.user_permissions.add(Permission.objects.get(codename='client_perm'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Client: {self.company_name} ({self.phone}) - {self.city} | {self.address}"

    def get_absolute_url(self):
        return reverse('client-detail', args=[str(self.id)])

    class Meta:
        ordering = ['city', 'company_name']
        constraints = [
            UniqueConstraint(
                Lower('company_name'),
                name='company_name_case_insensitive_unique',
                violation_error_message = "Company name already exists (case insensitive match)"
            ),
        ]

class Order(BaseDateModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, help_text="Unique ID for order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, help_text='Client order of product')
    date_order_create = models.DateTimeField(help_text='Date of create order')
    date_order_complete = models.DateTimeField(null=True, blank=True, help_text='Date of complete order')
    product_amount = models.PositiveIntegerField(
        default=1,
        help_text='Amount of products in order',
        validators=[
            MinValueValidator(1)
        ]
    )
    promo = models.ForeignKey(
        'Promo', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text='Applied promo code'
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, help_text='Client of order')
    pick_up_point = models.ForeignKey(
        'PickUpPoint',
        on_delete=models.CASCADE,
        help_text='Client\'s pick-up point'
    )

    @property
    def product_name(self):
        return self.product.name if self.product else None
    
    @property
    def product_price(self):
        return self.product.price
    
    @property
    def promo_sale_percentage(self):
        return str(self.promo.sale*100) + '%'

    @property
    def get_total(self):
        total = self.product.price * self.product_amount
        if self.promo:
            total = total * (1 - self.promo.sale)
        return round(total, 2)

    @property
    def client_pick_up_point(self):
        return self.client.pick_up_point

    @property
    def client_company(self):
        return self.client.company_name if self.client else None

    def clean(self):
        super().clean()
        if self.product_amount == 0:
            raise ValidationError({'product_amount': 'Amount of products must be positive number (not zero!)'})
        elif self.date_order_create == None:
            raise ValidationError({'date_order_create': 'Date of creating order must be initialize!'})
        elif self.date_order_complete != None and (self.date_order_complete > timezone.now() or self.date_order_complete < self.date_order_create):
            raise ValidationError({'date_order_complete': 'End date must be greater than date of create and not be future'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order: <{self.product_amount}> {self.product_name} ({self.date_order_create}-{self.date_order_complete}) by {self.client_company}'
    
    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])

    class Meta:
        ordering = ['-date_order_create', '-product_amount', 'product']

class City(BaseDateModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, help_text="Unique ID for city")
    name = models.CharField(max_length=100, default='city-'+str(uuid.uuid4()), help_text='Name of city')

    def clean(self):
        super().clean()
        if not self.name.strip():
            raise ValidationError({'name': 'Name must be initialize'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('city-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='city_name_case_insensitive_unique',
                violation_error_message = "Name already exists (case insensitive match)"
            ),
        ]

class PickUpPoint(BaseDateModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, help_text="Unique ID for pick-up point")
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, help_text='City of pick-up point')
    address = models.CharField(max_length=100, help_text='Address of pick-up point')

    def display_city_name(self):
        return self.city.name

    def clean(self):
        super().clean()
        if not self.address.strip():
            raise ValidationError({'address': 'Address must be initialize'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.city}: {self.address}'
    
    def get_absolute_url(self):
        return reverse('pick_up_point-detail', args=[str(self.id)])

    class Meta:
        ordering = ['city', 'address']

class Phone(BaseDateModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, help_text="Unique ID for phone")
    phone = models.CharField(max_length=19, default='+375 (29) 000-00-00', help_text='Phone number of client')

    def clean(self):
        super().clean()
        if not re.match(r'^\+375\s?\(?29\)?\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}$', self.phone):
            raise ValidationError({'phone': 'Phone number must be in format: +375 (29) XXX-XX-XX'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone
    
    def get_absolute_url(self):
        return reverse('phone-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('phone'),
                name='phone_case_insensitive_unique',
                violation_error_message = "Phone already exists (case insensitive match)"
            ),
        ]

class Promo(BaseDateModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, help_text="Unique ID for phone")
    info = models.CharField(
        max_length=50,
        default='Promo code for any orders',
        help_text='Promo code for clients'
    )
    sale = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.1,
        help_text='Sale for order',
        validators=[
            MaxValueValidator(1.0),
            MinValueValidator(0.0)
        ]
    )

    def promo_sale_percentage(self):
        return str(self.sale*100) + '%'

    def get_default_end_date():
        return date.today() + datetime.timedelta(days=7)
    
    end_date = models.DateField(default=get_default_end_date)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text='Product\'s promo',
    )

    def get_product_name(self):
        return self.product.name

    def is_active(self):
        return date.today() < self.end_date

    def clean(self):
        super().clean()
        if self.sale > 1.0 or self.sale < 0.0:
            raise ValidationError({'sale': 'Sale for client must be 0 <= sale <= 1'})
        elif self.end_date < date.today():
            raise ValidationError({'end_date': 'Promo has expired'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.get_product_name()} ({self.promo_sale_percentage()}): {self.info}'
    
    def get_absolute_url(self):
        return reverse('promo-detail', args=[str(self.id)])

    class Meta:
        ordering = ['sale']

class AboutInfo(BaseDateModel):
    header = models.CharField(
        max_length=100,
        help_text='Header for Company Info'
    )
    info = models.TextField(
        help_text='Description for Company'
    )
    logo = models.ImageField(
        blank=True,
        default='default_about_logo.png',
        help_text='Logotype for Company'
    )

    def __str__(self):
        return self.header
    
    def get_absolute_url(self):
        return reverse('about-detail', args=[str(self.id)])

    class Meta:
        ordering = ['created_at']

class News(BaseDateModel):
    header = models.CharField(
        max_length=400,
        help_text='Header for News'
    )
    info = models.TextField(
        help_text='Description of News'
    )
    image = models.ImageField(
        blank=True,
        default='default_news_logo.png',
        help_text='Image for news'
    )

    def __str__(self):
        return self.header
    
    def get_absolute_url(self):
        return reverse('news-detail', args=[str(self.id)])

    class Meta:
        ordering = ['created_at']

class FAQ(BaseDateModel):
    question = models.CharField(
        max_length=200,
        help_text='Question'
    )
    answer = models.TextField(
        help_text='Answer'
    )
  
    def __str__(self):
        return self.question
    
    def get_absolute_url(self):
        return reverse('faq-detail', args=[str(self.id)])

    class Meta:
        ordering = ['created_at']
        constraints = [
            UniqueConstraint(
                Lower('question'),
                name='question_case_insensitive_unique',
                violation_error_message = "Question already exists (case insensitive match)"
            ),
        ]

class Vacancy(BaseDateModel):
    title = models.CharField(
        max_length=200,
        help_text='Title for Vacancy'
    )
    info = models.TextField(
        help_text='Description of Vacancy'
    )
    requirements = models.TextField(
        help_text='Requirements of Vacancy'
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Salary for this vacancy',
        validators=[
            MinValueValidator(0.01)
        ]
    )

    def clean(self):
        super().clean()
        if self.salary <= 0:
            raise ValidationError({'salary': 'Salary for vacancy must be positive decimal number!'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('vacancy-detail', args=[str(self.id)])

    class Meta:
        ordering = ['title']
        constraints = [
            UniqueConstraint(
                Lower('title'),
                name='title_case_insensitive_unique',
                violation_error_message = "Title for vacancy already exists (case insensitive match)"
            ),
        ]

class Review(BaseDateModel):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        help_text='Review\'s user'
    )
    review = models.CharField(
        max_length=500,
        help_text='User\'s review'
    )
    grade = models.PositiveIntegerField(
        default=5,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
        help_text='User\'s grade'
    )

    def display_username(self):
        return self.user.username
    
    def clean(self):
        super().clean()
        if self.grade < 1 or self.grade > 5:
            raise ValidationError({'grade': 'Grade for review must be in range from 1 to 5!'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.display_username()}: {self.review}'
    
    def get_absolute_url(self):
        return reverse('review-detail', args=[str(self.id)])

    class Meta:
        ordering = ['-created_at']

class AppPermissions(models.Model):
    class Meta:
        managed = False
        permissions = (
            ('employee_perm', 'Employee permissions'),
            ('client_perm', 'Client permissions')
        )
