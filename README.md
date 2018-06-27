[![Build Status](https://travis-ci.org/micahoriaso/Ride-My-Way.svg?branch=ft-ride-offers-api-158459164)](https://travis-ci.org/micahoriaso/Ride-My-Way)
[![Coverage Status](https://coveralls.io/repos/github/micahoriaso/Ride-My-Way/badge.svg?branch=ft-ride-offers-api-158459164)](https://coveralls.io/github/micahoriaso/Ride-My-Way?branch=ft-ride-offers-api-158459164)

# Ride-My-Way
Ride-My-Way App is a carpooling application that provides drivers with the ability to create ride offers and passengers to join available ride offers.

# Screenshot
![fireshot capture 007 - ride detail - file____home_oriaso_desktop_python_ride-my-way_ui_profile html](https://user-images.githubusercontent.com/20840601/41377320-6472fa3e-6f64-11e8-9a09-fcbdfd4eb886.png)

# Installation
* Clone the repo from github
```
https://github.com/micahoriaso/Ride-My-Way.git
```
* Create a virtual environment and activate it
```
python3 -m venv venv
source venv/bin/activate
```
* Install all dependencies

```
pip install -r requirements.txt
```
* Run the Flask application
```
flask run
```
# Testing
To test run the command 
```
pytest
```
# Endpoints

Endpoint | Functionality 
------------ | -------------
POST   /api/v1/rides | Create a ride offer
GET   /api/v1/rides | Get all rides
GET   /api/v1/rides/<ride_id> | Get a single ride offer
PUT   /api/v1/rides/<ride_id> | Update a single ride offer
DELETE   /api/v1/rides/<ride_id> | Delete a ride offer
POST   /api/v1/rides/<ride_id>/requests | Create a request for a particular ride
GET   /api/v1/rides/<ride_id>/requests | Get all requests for a particular ride
GET   /api/v1/rides/<ride_id>/requests/<request_id> | Get a ride request
PUT  /api/v1/rides/<ride_id>/requests/<request_id> | Update a ride request
DELETE   /api/v1/rides/<ride_id>/requests/<request_id> | Delete a single request

### Create A ride

Below is an example of a request to create a ride. 
```
/api/v1/rides/
```
Payload
```
{
        "date": "12-06-2018",
        "time": "11:00",
        "pickup": "Nyayo Stadium",
        "dropoff": "Belle Vue",
        "price": "100",
        "capacity": "3",
        "available_seats": "1",
        "driver": "Farrell",
        "car": "Mazda MX5",
        "registration": "KAA 987I"
}
```

The following response will be returned
```
{
    "status": "success",
    "data": {
        "pickup": "Nyayo Stadium",
        "available_seats": 1,
        "id": 1,
        "date": "12-06-2018",
        "time": "11:00",
        "price": 100.0,
        "dropoff": "Belle Vue",
        "capacity": 3,
        "registration": "KAA 987I",
        "ride_status": "In Offer",
        "driver": "Farrell",
        "car": "Mazda MX5"
    }
}
```

### Get ride offers
Below is an example of a *get* request endpoint to get the all ride offers

```
/api/v1/rides/
```
### Get a ride offer by id
To get a ride offer its id by use, in doing so, make sure you have added atleast on ride offer
```
/api/v1/rides/<ride_id>
```
eg
```
/api/v1/rides/1
```
The following response will be returned.
```
{
    "ride": {
        "pickup": "Nyayo Stadium",
        "available_seats": 1,
        "id": 1,
        "date": "12-06-2018",
        "time": "11:00",
        "price": 100,
        "dropoff": "Belle Vue",
        "capacity": 3,
        "registration": "KAA 987I",
        "ride_status": "In Offer",
        "driver": "Farrell",
        "car": "Mazda MX5"
    }
}
```

### Edit a ride offer
Send a `PUT` request in this syntax, make sure to have added at least on ride offer
```
/api/v1/rides/<ride_id>
```
e.g.
```
/api/v1/rides/1
```
Payload
```
{
	"date": "14-06-2018",
}
```

### Delete a Ride Offer
Send a `Delete`request with the ride Id as shown below. Make sure to have added at least on ride offer
```
/api/v1/rides/<ride_id>
```
e.g.
```
/api/v1/rides/1
```

## Ride Requests
You can also add, edit, update and delete ride requests.

### Get requests from a ride
Get all the requests of a ride by
specifying the ride id.
```
/api/v1/rides/<ride_id>/requests
```
e.g.
```
/api/v1/rides/1/requests
```

### Get request for a ride
Use the endpoint below, make sure to have added atleast one ride request
```
/api/v1/rides/<ride_id>/requests/<request_id>
```
e.g.

### Add request to ride
Send a Json payload to the following endpoint
```
api/v1/rides/<ride_id>/requests
```
e.g.
```
api/v1/rides/1/requests
```
Example Json payload
```
{
	"requestor_id": 3,
}
```

### Editing a ride request
A ride request can be editied by sending a `PUT` request
with a Json payload  to the following endpoint. Make sure to have added at least one ride request
```
/api/v1/rides/<ride_id>/requests/<request_id>
```
e.g.
```
/api/v1/rides/2/requests/1
```
Json payload
```
{
	"request_status": "Accepted"
}
```
### Delete a ride request
To delete a request from a ride offer, send a `DELETE`
request to the following endpoint. Make sure to have added at least one ride request
```
/api/v1/rides/<ride_id>/requests/<request_id>
```
e.g.
```
/api/v1/rides/2/requests/1
```

# Author
* **Micah Oriaso** [micahoriaso](https://github.com/micahoriaso)

## Acknowledgments

* Derrick Kipkorir [@Derrickkip](https://github.com/Derrickkip)
* Wandesky Brian [@wandesky](https://github.com/wandesky)


