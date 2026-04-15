from django.db import models
import uuid  
from datetime import date 
import re
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, Permission
from django.conf import settings

class CustomUser(AbstractUser):
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

        if self.age < 18:
            raise ValidationError({'birth_date': 'Age must be 18 or older'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return AbstractUser.__str__(self)

class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, help_text="Unique ID for product")
    name = models.CharField(max_length=100, default='product-'+str(uuid.uuid4()), help_text='Name for product')
    product_type = models.ManyToManyField('ProductType', help_text='Type for product')
    product_model = models.ForeignKey('ProductModel', on_delete=models.CASCADE, null=True, help_text='Model for product')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price for product')
    
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
        return ' ,'.join(str(product_type) for product_type in self.product_type.all()[:3])
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
        ordering = ['product_model', 'name']
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='product_name_case_insensitive_unique',
                violation_error_message = "Name already exists (case insensitive match)"
            ),
        ]

class ProductType(models.Model):
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

class ProductModel(models.Model):
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

class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, help_text='Employee\'s unique ID')

    def display_username(self):
        return self.user.username
    
    def clean(self):
        super().clean()
        if Client.objects.filter(user__exact=self.user).exists() or self.user.is_superuser:
            raise ValidationError('This user is not available!')
        
    def save(self, *args, **kwargs):
        self.full_clean()
        self.user.user_permissions.add(Permission.objects.get(codename='employee_perm'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Employee: {self.display_username()}"
    
    def get_absolute_url(self):
        return reverse('employee-detail', args=[str(self.id)])

class Client(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile',
    )
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, help_text="Client\'s unique ID")
    company_name = models.CharField(max_length=100, help_text='Client\'s company name')
    phone = models.OneToOneField('Phone', on_delete=models.CASCADE, null=True, help_text='Client\'s phone')
    address = models.CharField(max_length=100, help_text='Client\'s address')
    
    def clean(self):
        super().clean()
        if self.user.is_superuser or Employee.objects.filter(user__exact=self.user).exists():
            raise ValidationError('This user is not available!')
        elif not self.company_name.strip():
            raise ValidationError({'company_name': 'Company name must be initialize'})
        elif not self.address.strip():
            raise ValidationError({'address': 'Address must be initialize'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        self.user.user_permissions.add(Permission.objects.get(codename='client_perm'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Client: {self.company_name} ({self.phone}) - {self.address}"
    
    def get_absolute_url(self):
        return reverse('client-detail', args=[str(self.id)])

    class Meta:
        ordering = ['company_name']
        constraints = [
            UniqueConstraint(
                Lower('company_name'),
                name='company_name_case_insensitive_unique',
                violation_error_message = "Company name already exists (case insensitive match)"
            ),
        ]

class Order(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, help_text="Unique ID for order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, help_text='Client order of product')
    date_order_create = models.DateField(default=date.today, editable=False, help_text='Date of create order')
    date_order_complete = models.DateField(null=True, blank=True, help_text='Date of complete order')
    product_amount = models.PositiveIntegerField(default=1, help_text='Amount of products in order')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, help_text='Client of order')

    @property
    def product_name(self):
        return self.product.name if self.product else None
    
    @property
    def client_company(self):
        return self.client.company_name if self.client else None

    def clean(self):
        super().clean()
        if self.product_amount == 0:
            raise ValidationError({'product_amount': 'Amount of products must be positive number (not zero!)'})
        elif self.date_order_create > date.today():
            raise ValidationError({'date_order_create': 'Date of creating order must be today or past, not future'})
        elif self.date_order_complete != None and (self.date_order_complete > date.today() or self.date_order_complete < self.date_order_create):
            raise ValidationError({'date_order_complete': 'End date must be greater than date of create and not be future'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order: <{self.product_amount}> {self.product_name} ({self.date_order_create}-{self.date_order_complete}) by {self.client_company}'
    
    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])

    class Meta:
        ordering = ['date_order_create', 'client', 'product', 'product_amount']

class City(models.Model):
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

class PickUpPoint(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, help_text="Unique ID for pick-up point")
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, help_text='City of pick-up point')
    address = models.CharField(max_length=100, help_text='Address of pick-up point')

    def clean(self):
        super().clean()
        if not self.address.strip():
            raise ValidationError({'address': 'Address must be initialize'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Pick-up point: {self.city} - {self.address}'
    
    def get_absolute_url(self):
        return reverse('pickUpPoint-detail', args=[str(self.id)])

    class Meta:
        ordering = ['city', 'address']

class Phone(models.Model):
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

class Promo(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, help_text="Unique ID for phone")
    info = models.CharField(
        max_length=50,
        default='Promo code for any orders',
        help_text='Promo code for clients'
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, help_text='Client\'s promo code')
    sale = models.DecimalField(max_digits=3, decimal_places=2, default=0.1, help_text='Sale for order')

    def clean(self):
        super().clean()
        if self.sale > 1.0 or self.sale < 0.0:
            raise ValidationError({'sale': 'Sale for client must be 0 <= sale <= 1'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.info
    
    def get_absolute_url(self):
        return reverse('promo-detail', args=[str(self.id)])

    class Meta:
        ordering = ['client', 'sale']

class AppPermissions(models.Model):
    class Meta:
        managed = False
        permissions = (('employee_perm', 'Employee permissions'), ('client_perm', 'Client permissions'))
