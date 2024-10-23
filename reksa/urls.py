from django.urls import path
from reksa.views import food_plans_list, food_plan

app_name = 'reksa'

urlpatterns = [
    path('food_plans/', food_plans_list, name='food_plans'),
    path('food_plan/', food_plan, name='food_plan'),
]