from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_reviews_by_id_from_cf, post_request
from datetime import datetime
import logging
import json
from .models import CarDealer, DealerReview, CarModel, CarMake

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...


# Create a `contact` view to return a static contact page
#def contact(request):

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successfully!")
            return redirect('djangoapp:index')
        else:
            messages.warning(request, "Invalid username or password.")
            return redirect("djangoapp:index")



# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    print("Log out the user '{}'".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')
    
# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['lastname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{}is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(
                username == username, first_name=first_name, last_name=last_name, password=password,)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/c47d8d02-01c2-43d0-9638-9b6127312e31/dealership-package/get-dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)

def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = 'https://us-south.functions.appdomain.cloud/api/v1/web/c47d8d02-01c2-43d0-9638-9b6127312e31/dealership-package/get-dealership'
        context = {"reviews":  get_dealer_reviews_from_cf(url, dealer_id)}
        
        return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, dealer_id):
    context = {}
    # If it is a GET request, just render the add_review page
    if request.method == 'GET':
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/05174de9-c4f2-4d8f-a22f-b17713e83492/dealership-package/get-dealership"
        # Get dealers from the URL
        context = {
            "dealer_id": dealer_id,
            "dealer_name": get_dealers_from_cf(url)[dealer_id-1].full_name,
            "cars": CarModel.objects.all()
        }
        #print(context)
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if (request.user.is_authenticated):
            review = dict()
            review["id"]=0#placeholder
            review["name"]=request.POST["name"]
            review["dealership"]=dealer_id
            review["review"]=request.POST["content"]
            if ("purchasecheck" in request.POST):
                review["purchase"]=True
            else:
                review["purchase"]=False
            print(request.POST["car"])
            if review["purchase"] == True:
                car_parts=request.POST["car"].split("|")
                review["purchase_date"]=request.POST["purchase_date"] 
                review["car_make"]=car_parts[0]
                review["car_model"]=car_parts[1]
                review["car_year"]=car_parts[2]

            else:
                review["purchase_date"]=None
                review["car_make"]=None
                review["car_model"]=None
                review["car_year"]=None
            json_result = post_request("https://eu-gb.functions.appdomain.cloud/api/v1/web/05174de9-c4f2-4d8f-a22f-b17713e83492/dealership-package/post-review", review, dealerId=dealer_id)
            print(json_result)
            if "error" in json_result:
                context["message"] = "ERROR: Review was not submitted."
            else:
                context["message"] = "Review was submited"
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)


