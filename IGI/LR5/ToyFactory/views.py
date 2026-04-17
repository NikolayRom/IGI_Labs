from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import transaction
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def index(request):
    
    context = {}

    if News.objects.last() != None:
        context = {'last_news': News.objects.last()}
    
    return render(
        request,
        'index.html',
        context=context
    )

def account(request):
    form = UserUpdateForm(instance=request.user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        form.save()
        return redirect('index')
    
    context = {'form': form}
    return render(request, 'registration/account.html', context=context)

def client_profile(request):
    form = ClientUpdateForm(instance=Client.objects.filter(user__exact=request.user).first())
    if request.method == 'POST':
        form = ClientUpdateForm(request.POST, instance=Client.objects.filter(user__exact=request.user).first())
        if form.is_valid():
            form.save()
            return redirect('client-profile')
    
    context = {'form': form}
    return render(request, 'registration/client_profile.html', context=context)

def employee_profile(request):
    form = EmployeeUpdateForm(instance=Employee.objects.filter(user__exact=request.user).first())
    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, request.FILES, instance=Employee.objects.filter(user__exact=request.user).first())
        if form.is_valid():
            form.save()
            return redirect('employee-profile')
    
    context = {'form': form}
    return render(request, 'registration/employee_profile.html', context=context)

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

def about(request):
    context = {}
    if(AboutInfo.objects.last() != None):
        context = {'about_info': AboutInfo.objects.last()}
    return render(
        request,
        'about.html',
        context=context
    )

def privacy_policy(request):
    return render(
        request,
        'privacy_policy.html',
        context={}
    )

def reviews(request):

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = ReviewForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('reviews')
    else:
        form = ReviewForm()

    context={
        'form': form,
        'review_list': Review.objects.all()
    }
    return render(
        request,
        'reviews.html',
        context=context
    )

class PromoListView(generic.ListView):
    model = Promo
    paginate_by = 10

class PromoDetailView(generic.DetailView):
    model = Promo

class NewsListView(generic.ListView):
    model = News
    paginate_by = 10

class NewsDetailView(generic.DetailView):
    model = News

class FAQListView(generic.ListView):
    model = FAQ
    paginate_by = 10

class FAQDetailView(generic.DetailView):
    model = FAQ

class EmployeeListView(generic.ListView):
    model = Employee
    paginate_by = 10

class EmployeeDetailView(generic.DetailView):
    model = Employee

class VacancyListView(generic.ListView):
    model = Vacancy
    paginate_by = 10

class VacancyDetailView(generic.DetailView):
    model = Vacancy

# '''
# CRUD: City Model
# '''
# class CityListView(generic.ListView):
#     model = City
#     paginate_by = 10

# class CityDetailView(generic.DetailView):
#     model = City

# class CityCreate(CreateView):
#     model = City
#     fields = '__all__'

# class CityUpdate(UpdateView):
#     model = City
#     fields = '__all__'

# class CityDelete(DeleteView):
#     model = City
#     success_url = reverse_lazy('citys')

# '''
# CRUD: Product Model
# '''
# class ProductListView(generic.ListView):
#     model = Product
#     paginate_by = 10

# class ProductDetailView(generic.DetailView):
#     model = Product

# class ProductCreate(CreateView):
#     model = Product
#     fields = '__all__'

# class ProductUpdate(UpdateView):
#     model = Product
#     fields = '__all__'

# class ProductDelete(DeleteView):
#     model = Product
#     success_url = reverse_lazy('products')

# '''
# CRUD: ProductType Model
# '''
# class ProductTypeListView(generic.ListView):
#     model = ProductType
#     paginate_by = 10

# class ProductTypeDetailView(generic.DetailView):
#     model = ProductType

# class ProductTypeCreate(CreateView):
#     model = ProductType
#     fields = '__all__'

# class ProductTypeUpdate(UpdateView):
#     model = ProductType
#     fields = '__all__'

# class ProductTypeDelete(DeleteView):
#     model = ProductType
#     success_url = reverse_lazy('product_types')

# '''
# CRUD: ProductModel Model
# '''
# class ProductModelListView(generic.ListView):
#     model = ProductModel
#     paginate_by = 10

# class ProductModelDetailView(generic.DetailView):
#     model = ProductModel

# class ProductModelCreate(CreateView):
#     model = ProductModel
#     fields = '__all__'

# class ProductModelUpdate(UpdateView):
#     model = ProductModel
#     fields = '__all__'

# class ProductModelDelete(DeleteView):
#     model = ProductModel
#     success_url = reverse_lazy('product_models')

# '''
# CRUD: Client Model
# '''
# class ClientListView(generic.ListView):
#     model = Client
#     paginate_by = 10

# class ClientDetailView(generic.DetailView):
#     model = Client

# class ClientCreate(CreateView):
#     model = Client
#     fields = '__all__'

# class ClientUpdate(UpdateView):
#     model = Client
#     fields = '__all__'

# class ClientDelete(DeleteView):
#     model = Client
#     success_url = reverse_lazy('clients')

# '''
# CRUD: Order Model
# '''
# class OrderListView(generic.ListView):
#     model = Order
#     paginate_by = 10

# class OrderDetailView(generic.DetailView):
#     model = Order

# class OrderCreate(CreateView):
#     model = Order
#     fields = '__all__'

# class OrderUpdate(UpdateView):
#     model = Order
#     fields = '__all__'

# class OrderDelete(DeleteView):
#     model = Order
#     success_url = reverse_lazy('orders')

# '''
# CRUD: PickUpPoint Model
# '''
# class PickUpPointListView(generic.ListView):
#     model = PickUpPoint
#     paginate_by = 10

# class PickUpPointDetailView(generic.DetailView):
#     model = PickUpPoint

# class PickUpPointCreate(CreateView):
#     model = PickUpPoint
#     fields = '__all__'

# class PickUpPointUpdate(UpdateView):
#     model = PickUpPoint
#     fields = '__all__'

# class PickUpPointDelete(DeleteView):
#     model = PickUpPoint
#     success_url = reverse_lazy('pick-up_points')

# '''
# CRUD: Phone Model
# '''
# class PhoneListView(generic.ListView):
#     model = Phone
#     paginate_by = 10

# class PhoneDetailView(generic.DetailView):
#     model = Phone

# class PhoneCreate(CreateView):
#     model = Phone
#     fields = '__all__'

# class PhoneUpdate(UpdateView):
#     model = Phone
#     fields = '__all__'

# class PhoneDelete(DeleteView):
#     model = Phone
#     success_url = reverse_lazy('phones')

# '''
# CRUD: Promo Model
# '''
# class PromoListView(generic.ListView):
#     model = Promo
#     paginate_by = 10

# class PromoDetailView(generic.DetailView):
#     model = Promo

# class PromoCreate(CreateView):
#     model = Promo
#     fields = '__all__'

# class PromoUpdate(UpdateView):
#     model = Promo
#     fields = '__all__'

# class PromoDelete(DeleteView):
#     model = Promo
#     success_url = reverse_lazy('promos')

# '''
# CRUD: Employee Model
# '''
# class EmployeeListView(generic.ListView):
#     model = Employee
#     paginate_by = 10

# class EmployeeDetailView(generic.DetailView):
#     model = Employee

# class EmployeeCreate(CreateView):
#     model = Employee
#     fields = '__all__'

# class EmployeeUpdate(UpdateView):
#     model = Employee
#     fields = '__all__'

# class EmployeeDelete(DeleteView):
#     model = Employee
#     success_url = reverse_lazy('employees')
