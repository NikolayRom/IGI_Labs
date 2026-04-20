import datetime
from unittest.mock import patch
from django.test import TestCase, Client as HttpClient
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from ToyFactory.models import *

class ViewTestBase(TestCase):
    def setUp(self):
        self.client = HttpClient()
        self.city = City.objects.create(name="Minsk")
        self.phone = Phone.objects.create(phone="+375 (29) 111-22-33")
        self.user_client = CustomUser.objects.create_user(
            username="client_user", password="password", birth_date=datetime.date(2000, 1, 1), email="c@c.com"
        )
        self.client_profile = Client.objects.create(
            user=self.user_client, company_name="TestCorp", phone=self.phone, address="Addr", city=self.city
        )
        
        self.admin = CustomUser.objects.create_superuser(
            username="admin", password="password", birth_date=datetime.date(1990, 1, 1), email="a@a.com"
        )
        
        self.product_model = ProductModel.objects.create(name="Model")
        self.product = Product.objects.create(name="Doll", price=Decimal("10.00"), product_model=self.product_model)
        self.point = PickUpPoint.objects.create(city=self.city, address="Point 1")

class PublicViewsTest(ViewTestBase):
    @patch('requests.get')
    def test_index_view(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'articles': []}
        
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_about_view(self):
        AboutInfo.objects.create(header="H", info="I")
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_reviews_view_get(self):
        response = self.client.get(reverse('reviews'))
        self.assertEqual(response.status_code, 200)

class OrderAndCartTest(ViewTestBase):
    def test_cart_access_denied_for_anonymous(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 302) 

    def test_cart_view_and_order_create(self):
        self.client.login(username="client_user", password="password")
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        
        data = {
            'product': self.product.id,
            'product_amount': 2,
            'pick_up_point': self.point.id,
        }
        response = self.client.post(reverse('cart'), data)
        self.assertEqual(Order.objects.filter(client=self.client_profile).count(), 1)
        self.assertRedirects(response, reverse('cart'))

    def test_order_complete_checkout(self):
        self.client.login(username="client_user", password="password")
        Order.objects.create(
            product=self.product, product_amount=1, client=self.client_profile, 
            pick_up_point=self.point, date_order_create=timezone.now()
        )
        response = self.client.post(reverse('orders-complete'))
        self.assertTrue(Order.objects.filter(date_order_complete__isnull=False).exists())

class AnalyticsViewTest(ViewTestBase):
    def test_analytics_restricted_to_superuser(self):
        self.client.login(username="client_user", password="password")
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, 302)

    def test_analytics_superuser_access(self):
        self.client.login(username="admin", password="password")
        Order.objects.create(
            product=self.product, product_amount=5, client=self.client_profile, 
            pick_up_point=self.point, date_order_create=timezone.now(),
            date_order_complete=timezone.now()
        )
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('chart', response.context)

class ListViewTest(ViewTestBase):
    def test_news_view(self): 
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)

    def test_faq_view(self): 
        response = self.client.get(reverse('faq'))
        self.assertEqual(response.status_code, 200)

    def test_contacts_view(self): 
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)

    def test_contacts_view(self): 
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)

    def test_vacancys_view(self): 
        response = self.client.get(reverse('vacancys'))
        self.assertEqual(response.status_code, 200)

    def test_promos_view(self): 
        response = self.client.get(reverse('promos'))
        self.assertEqual(response.status_code, 200)

    def test_products_view(self): 
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)

    def test_clients_view(self): 
        response = self.client.get(reverse('clients'))
        self.assertEqual(response.status_code, 200)

    def test_cities_view(self): 
        response = self.client.get(reverse('cities'))
        self.assertEqual(response.status_code, 200)