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
from django.db.models import Sum, F, Case, When, DecimalField
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.functions import Coalesce
from decimal import Decimal
import requests

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from django.db.models.functions import TruncMonth

import logging
logger = logging.getLogger('ToyFactory')

def index(request):
    
    api_key = '90a48ee7dbca43028bde1930c1da9870'
    api_theme = 'toys'
    api_from_date = date.today() - datetime.timedelta(days=7)
    api_language = 'en'
    api_path = f'https://newsapi.org/v2/everything?q="{api_theme}"&from={api_from_date}&language={api_language}&sortBy=popularity&apiKey={api_key}'
    api_max_news = 3

    articles = []

    try:
        api_response = requests.get(api_path)
        if api_response.status_code == 200:
            data = api_response.json()
            articles = data.get('articles', [])[:api_max_news]
            logger.info(f"Index view: API success: {api_path}")
    except Exception as e:
        print('Error during request to API:' + e)
        logger.error(f"Index view: API Error: {api_path}. Error: {e}")

    context = {'api_data': articles}

    if News.objects.last() != None:
        context['last_news'] = News.objects.last()
    else:
        logger.warning(f"Index view: News.objects.last() not found!")
    
    return render(
        request,
        'index.html',
        context=context
    )

def account(request):
    form = UserUpdateForm(instance=request.user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            logger.error(f"Account view: Form Error: form = UserUpdateForm")
    
    context = {'form': form}
    return render(request, 'registration/account.html', context=context)

def client_profile(request):
    client = Client.objects.filter(user__exact=request.user).first()
    if client == None:
        logger.warning(f"client_profile view: client warning: client not found!")
    form = ClientUpdateForm(instance=client)
    if request.method == 'POST':
        form = ClientUpdateForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client-profile')
        else:
            logger.error(f"client_profile view: form Error: ClientUpdateForm is not valid!")
    
    context = {
        'form': form,
        'client': client
    }
    return render(request, 'registration/client_profile.html', context=context)

def employee_profile(request):
    employee = Employee.objects.filter(user__exact=request.user).first()
    if employee == None:
        logger.warning(f"employee_profile view: employee warning: employee not found!")
    form = EmployeeUpdateForm(instance=employee)
    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee-profile')
        else:
            logger.error(f"employee_profile view: form Error: EmployeeUpdateForm is not valid!")
    
    context = {
        'form': form,
        'employee': employee
    }
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
        else:
            logger.error(f"register view: register Error: ClientRegistrationForm is not valid!")
    context = {'form': form}
    return render(request, 'registration/register.html', context=context)

def about(request):

    context = {}

    if(AboutInfo.objects.last() != None):
        context['about_info'] = AboutInfo.objects.last()
    else:
        logger.warning(f"about view: AboutInfo warning: AboutInfo.objects.last() not found!")

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
            logger.info(f"Reviews view: redirect: user is not authenticated")
            return redirect('login')
        form = ReviewForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('reviews')
        else:
            logger.error(f"Reviews view: form Error: Review form is not valid!")
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

    if client == None:
        logger.warning(f"Order create view: client warning: request.user.client_profile not found!")

    if request.method == 'POST':
        form = OrderCreateForm(request.POST, client=client)
        if form.is_valid():
            form.save()
            return redirect('cart')
        else:
            logger.error(f"Order create view: form Error: OrderCreateForm is not valid!")
    else:
        form = OrderCreateForm(client=client)

    order_list = Order.objects.filter(client=client, date_order_complete__isnull=True).all().order_by('-date_order_create')

    if order_list == None:
        logger.warning(f"Order create view: order_list warning: Order.objects.filter(client=client, date_order_complete__isnull=True).all().order_by('-date_order_create') not found!")

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
    logger.info(f"Order complete view: redirect to cart: request.method != POST")
    return redirect('cart')


def get_plot():
    monthly_sales = Order.objects.filter(date_order_complete__isnull=False) \
        .annotate(month=TruncMonth('date_order_complete')) \
        .values('month') \
        .annotate(total = Coalesce(
                Sum(
                    Case(
                        When(
                            promo__isnull=False,
                            then=(
                                F('product_amount') * F('product__price') * (Decimal('1') - F('promo__sale'))
                            )
                        ),
                        default=F('product_amount') * F('product__price'),
                        output_field=DecimalField()
                    )
                ),
                Decimal('0'),
                output_field=DecimalField()
            )) \
        .order_by('month')

    if not monthly_sales:
        logger.warning(f"monthly_sales not found!")
        return None, 0

    x_data = list(range(1, len(monthly_sales) + 1))
    y_data = [float(item['total']) for item in monthly_sales]
    labels = [item['month'].strftime('%b %Y') for item in monthly_sales]

    n = len(x_data)
    sum_x = sum(x_data)
    sum_y = sum(y_data)
    sum_xx = sum(x**2 for x in x_data)
    sum_xy = sum(x*y for x, y in zip(x_data, y_data))

    a = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2) if (n * sum_xx - sum_x**2) != 0 else 0
    b = (sum_y - a * sum_x) / n

    trend_y = [a * x + b for x in x_data]
    forecast = a * (n + 1) + b 

    plt.figure(figsize=(8, 4))
    plt.plot(labels, y_data, marker='o', label='Sales')
    plt.plot(labels, trend_y, linestyle='--', color='red', label='Linear trend')
    plt.title('Analytics and sales trend')
    plt.xlabel('Month')
    plt.ylabel('Income')
    plt.legend()
    plt.grid(True)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close() 
    
    return image_base64, round(forecast, 2)

def generate_bar_chart(labels, values, title, color):
    
    if not labels or not values:
        logger.warning(f"labels or values not found!")
        return None
    
    plt.figure(figsize=(8, 5))
    plt.barh(labels, [float(v) for v in values], color=color)
    plt.title(title)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()
    return image_base64

@login_required
def analytics_view(request):
    
    if request.user.is_superuser:

        product_popularity = Product.objects.filter(
            order__date_order_complete__gte=timezone.now()-timezone.timedelta(days=30)
        ).annotate(
            total_sum = Coalesce(Sum('order__product_amount'), 0)
        ).order_by('-total_sum')

        if not product_popularity:
            logger.warning(f"product_popularity not found!")

        worse_product = product_popularity.last()
        best_product = product_popularity.first()

        chart_image, forecast_value = get_plot()
        
        clients_report = Client.objects.filter(
            order__date_order_complete__gte=timezone.now()-timezone.timedelta(days=30)
        ).annotate(
            units = Coalesce(Sum('order__product_amount'), 0),
            income=Coalesce(
                Sum(
                    Case(
                        When(
                            order__promo__isnull=False,
                            then=(
                                F('order__product_amount') * F('order__product__price') * (Decimal('1') - F('order__promo__sale'))
                            )
                        ),
                        default=F('order__product_amount') * F('order__product__price'),
                        output_field=DecimalField()
                    )
                ),
                Decimal('0'),
                output_field=DecimalField()
            )
        ).order_by('-income')

        if not clients_report:
            logger.warning(f"clients_report not found!")

        products_report = Product.objects.filter(
                order__date_order_complete__gte=timezone.now()-timezone.timedelta(days=30)
        ).annotate(
            units = Coalesce(Sum('order__product_amount'), 0),
            income=Coalesce(
                Sum(
                    Case(
                        When(
                            order__promo__isnull=False,
                            then=(
                                F('order__product_amount') * F('price') * (Decimal('1') - F('order__promo__sale'))
                            )
                        ),
                        default=F('order__product_amount') * F('price'),
                        output_field=DecimalField()
                    )
                ),
                Decimal('0'),
                output_field=DecimalField()
            )
        ).order_by('-income')

        if not products_report:
            logger.warning(f"products_report not found!")

        client_names = [c.company_name for c in clients_report[:10]] 
        client_income = [c.income for c in clients_report[:10]]
        client_units = [c.units for c in clients_report[:10]]

        product_names = [p.name for p in products_report[:10]]
        product_income = [p.income for p in products_report[:10]]
        product_units = [p.units for p in products_report[:10]]

        chart_client_income = generate_bar_chart(client_names, client_income, 'Sales income by clients ($)', 'skyblue')
        chart_client_units = generate_bar_chart(client_names, client_units, 'Sales amount by clients (units)', 'lightgreen')
        
        chart_product_income = generate_bar_chart(product_names, product_income, 'Sales income by products ($)', 'salmon')
        chart_product_units = generate_bar_chart(product_names, product_units, 'Sales amount by products (units)', 'gold')

        context = {
            'chart': chart_image,
            'forecast': forecast_value,
            'clients_report': clients_report,
            'products_report': products_report,
            'worse_product': worse_product,
            'best_product': best_product,

            'chart_client_income': chart_client_income,
            'chart_client_units': chart_client_units,
            'chart_product_income': chart_product_income,
            'chart_product_units': chart_product_units,
        }
        return render(request, 'analytics.html', context)
    
    logger.info(f"Redirect to login: user is not superuser")
    return redirect('login')

class OrderClientListView(generic.ListView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Order
    paginate_by = 10
    template_name = 'ToyFactory/client_orders_list.html'
    permission_required = 'ToyFactory.client_perm'
    def get_queryset(self):
        orders = Order.objects.filter(client=self.request.user.client_profile, date_order_complete__isnull=False)

        if not orders:
            logger.warning(f"orders not found!")

        return orders
    
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
        order_list = self.get_object().order_set.filter(date_order_complete__isnull=False)
        if not order_list:
            logger.warning(f"order_list not found!")
        context['order_list'] = order_list
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
        pickuppoint_list = self.get_object().pickuppoint_set.all()
        if not pickuppoint_list:
            logger.warning(f"pickuppoint_list not found!")
        context['pickuppoint_list'] = pickuppoint_list
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
