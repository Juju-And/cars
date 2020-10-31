import json

from django.test import TestCase
from rest_framework.test import APIClient

from carmanager.models import Car, Rate
from carmanager.views import generate_all_cars_list


class CheckNumberTest(TestCase):
    def setUp(self):
        Car.objects.create(id=101, car_make="MERCEDES-BENZ", model_name="Milan")
        Car.objects.create(id=102, car_make="MERCEDES-BENZ", model_name="Sprinter")
        Car.objects.create(id=103, car_make="Audi", model_name="TT")

        Rate.objects.create(car_id=101, rate_point=1)
        Rate.objects.create(car_id=101, rate_point=2)
        Rate.objects.create(car_id=101, rate_point=3)
        Rate.objects.create(car_id=102, rate_point=5)
        Rate.objects.create(car_id=102, rate_point=2)
        Rate.objects.create(car_id=103, rate_point=4)

    def test_generate_all_cars_list(self):
        # given
        cars = Car.objects.all()

        # when
        cars_list = generate_all_cars_list(cars=cars)

        # then
        self.assertEqual(3, len(cars_list))

    def test_post_new_car(self):
        # given
        client = APIClient()

        # when
        response = client.post(
            "/cars", {"car_make": "honda", "model_name": "civic"}, format="json"
        )

        # then
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {"Message": "Car successfully added!"}, json.loads(response.content)
        )
        self.assertEqual(4, len(Car.objects.all()))

    def test_post_new_car__when_invalid_car_mark_model_name(self):
        # given
        client = APIClient()

        # when - then
        with self.assertRaises(ValueError):
            client.post(
                "/cars", {"car_make": "aaaaaa", "model_name": "civic"}, format="json"
            )
            client.post(
                "/cars", {"car_make": "honda", "model_name": "cevic"}, format="json"
            )
