import requests
import json
import os
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Make HTTP GET requests
def get_request(url, **kwargs):
   print(kwargs)
   print("GET from {} ".format(url))
   api_key = kwargs.get("api_key")
   try:
      # Call get method of requests library with URL and parameters
      if api_key:
         params = dict()
         params["text"] = kwargs["text"]
         params["version"] = kwargs["version"]
         params["features"] = kwargs["features"]
         params["return_analyzed_text"] = kwargs["return_analyzed_text"]
         response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
      else:
         response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
   except:
      # If any error occurs
      print("Network exception occurred")
   status_code = response.status_code
   print("With status {} ".format(status_code))
   json_data = json.loads(response.text)
   return json_data


# Make HTTP POST requests
def post_request(url, json_payload, **kwargs):
   try:
      requests.post(url, params=kwargs, json=json_payload)
   except:
      # If any error occurs
      print("Network exception occurred")

# Get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
   results = []
   # Call get_request with a URL parameter
   json_result = get_request(url)
   if json_result:
      # Get the row list in JSON as dealers
      dealers = json_result
      # For each dealer object
      for dealer in dealers:
         # Create a CarDealer object with values in `doc` object
         dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                 id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                 short_name=dealer["short_name"],
                                 st=dealer["st"], state=dealer["state"], zip=dealer["zip"])
         results.append(dealer_obj)

   return results

def get_dealer_by_id(url, dealerId):
   # Call get_request with a URL and ID parameter
   json_result = get_request(url, id=dealerId)
   if json_result:
      dealers = json_result
      # For each dealer object
      for dealer in dealers:
         # Create a CarDealer object with values in `doc` object
         dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                 id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                 short_name=dealer["short_name"],
                                 st=dealer["st"], state=dealer["state"], zip=dealer["zip"])

   return dealer_obj

def get_dealer_by_state(url, state):
   # Call get_request with a URL and ID parameter
   results = []
   json_result = get_request(url, state=state)
   if json_result:
      dealers = json_result
      # For each dealer object
      for dealer in dealers:
         # Create a CarDealer object with values in `doc` object
         dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                 id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                 short_name=dealer["short_name"],
                                 st=dealer["st"], state=dealer["state"], zip=dealer["zip"])
         results.append(dealer_obj)

   return results


# Get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
   results = []
   json_result = get_request(url, id=dealerId)

   if json_result:
      reviews = json_result
      
      for review in reviews:
         review_obj = DealerReview(name=review["name"], purchase=review["purchase"], review=review["review"],
                                    purchase_date=review["purchase_date"], car_make=review["car_make"], car_model=review["car_model"],
                                    car_year=review["car_year"], dealership=review["dealership"], sentiment="", id=review["id"])
         review_obj.sentiment = analyze_review_sentiments(review["review"])
         results.append(review_obj)
   
   return results

# Call Watson NLU and analyze text
def analyze_review_sentiments(text):
   url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/934b17b7-28ca-4355-8621-0a00f87bb4be"
   api_key = os.environ.get("NLU_API_KEY")
   authenticator = IAMAuthenticator(api_key)
   natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-08-10',authenticator=authenticator)
   natural_language_understanding.set_service_url(url)
   response = natural_language_understanding.analyze(
      text=text,
      features=Features(sentiment=SentimentOptions(targets=[text]))).get_result()
   label=json.dumps(response, indent=2)
   label = response['sentiment']['document']['label']
   
   
   return(label)
   

