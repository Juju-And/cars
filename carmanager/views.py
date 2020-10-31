import json
from typing import Dict, Any

from django.db.models import Avg
from django.forms import model_to_dict
from django.http import Http404, JsonResponse
from django.views import View
from pip._vendor import requests
from rest_framework.exceptions import ValidationError

from carmanager.models import Car, Rate


class CarsView(View):
    def get(self, request):
        cars = Car.objects.all()
        cars_list = []
        for car in cars:
            single_car_rates = (
                Rate.objects.filter(car=car).all().aggregate(Avg("rate_point"))
            )
            car_record = model_to_dict(car)
            car_record.update(single_car_rates)
            cars_list.append(car_record)

        return JsonResponse(cars_list, safe=False)

    def post(self, request):
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        car_make = body["car_make"]
        model_name = body["model_name"]

        car_make_url = f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{car_make}?format=json"
        car_make_json = requests.get(car_make_url).json()

        self.__validate_car_make_and_model(
            car_make_json=car_make_json, model_name=model_name
        )
        # TO DO - fix brand verification
        Car.objects.create(
            car_make=car_make_json["Results"][0]["Make_Name"], model_name=model_name
        )

        return JsonResponse({"Message": "Car successfully added!"})

    @staticmethod
    def __validate_car_make_and_model(car_make_json: Dict[str, Any], model_name: str):

        if len(car_make_json["Results"]) == 0:
            raise Http404("Make car not found.")

        car_models = []
        for result in car_make_json["Results"]:
            car_models.append(result["Model_Name"])
        try:
            car_models.index(model_name)
        except:
            raise Http404("Model name not found.")

        return car_make_json


class CarsRatingView(View):
    def post(self, request):
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)

        rate_point = body["rate_point"]
        car_id = body["car_id"]
        self.__validate_rating(rate_point)

        car = Car.objects.filter(id=car_id).first()
        Rate.objects.create(car=car, rate_point=rate_point)

        return JsonResponse(
            {
                "Message": f"Car {car.car_make} {car.model_name} successfully rate to {rate_point}!"
            }
        )

    @staticmethod
    def __validate_rating(rate_point):
        if 0 > rate_point or rate_point > 5:
            raise ValidationError("Invalid rate value.")
