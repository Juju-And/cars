import json
from typing import Dict, Any, List

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
        return JsonResponse(generate_all_cars_list(cars), safe=False)

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
            car_make=car_make_json["Results"][0]["Make_Name"].upper(),
            model_name=model_name.upper(),
        )

        return JsonResponse({"Message": "Car successfully added!"})

    @staticmethod
    def __validate_car_make_and_model(car_make_json: Dict[str, Any], model_name: str):
        car_makes = []
        for result in car_make_json["Results"]:
            car_makes.append(result["Model_Name"].lower())
        try:
            car_makes.index(model_name.lower())
        except ValueError:
            raise ValueError("Invalid make car.")

        car_models = []
        for result in car_make_json["Results"]:
            car_models.append(result["Model_Name"].lower())
        try:
            car_models.index(model_name.lower())
        except ValueError:
            raise ValueError("Invalid model name.")

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


class CarsPopularityView(View):
    def get(self, request):
        cars = Car.objects.all()
        cars_list = []
        for car in cars:
            total_rate_entries = Rate.objects.filter(car=car).count()
            car_record = model_to_dict(car)
            car_record["total_rate_entries"] = total_rate_entries
            cars_list.append(car_record)
        cars_sorted_list = sorted(
            cars_list, key=lambda k: k["total_rate_entries"], reverse=True
        )
        return JsonResponse(cars_sorted_list, safe=False)


def generate_all_cars_list(cars) -> List:
    cars_list = []
    for car in cars:
        car_avg_rates = Rate.objects.filter(car=car).all().aggregate(Avg("rate_point"))
        car_record = model_to_dict(car)
        car_record.update(car_avg_rates)
        cars_list.append(car_record)
    return cars_list
