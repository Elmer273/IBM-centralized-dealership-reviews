from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_dealer_by_id
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)



# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)
        
# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['psw']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)
        
    elif request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://elmermartine-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # url = "http://localhost:3000/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        review_url = "https://elmermartine-5000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        # review_url = "http://127.0.0.1:5000/api/get_reviews"
        reviews = get_dealer_reviews_from_cf(review_url, dealerId=dealer_id)

        dealer_url = "https://elmermartine-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # dealer_url = "http://localhost:3000/dealerships/get"
        dealer = get_dealer_by_id(dealer_url, dealer_id)  

        context["dealer"] = dealer
        context["dealer_id"] = dealer_id
        context["reviews"] = reviews

        return render(request, 'djangoapp/dealer_details.html', context)
    
# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            url = "https://elmermartine-5000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
            # url = "http://127.0.0.1:5000/api/post_review"

            purchase_check = False
            if request.POST['purchasecheck'] == 'on':
                purchase_check = True

            car_model, car_make, car_year = request.POST['car_details'].split('-')
            json_payload = {
                "id": 51,
                "name": f"{request.user.first_name} {request.user.last_name}",
                "dealership": dealer_id,
                "review": request.POST['review'],
                "purchase": purchase_check,
                "purchase_date": datetime.utcnow().isoformat(),
                "car_make": car_make,
                "car_model": car_model,
                "car_year": car_year,
            }

            post_request(url, json_payload)

            return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
        
        elif request.method == "GET":
            context = {}
            dealer_url = "https://elmermartine-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
            # dealer_url = "http://localhost:3000/dealerships/get"

            cars = list(CarModel.objects.filter(dealer_id=dealer_id))
            dealer = get_dealer_by_id(dealer_url, dealer_id)  

            context["dealer"] = dealer
            context["dealer_id"] = dealer_id
            context["cars"] = cars

            return render(request, 'djangoapp/add_review.html', context)

    else: 
        print("User is not authenticated")
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)