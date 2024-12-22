from django.shortcuts import get_object_or_404, render

from restaurant.models import Restaurant


def home(request):
    return render(request, "front/home.html")


def list_restaurant(request):
    restaurants = Restaurant.objects.all()
    return render(request, "front/list_restaurant.html", {"restaurants": restaurants})


def detail_restaurant(request, restaurant_pk):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_pk)
    return render(request, "front/detail_restaurant.html", {"restaurant": restaurant})
