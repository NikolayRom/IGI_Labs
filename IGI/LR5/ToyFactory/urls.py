from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^$', views.index, name='index'),

    re_path(r'^citys/$', views.CityListView.as_view(), name='citys'),
    re_path(r'^city/(?P<pk>\d+)$', views.CityDetailView.as_view(), name='city-detail'),
    re_path(r'^city/create/$', views.CityCreate.as_view(), name='city_create'),
    re_path(r'^city/(?P<pk>\d+)/update/$', views.CityUpdate.as_view(), name='city_update'),
    re_path(r'^city/(?P<pk>\d+)/delete/$', views.CityDelete.as_view(), name='city_delete'),

    re_path(r'^products/$', views.ProductListView.as_view(), name='products'),
    re_path(r'^product/(?P<pk>\d+)$', views.ProductDetailView.as_view(), name='product-detail'),
    re_path(r'^product/create/$', views.ProductCreate.as_view(), name='product_create'),
    re_path(r'^product/(?P<pk>\d+)/update/$', views.ProductUpdate.as_view(), name='product_update'),
    re_path(r'^product/(?P<pk>\d+)/delete/$', views.ProductDelete.as_view(), name='product_delete'),

    re_path(r'^product_types/$', views.ProductTypeListView.as_view(), name='product_types'),
    re_path(r'^product_type/(?P<pk>\d+)$', views.ProductTypeDetailView.as_view(), name='product_type-detail'),
    re_path(r'^product_type/create/$', views.ProductTypeCreate.as_view(), name='product_type_create'),
    re_path(r'^product_type/(?P<pk>\d+)/update/$', views.ProductTypeUpdate.as_view(), name='product_type_update'),
    re_path(r'^product_type/(?P<pk>\d+)/delete/$', views.ProductTypeDelete.as_view(), name='product_type_delete'),

    re_path(r'^product_models/$', views.ProductModelListView.as_view(), name='product_models'),
    re_path(r'^product_model/(?P<pk>\d+)$', views.ProductModelDetailView.as_view(), name='product_model-detail'),
    re_path(r'^product_model/create/$', views.ProductModelCreate.as_view(), name='product_model_create'),
    re_path(r'^product_model/(?P<pk>\d+)/update/$', views.ProductModelUpdate.as_view(), name='product_model_update'),
    re_path(r'^product_model/(?P<pk>\d+)/delete/$', views.ProductModelDelete.as_view(), name='product_model_delete'),

    re_path(r'^clients/$', views.ClientListView.as_view(), name='clients'),
    re_path(r'^client/(?P<pk>\d+)$', views.ClientDetailView.as_view(), name='client-detail'),
    re_path(r'^client/create/$', views.ClientCreate.as_view(), name='client_create'),
    re_path(r'^client/(?P<pk>\d+)/update/$', views.ClientUpdate.as_view(), name='client_update'),
    re_path(r'^client/(?P<pk>\d+)/delete/$', views.ClientDelete.as_view(), name='client_delete'),

    re_path(r'^orders/$', views.OrderListView.as_view(), name='orders'),
    re_path(r'^order/(?P<pk>\d+)$', views.OrderDetailView.as_view(), name='order-detail'),
    re_path(r'^order/create/$', views.OrderCreate.as_view(), name='order_create'),
    re_path(r'^order/(?P<pk>\d+)/update/$', views.OrderUpdate.as_view(), name='order_update'),
    re_path(r'^order/(?P<pk>\d+)/delete/$', views.OrderDelete.as_view(), name='order_delete'),

    re_path(r'^pick-up_points/$', views.PickUpPointListView.as_view(), name='pick-up_points'),
    re_path(r'^pick-up_point/(?P<pk>\d+)$', views.PickUpPointDetailView.as_view(), name='pick-up_point-detail'),
    re_path(r'^pick-up_point/create/$', views.PickUpPointCreate.as_view(), name='pick-up_point_create'),
    re_path(r'^pick-up_point/(?P<pk>\d+)/update/$', views.PickUpPointUpdate.as_view(), name='pick-up_point_update'),
    re_path(r'^pick-up_point/(?P<pk>\d+)/delete/$', views.PickUpPointDelete.as_view(), name='pick-up_point_delete'),

    re_path(r'^phones/$', views.PhoneListView.as_view(), name='phones'),
    re_path(r'^phone/(?P<pk>\d+)$', views.PhoneDetailView.as_view(), name='phone-detail'),
    re_path(r'^phone/create/$', views.PhoneCreate.as_view(), name='phone_create'),
    re_path(r'^phone/(?P<pk>\d+)/update/$', views.PhoneUpdate.as_view(), name='phone_update'),
    re_path(r'^phone/(?P<pk>\d+)/delete/$', views.PhoneDelete.as_view(), name='phone_delete'),

    re_path(r'^promos/$', views.PromoListView.as_view(), name='promos'),
    re_path(r'^promo/(?P<pk>\d+)$', views.PromoDetailView.as_view(), name='promo-detail'),
    re_path(r'^promo/create/$', views.PromoCreate.as_view(), name='promo_create'),
    re_path(r'^promo/(?P<pk>\d+)/update/$', views.PromoUpdate.as_view(), name='promo_update'),
    re_path(r'^promo/(?P<pk>\d+)/delete/$', views.PromoDelete.as_view(), name='promo_delete'),

    re_path(r'^employees/$', views.EmployeeListView.as_view(), name='employees'),
    re_path(r'^employee/(?P<pk>\d+)$', views.EmployeeDetailView.as_view(), name='employee-detail'),
    re_path(r'^employee/create/$', views.EmployeeCreate.as_view(), name='employee_create'),
    re_path(r'^employee/(?P<pk>\d+)/update/$', views.EmployeeUpdate.as_view(), name='employee_update'),
    re_path(r'^employee/(?P<pk>\d+)/delete/$', views.EmployeeDelete.as_view(), name='employee_delete'),
]