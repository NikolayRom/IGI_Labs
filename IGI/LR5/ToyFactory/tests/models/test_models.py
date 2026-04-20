from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
from ToyFactory.models import *

class ModelTest(TestCase):

    def setUp(self):

        self.city = City.objects.create(name="Minsk")
        self.phone = Phone.objects.create(phone="+375 (29) 111-22-33")
        

        self.user = CustomUser.objects.create_user(
            username="testuser", 
            password="password", 
            birth_date=date(2000, 1, 1),
            email="test@test.com"
        )
        

        self.p_type = ProductType.objects.create(name="Toy")
        self.p_model = ProductModel.objects.create(name="BearModel")


    def test_user_age_and_validation(self):
        self.assertTrue(self.user.age >= 18)
        self.assertEqual(str(self.user), "testuser")
        

        young_user = CustomUser(username="kid", birth_date=date.today())
        with self.assertRaises(ValidationError):
            young_user.save()


    def test_product_logic(self):
        product = Product.objects.create(
            name="Teddy", 
            price=Decimal("15.50"), 
            product_model=self.p_model
        )
        product.product_type.add(self.p_type)
        
        self.assertEqual(product.display_product_type(), "Toy")
        self.assertIn("BearModel", str(product))
        self.assertEqual(product.get_absolute_url(), f"/api/product/{product.id}")

    def test_product_invalid_price(self):
        with self.assertRaises(ValidationError):
            Product.objects.create(name="Free", price=0, product_model=self.p_model)


    def test_employee_logic(self):
        emp = Employee.objects.create(
            user=self.user,
            phone=self.phone,
            info="Manager"
        )
        self.assertEqual(emp.display_username(), "testuser")
        self.assertEqual(emp.display_email(), "test@test.com")
        self.assertIn("https://randomfox.ca/images/", emp.get_avatar_url)
        self.assertIn("Employee: testuser", str(emp))


    def test_client_logic(self):
        client = Client.objects.create(
            user=self.user,
            company_name="ToyCorp",
            phone=self.phone,
            address="Main St 1",
            city=self.city
        )
        self.assertEqual(client.display_username(), "testuser")
        self.assertIn("ToyCorp", str(client))

    def test_client_invalid_role(self):

        self.user.is_superuser = True
        self.user.save()
        client = Client(user=self.user, company_name="Error", phone=self.phone, address="A", city=self.city)
        with self.assertRaises(ValidationError):
            client.clean()


    def test_order_total_and_promo(self):
        product = Product.objects.create(name="Car", price=Decimal("100.00"), product_model=self.p_model)
        client = Client.objects.create(user=self.user, company_name="C", phone=self.phone, address="A", city=self.city)
        point = PickUpPoint.objects.create(city=self.city, address="Point A")
        
        order = Order.objects.create(
            product=product, product_amount=2, client=client, 
            pick_up_point=point, date_order_create=timezone.now()
        )
        self.assertEqual(order.get_total, 200.00)

        promo = Promo.objects.create(info="Sale", sale=Decimal("0.10"), product=product)
        order.promo = promo
        order.save()
        self.assertEqual(order.get_total, 180.00)

    def test_phone_regex(self):
        with self.assertRaises(ValidationError):
            Phone.objects.create(phone="invalid")
        
        valid_phone = Phone.objects.create(phone="+375 (29) 123-45-67")
        self.assertEqual(str(valid_phone), "+375 (29) 123-45-67")

    def test_promo_active(self):
        product = Product.objects.create(name="P", price=10, product_model=self.p_model)
        promo = Promo.objects.create(sale=Decimal("0.5"), product=product)
        self.assertTrue(promo.is_active())
        self.assertEqual(promo.promo_sale_percentage(), "50.0%")

    def test_simple_models_str(self):
        faq = FAQ.objects.create(question="Q?", answer="A!")
        self.assertEqual(str(faq), "Q?")
        
        news = News.objects.create(header="News!", info="Info")
        self.assertEqual(str(news), "News!")
        
        about = AboutInfo.objects.create(header="About", info="Text")
        self.assertEqual(str(about), "About")
        
        vac = Vacancy.objects.create(title="Dev", info="I", requirements="R", salary=1000)
        self.assertEqual(str(vac), "Dev")

    def test_vacancy_negative_salary(self):
        vac = Vacancy(title="V", info="I", requirements="R", salary=-100)
        with self.assertRaises(ValidationError):
            vac.save()

    def test_review_grade_range(self):
        rev = Review(user=self.user, review="Good", grade=10)
        with self.assertRaises(ValidationError):
            rev.save()
        
        rev_ok = Review.objects.create(user=self.user, review="Nice", grade=5)
        self.assertIn("testuser", str(rev_ok))

    def test_city_unique_constraint(self):
        City.objects.create(name="Gomel")
        with self.assertRaises(Exception): 
            City.objects.create(name="gomel")