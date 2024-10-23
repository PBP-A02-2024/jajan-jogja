from django.urls import path
from reksa.views import food_plans

app_name = 'reksa'

urlpatterns = [
    path('food_plans/', food_plans, name='food_plans'),
]