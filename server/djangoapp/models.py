from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
   name = models.CharField(null=False, max_length=30, default='BMW')
   description = models.CharField(max_length=1000)
   country = models.CharField(max_length=56)

   def __str__(self):
      return "Name: " + self.name + "," + \
             "Description: " + self.description + \
             "Country " + self.country

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

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

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
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

# <HINT> Create a plain Python class `DealerReview` to hold review data
