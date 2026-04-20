import datetime
from django.test import TestCase
from django.utils import timezone
from ToyFactory.models import *
from ToyFactory.forms import *
from decimal import Decimal

class FormTestBase(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="Minsk")
        self.phone_obj = Phone.objects.create(phone="+375 (29) 111-11-11")
        self.p_model = ProductModel.objects.create(name="ModelX")
        self.product = Product.objects.create(name="Bear", price=10, product_model=self.p_model)
        self.point = PickUpPoint.objects.create(city=self.city, address="Street 1")
        
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password", birth_date=date(2000, 1, 1), email="old@mail.com"
        )

class UserAndProfileFormsTest(FormTestBase):
    def test_custom_user_creation_form(self):
        data = {
            'username': 'newuser',
            'birth_date': '01.01.2000',
            'password1': 'laba2026',
            'password2': 'laba2026',
        }
        form = CustomUserCreationForm(data=data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'newuser')

    def test_client_registration_form_invalid_phone(self):
        data = {
            'username': 'client1',
            'birth_date': '01.01.2000',
            'password1': 'pass123',
            'password2': 'pass123',
            'company_name': 'MyCompany',
            'phone': '12345',
            'address': 'Address',
            'city': self.city.id
        }
        form = ClientRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

class AdminAndUpdateFormsTest(FormTestBase):
    def test_employee_admin_form_email_duplicate(self):
        other_user = CustomUser.objects.create_user(
            username="other", birth_date=date(1990, 1, 1), email="busy@mail.com"
        )
        data = {
            'user': self.user.id,
            'email': 'busy@mail.com', 
            'info': 'Some info',
            'phone': self.phone_obj.id
        }
        form = EmployeeAdminForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_client_update_form_initial_and_save(self):
        client_prof = Client.objects.create(
            user=self.user, company_name="OldComp", phone=self.phone_obj, address="OldAddr", city=self.city
        )
        data = {
            'company_name': 'NewComp',
            'phone': '+375 (29) 999-99-99', 
            'address': 'NewAddr',
            'city': self.city.id
        }
        form = ClientUpdateForm(data=data, instance=client_prof)
        self.assertTrue(form.is_valid())
        form.save()
        client_prof.refresh_from_db()
        self.assertEqual(client_prof.company_name, 'NewComp')
        self.assertEqual(client_prof.phone.phone, '+375 (29) 999-99-99')

class ReviewAndOrderFormsTest(FormTestBase):
    def test_review_form_invalid_grade(self):
        form = ReviewForm(data={'review': 'Bad', 'grade': 10}, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('grade', form.errors)

    def test_order_create_form_promo_mismatch(self):
        other_product = Product.objects.create(name="Other", price=5, product_model=self.p_model)
        promo = Promo.objects.create(info="Sale", sale=Decimal('0.1'), product=other_product)
        
        client_prof = Client.objects.create(
            user=self.user, company_name="C", phone=self.phone_obj, address="A", city=self.city
        )
        
        data = {
            'product': self.product.id,
            'product_amount': 1,
            'promo': promo.id, 
            'pick_up_point': self.point.id
        }
        form = OrderCreateForm(data=data, client=client_prof)
        self.assertFalse(form.is_valid())
        self.assertIn('promo', form.errors)