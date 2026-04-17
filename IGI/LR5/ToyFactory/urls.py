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
    re_path(r'^promo/(?P<pk>[0-9a-f-]+)$', views.PromoDetailView.as_view(), name='promo-detail')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)