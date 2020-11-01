from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Car(models.Model):
    car_make = models.TextField(max_length=64)
    model_name = models.TextField(max_length=64)
    date_added = models.DateTimeField(auto_now_add=True)


class Rate(models.Model):
    rate_point = models.IntegerField(
        default=1, validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    car = models.ForeignKey(Car, related_name="rates", on_delete=models.CASCADE)
