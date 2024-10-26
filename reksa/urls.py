from django.urls import path
from reksa.views import food_plans_list, food_plan_detail_view, food_plan_create

app_name = 'reksa'

urlpatterns = [
    path('', food_plans_list, name='food_plans_list'),
    path('food_plan/<uuid:food_plan_id>/', food_plan_detail_view, name='food_plan_detail_view'),
    path('create/', food_plan_create, name='food_plan_create'),
]