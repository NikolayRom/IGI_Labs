from . import views
from django.urls import re_path, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    re_path(r'^home/$', views.index, name='index'),
    re_path(r'^$', RedirectView.as_view(url='home/')),
    re_path(r'^about/$', views.about, name='about'),
    re_path(r'^news/$', views.NewsListView.as_view(), name='news'),
    re_path(r'^news/(?P<pk>[0-9a-f-]+)$', views.NewsDetailView.as_view(), name='news-detail'),
    re_path(r'^faq/$', views.FAQListView.as_view(), name='faq'),
    re_path(r'^faq/(?P<pk>[0-9a-f-]+)$', views.FAQDetailView.as_view(), name='faq-detail'),
    re_path(r'^contacts/$', views.EmployeeListView.as_view(), name='contacts'),
    re_path(r'^contacts/(?P<pk>[0-9a-f-]+)$', views.EmployeeDetailView.as_view(), name='contacts-detail'),
    re_path(r'^privacy_policy/$', views.privacy_policy, name='privacy_policy'),
    re_path(r'^vacancys/$', views.VacancyListView.as_view(), name='vacancys'),
    re_path(r'^vacancy/(?P<pk>[0-9a-f-]+)$', views.VacancyDetailView.as_view(), name='vacancy-detail'),
    re_path(r'^reviews/$', views.reviews, name='reviews'),
    re_path(r'^promos/$', views.PromoListView.as_view(), name='promos'),
    re_path(r'^promo/(?P<pk>[0-9a-f-]+)$', views.PromoDetailView.as_view(), name='promo-detail'),
    re_path(r'^products/$', views.ProductListView.as_view(), name='products'),
    re_path(r'^product/(?P<pk>[0-9a-f-]+)$', views.ProductDetailView.as_view(), name='product-detail'),
    re_path(r'^product/create/$', views.ProductCreateView.as_view(), name='product-create'),
    re_path(r'^product/(?P<pk>[0-9a-f-]+)/update/$', views.ProductUpdateView.as_view(), name='product-update'),
    re_path(r'^product/(?P<pk>[0-9a-f-]+)/delete/$', views.ProductDeleteView.as_view(), name='product-delete'),
    re_path(r'^product_type/create/$', views.ProductTypeCreateView.as_view(), name='product_type-create'),
    re_path(r'^product_model/create/$', views.ProductModelCreateView.as_view(), name='product_model-create'),
    re_path(r'^clients/$', views.ClientListView.as_view(), name='clients'),
    re_path(r'^client/(?P<pk>[0-9a-f-]+)$', views.ClientDetailView.as_view(), name='client-detail'),
    re_path(r'^cities/$', views.CityListView.as_view(), name='cities'),
    re_path(r'^city/(?P<pk>[0-9a-f-]+)$', views.CityDetailView.as_view(), name='city-detail'),
    re_path(r'^pick_up_point/(?P<pk>[0-9a-f-]+)$', views.PickUpPointDetailView.as_view(), name='pick_up_point-detail'),
    re_path(r'^client/cart/$', views.order_create, name='cart'),
    re_path(r'^client/cart/order/(?P<pk>[0-9a-f-]+)/delete/$', views.OrderDeleteView.as_view(), name='order-delete'),
    re_path(r'^client/cart/complete$', views.order_complete, name='orders-complete'),
    re_path(r'^client/orders/$', views.OrderClientListView.as_view(), name='client-orders')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)