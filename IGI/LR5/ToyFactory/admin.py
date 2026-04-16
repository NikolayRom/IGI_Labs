from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import *

class CustomUserAdmin(UserAdmin):
    list_display = [
        'username',
        'email',
        'birth_date',
        'is_staff',
        'is_superuser'
    ]

    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info:', {'fields': ('birth_date',)},),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info:', {"fields": ("birth_date",)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_product_type', 'product_model', 'price']
    list_filter = ['name', 'product_model', 'price']

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'phone', 'address']
    list_filter = ['company_name']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('user',) 
        return ()

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeAdminForm
    list_display = ['display_username', 'display_email', 'phone', 'user']
    list_filter = ['user']

    def get_readonly_fields(self, request, obj =None):
        if obj:
            return ('user',)
        return ()

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['client_company', 'product_name', 'product_amount', 'date_order_create', 'date_order_complete']
    list_filter = ['client__company_name', 'product__name', 'product_amount', 'date_order_create']

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']

@admin.register(PickUpPoint)
class PickUpPointAdmin(admin.ModelAdmin):
    list_display = ['city', 'address']
    list_filter = ['city', 'address']

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ['phone']
    list_filter = ['phone']

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ['info', 'sale', 'end_date']
    list_filter = ['info', 'sale', 'end_date']

@admin.register(AboutInfo)
class AboutInfoAdmin(admin.ModelAdmin):
    list_display = ['header', 'info', 'pub_date']
    list_filter = ['header', 'info', 'pub_date']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['header', 'info', 'pub_date']
    list_filter = ['header', 'info', 'pub_date']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'pub_date']
    list_filter = ['question', 'answer', 'pub_date']

