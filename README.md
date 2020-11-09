# Cars

This is a web application using Django, and based on api data https://vpic.nhtsa.dot.gov/api/.
App allows user to check existence of provided car brand and model, and adding it to the database if exists. 
Another function is possibility to rate cars.

## Running the app in local development

The provided Docker Compose file allows you to run the app locally in development. To start the container, run:

```
$ docker-compose up
```

Once the stack has launched, you can test the application by executing GET/POST commands described below.

## Executing the Tests

```
$ python ./manage.py test
```

## REST API

The REST API to the example app is described below.

### Get list of Cars

### Request

```
/cars/
```
```
curl -i -H 'Accept: application/json' http://localhost:8000/cars/
```

> Example responses
```json
[
    {
        "id": 1,
        "car_make": "HONDA",
        "model_name": "CIVIC",
        "rate_point__avg": 3.6666666666666665
    },
    {
        "id": 2,
        "car_make": "AUDI",
        "model_name": "TT",
        "rate_point__avg": null
    },
    {
        "id": 3,
        "car_make": "FIAT",
        "model_name": "DUCATO",
        "rate_point__avg": 3.5
    }
]
```
### Responses

|Status|Meaning|Description|
|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of added cars


### Create a new Car

### Request

```
POST /cars/
```
```
curl -i -H 'Accept: application/json' -d 'car_make=sample-name&model_name=sample-model' http://localhost:8000/cars/
```
> Body parameter

```json
{
    "car_make": "Audi",
    "model_name": "TT"
}
```

> Example responses
```json
{
  "Message": "Car successfully added!"
}
```

### Responses

|Status|Meaning|Description|
|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Car added do the database
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc4918#section-11.2)|Wrong Payload Type

### Rate a Car

### Request

```
POST /rate/
```
```
curl -i -H 'Accept: application/json' -d 'car_make=sample-name&model_name=sample-model' http://localhost:8000/rate/
```
> Body parameter

```json
{
    "car_id": "101",
    "rate_point": "4"
}
```

> Example responses
```json
{
  "Message": "Car AUDI TT successfully rate to 4!"
}
```

### Responses

|Status|Meaning|Description|
|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Rate added
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Car not found

### Get list of rated cars

### Request

```
POST /popular/
```
```
curl -i -H 'Accept: application/json' http://localhost:8000/popular/
```

> Example responses
```json
[
  {
    "id": 1,
    "car_make": "HONDA",
    "model_name": "CIVIC",
    "total_rate_entries": 3
  },
  {
    "id": 3,
    "car_make": "FIAT",
    "model_name": "DUCATO",
    "total_rate_entries": 2
  },
  {
    "id": 2,
    "car_make": "HONDA",
    "model_name": "CIVIC",
    "total_rate_entries": 0
  },
  {
    "id": 4,
    "car_make": "AUDI",
    "model_name": "TT",
    "total_rate_entries": 0
  }
]
```

### Responses

|Status|Meaning|Description|
|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of cars sorted by popularity


## Demo version

http://cars-rate.herokuapp.com/