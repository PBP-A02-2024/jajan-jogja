from django.urls import path
from restaurant_and_food.views import show_restaurant

app_name = 'restaurant_and_food'

urlpatterns = [
    path('', show_restaurant, name='show_restaurant'),
]
