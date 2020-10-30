import json
from typing import Dict, Any

from django.http import Http404, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from pip._vendor import requests

from carmanager.models import Car


class CarsView(View):
    def get(self, request):
        cars = list(Car.objects.all().values())
        return JsonResponse(cars, safe=False)

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
