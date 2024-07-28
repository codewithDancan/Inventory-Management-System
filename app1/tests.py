from django.test import TestCase, SimpleTestCase, RequestFactory, Client
from djmoney.money import Money
from app.models import (
    Engine, 
    Seller,
    Vehicle,
    VehicleModel
)
from django.contrib.auth.models import AnonymousUser
from .views import (
    practice_year_view,
    VehicleListView,
)
from rest_framework.test import APITestCase, APIClient
# Create your tests here.

class TestingCalibrator(SimpleTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_pass(self):
        """checks if True == True, Value set to True"""
        self.assertTrue(True)

    def test_fail(self):
        """checks if False == False, Value set to False"""
        self.assertFalse(False)


"""testing Django models """
class ModelUnitTestCase(TestCase):
    def setUp(self):
        model = VehicleModel.objects.create(name="Grand Laredo")
        engine = Engine.objects.create(name="3.6L DO", vehicle_model=model)
        vehicle = Vehicle.objects.create(
            vin="aa8923",
            sold=False,
            price=Money(1500000, "Ksh"),
            make=4,
            vehicle_model = model,
            engine = engine,
        )
        seller = Seller.objects.create_user(
            "test", "testing@gmail.com", "password",
            is_staff=True,
            is_superuser=True,
            is_active = True,
            name = " Seller 1"
        )
        seller.vehicle.set([vehicle])

    def test_full_vehicle_name(self):
        vehicle_1 = Vehicle.objects.get(vin="aa8923")
        self.assertEqual(vehicle_1.full_vehicle_name(), "Jeep Grand Laredo - 3.6L DO")

""" testing HTTP View Request
    testing method based views 
"""
class YearRequestTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_methodbased(self):
        request = self.factory.get("my_year_path_3/2024/")
        request.user = AnonymousUser()
        response = practice_year_view(request, 2024)
        self.assertEqual(response.status_code, 200)

"""testing class-based views """

class VehicleListViewRequestTestCase(TestCase):
    # fixtures = ['app1']

    def setUp(self):
        self.factory = RequestFactory()

    def test_classbased(self):
        request = self.factory.get("vehicle/")
        request.user = AnonymousUser()
        response = VehicleListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

""" Testing authenticated view requests """
"""class SellerClientTestCase(TestCase):

    def setUp(self):
        self.user = Seller.objects.get(id=1)
        self.client = Client()
        self.client.login(
            username=self.user.username,
            password="mynewpassword"
        )
    def test_get(self):
        response = self.client.get("api/sellers/1")
        self.assertEqual(response.status_code, 200)
        seller = response.context["seller"]
        self.assertEqual(seller.name, "Dancan")"""

class EngineAPITestCase(APITestCase):

    def setUp(self):
        self.user  = Seller.objects.get(id=1)
        self.client = APIClient()
        self.client.login(
            username=self.user.username,
            password = "mynewpassword"
        )

    def test_post(self):
        response = self.client.post("engines/",
                                        {"name": "New Engine"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name', "New Engine"])


