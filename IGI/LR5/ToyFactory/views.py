from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import transaction
from django.contrib.auth.decorators import login_required, permission_required

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

@permission_required('ToyFactory.client_perm')
@login_required
def order_create(request):

    client = request.user.client_profile

    if request.method == 'POST':
        form = OrderCreateForm(request.POST, client=client)
        if form.is_valid():
            form.save()
            return redirect('cart')
    else:
        form = OrderCreateForm(client=client)

    order_list = Order.objects.filter(client=client, date_order_complete__isnull=True).all().order_by('-date_order_create')

    context={
        'form': form,
        'order_list': order_list,
        'total': sum(order.get_total for order in order_list)
    }
    return render(
        request,
        'cart.html',
        context=context
    )

@permission_required('ToyFactory.client_perm')
@login_required
def order_complete(request):

    if request.method == 'POST':
        Order.objects.filter(client=request.user.client_profile, date_order_complete__isnull=True).update(date_order_complete=timezone.now())
        return redirect('client-orders')
    return redirect('cart')

class OrderClientListView(generic.ListView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Order
    paginate_by = 10
    template_name = 'ToyFactory/client_orders_list.html'
    permission_required = 'ToyFactory.client_perm'
    def get_queryset(self):
        return Order.objects.filter(client=self.request.user.client_profile, date_order_complete__isnull=False)
    
class OrderDeleteView(DeleteView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Order
    permission_required = 'ToyFactory.client_perm'
    success_url = reverse_lazy('cart')

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

class ClientListView(generic.ListView):
    model = Client
    paginate_by = 10

class ClientDetailView(generic.DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_list'] = self.get_object().order_set.filter(date_order_complete__isnull=False)
        return context

class VacancyListView(generic.ListView):
    model = Vacancy
    paginate_by = 10

class VacancyDetailView(generic.DetailView):
    model = Vacancy

class ProductTypeCreateView(CreateView):
    model = ProductType
    fields = '__all__'
    success_url = reverse_lazy('products')

class ProductModelCreateView(CreateView):
    model = ProductModel
    fields = '__all__'
    success_url = reverse_lazy('products')

class CityListView(generic.ListView):
    model = City
    paginate_by = 10

class CityDetailView(generic.DetailView):
    model = City

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pickuppoint_list'] = self.get_object().pickuppoint_set.all()
        return context

class PickUpPointDetailView(generic.DetailView):
    model = PickUpPoint

'''
CRUD: Product Model
'''
class ProductListView(generic.ListView):
    model = Product
    paginate_by = 10

class ProductDetailView(generic.DetailView):
    model = Product

class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('products')

class ProductUpdateView(UpdateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('products')

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('products')
