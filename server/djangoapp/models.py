from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
   name = models.CharField(null=False, max_length=30, default='BMW')
   description = models.CharField(max_length=1000)
   country = models.CharField(max_length=56)

   def __str__(self):
      return "Name: " + self.name + "," + \
             "Description: " + self.description + \
             "Country " + self.country

class CarModel(models.Model):
   SEDAN = 'sedan'
   SUV = 'SUV'
   WAGON = 'wagon'
   HATCHBACK = 'hatchback'
   COUPE = 'coupe'
   PICKUP = "pickup"
   VAN = 'van'

   TYPE_CHOICES = [
      (SEDAN, 'Sedan'),
      (SUV, 'Sports Utility Vehicle'),
      (WAGON, 'Wagon'),
      (HATCHBACK, 'Hatchback'),
      (COUPE, 'Coupe'),
      (PICKUP, 'Pickup Truck'),
      (VAN, 'Van'),
   ]
   car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
   name = models.CharField(null=False, max_length=30, default='X5')
   dealer_id = models.IntegerField()
   type = models.CharField(max_length=9, choices=TYPE_CHOICES, default=SEDAN)
   year = models.CharField(max_length=4, default=now().year)

   def __str__(self):
      return "Car Make: " + self.car_make.name + "," + \
             "Name: " + self.name + "," + \
             "Dealer ID: " + str(self.dealer_id) + "," + \
             "Type: " + self.type + "," + \
             "Year: " + self.year

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, state, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer State
        self.state = state
        # State Abbreviation
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:
   
   def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
      self.dealership = dealership
      self.name = name
      self.purchase = purchase
      self.review = review
      self.purchase_date = purchase_date
      self.car_make = car_make
      self.car_model = car_model
      self.car_year = car_year
      self.sentiment = sentiment
      self.id = id