from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import transaction

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
    form = ClientRegistrationForm()
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                login(request, user)
                return redirect('index')
    context = {'form': form}
    return render(request, 'registration/register.html', context=context)

'''
CRUD: City Model
'''
class CityListView(generic.ListView):
    model = City
    paginate_by = 10

class CityDetailView(generic.DetailView):
    model = City

class CityCreate(CreateView):
    model = City
    fields = '__all__'

class CityUpdate(UpdateView):
    model = City
    fields = '__all__'

class CityDelete(DeleteView):
    model = City
    success_url = reverse_lazy('citys')

'''
CRUD: Product Model
'''
class ProductListView(generic.ListView):
    model = Product
    paginate_by = 10

class ProductDetailView(generic.DetailView):
    model = Product

class ProductCreate(CreateView):
    model = Product
    fields = '__all__'

class ProductUpdate(UpdateView):
    model = Product
    fields = '__all__'

class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('products')

'''
CRUD: ProductType Model
'''
class ProductTypeListView(generic.ListView):
    model = ProductType
    paginate_by = 10

class ProductTypeDetailView(generic.DetailView):
    model = ProductType

class ProductTypeCreate(CreateView):
    model = ProductType
    fields = '__all__'

class ProductTypeUpdate(UpdateView):
    model = ProductType
    fields = '__all__'

class ProductTypeDelete(DeleteView):
    model = ProductType
    success_url = reverse_lazy('product_types')

'''
CRUD: ProductModel Model
'''
class ProductModelListView(generic.ListView):
    model = ProductModel
    paginate_by = 10

class ProductModelDetailView(generic.DetailView):
    model = ProductModel

class ProductModelCreate(CreateView):
    model = ProductModel
    fields = '__all__'

class ProductModelUpdate(UpdateView):
    model = ProductModel
    fields = '__all__'

class ProductModelDelete(DeleteView):
    model = ProductModel
    success_url = reverse_lazy('product_models')

'''
CRUD: Client Model
'''
class ClientListView(generic.ListView):
    model = Client
    paginate_by = 10

class ClientDetailView(generic.DetailView):
    model = Client

class ClientCreate(CreateView):
    model = Client
    fields = '__all__'

class ClientUpdate(UpdateView):
    model = Client
    fields = '__all__'

class ClientDelete(DeleteView):
    model = Client
    success_url = reverse_lazy('clients')

'''
CRUD: Order Model
'''
class OrderListView(generic.ListView):
    model = Order
    paginate_by = 10

class OrderDetailView(generic.DetailView):
    model = Order

class OrderCreate(CreateView):
    model = Order
    fields = '__all__'

class OrderUpdate(UpdateView):
    model = Order
    fields = '__all__'

class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders')

'''
CRUD: PickUpPoint Model
'''
class PickUpPointListView(generic.ListView):
    model = PickUpPoint
    paginate_by = 10

class PickUpPointDetailView(generic.DetailView):
    model = PickUpPoint

class PickUpPointCreate(CreateView):
    model = PickUpPoint
    fields = '__all__'

class PickUpPointUpdate(UpdateView):
    model = PickUpPoint
    fields = '__all__'

class PickUpPointDelete(DeleteView):
    model = PickUpPoint
    success_url = reverse_lazy('pick-up_points')

'''
CRUD: Phone Model
'''
class PhoneListView(generic.ListView):
    model = Phone
    paginate_by = 10

class PhoneDetailView(generic.DetailView):
    model = Phone

class PhoneCreate(CreateView):
    model = Phone
    fields = '__all__'

class PhoneUpdate(UpdateView):
    model = Phone
    fields = '__all__'

class PhoneDelete(DeleteView):
    model = Phone
    success_url = reverse_lazy('phones')

'''
CRUD: Promo Model
'''
class PromoListView(generic.ListView):
    model = Promo
    paginate_by = 10

class PromoDetailView(generic.DetailView):
    model = Promo

class PromoCreate(CreateView):
    model = Promo
    fields = '__all__'

class PromoUpdate(UpdateView):
    model = Promo
    fields = '__all__'

class PromoDelete(DeleteView):
    model = Promo
    success_url = reverse_lazy('promos')

'''
CRUD: Employee Model
'''
class EmployeeListView(generic.ListView):
    model = Employee
    paginate_by = 10

class EmployeeDetailView(generic.DetailView):
    model = Employee

class EmployeeCreate(CreateView):
    model = Employee
    fields = '__all__'

class EmployeeUpdate(UpdateView):
    model = Employee
    fields = '__all__'

class EmployeeDelete(DeleteView):
    model = Employee
    success_url = reverse_lazy('employees')
