import json

from django.test import TestCase
from django_http_exceptions import HTTPExceptions
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from carmanager.models import Car, Rate


class CheckNumberTest(TestCase):
    def setUp(self):
        Car.objects.create(id=101, car_make="Fiat", model_name="Ducato")
        Car.objects.create(id=102, car_make="MERCEDES-BENZ", model_name="Sprinter")
        Car.objects.create(id=103, car_make="Audi", model_name="TT")

        Rate.objects.create(car_id=101, rate_point=1)
        Rate.objects.create(car_id=101, rate_point=2)

        Rate.objects.create(car_id=102, rate_point=3)
        Rate.objects.create(car_id=102, rate_point=5)
        Rate.objects.create(car_id=102, rate_point=2)

        Rate.objects.create(car_id=103, rate_point=1)

    def test_get_all_cars(self):
        # given
        client = APIClient()

        # when
        response = client.get("/cars")
        # then
        self.assertEqual(3, len(json.loads(response.content)))

    def test_get_most_popular(self):
        # given
        client = APIClient()

        # when
        response = client.get("/popular")

        # then
        self.assertEqual("MERCEDES-BENZ", json.loads(response.content)[0]["car_make"])

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

    def test_post_car_rate(self):
        # given
        client = APIClient()
        car_id = 101

        # when
        response = client.post(
            "/rate", {"car_id": car_id, "rate_point": 4}, format="json"
        )

        # then
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(Car.objects.filter(id=car_id).first().rates.all()))
        self.assertEqual(
            4, Car.objects.filter(id=car_id).first().rates.last().rate_point
        )

    def test_post_car_rate__when_invalid_value_less_1(self):
        # given
        client = APIClient()
        car_id = 101

        # when - then
        with self.assertRaises(ValidationError):
            client.post("/rate", {"car_id": car_id, "rate_point": 0}, format="json")

    def test_post_car_rate__when_invalid_value_more_5(self):
        # given
        client = APIClient()
        car_id = 101

        # when - then
        with self.assertRaises(ValidationError):
            client.post("/rate", {"car_id": car_id, "rate_point": 6}, format="json")

    def test_post_new_car__when_invalid_car_make(self):
        # given
        client = APIClient()

        # when - then
        response = client.post(
            "/cars", {"car_make": "aaaaaa", "model_name": "civic"}, format="json"
        )
        # then
        self.assertEqual(422, response.status_code)
        self.assertEqual("Invalid car make.", response.content.decode("utf-8"))

    def test_post_new_car__when_invalid_model_name(self):
        # given
        client = APIClient()

        # when
        response = client.post(
            "/cars", {"car_make": "honda", "model_name": "cevic"}, format="json"
        )
        self.assertEqual(422, response.status_code)
        self.assertEqual("Invalid model name.", response.content.decode("utf-8"))
