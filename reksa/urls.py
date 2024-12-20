from django.urls import path
from reksa.views import food_plans_list, food_plan_detail_view, food_plan_create, add_food_plan_item, remove_food_plan_item, update_food_plan_title, remove_food_plan_restaurant, remove_food_plan
from reksa.views import food_plan_json, food_plan_detail_json, food_plan_create_json
app_name = 'reksa'

urlpatterns = [
    path('', food_plans_list, name='food_plans_list'),
    path('food_plan/<uuid:food_plan_id>/', food_plan_detail_view, name='food_plan_detail_view'),
    path('create/', food_plan_create, name='food_plan_create'),
    path('add_item/<uuid:food_plan_id>/', add_food_plan_item, name='add_food_plan_item'),
    path('remove_item/<uuid:food_plan_id>/', remove_food_plan_item, name='remove_food_plan_item'),
    path('update_title/<uuid:food_plan_id>/', update_food_plan_title, name='update_food_plan_title'),
    path('remove_restaurant/<uuid:food_plan_id>/', remove_food_plan_restaurant, name='remove_food_plan_restaurant'),
    path('remove/<uuid:food_plan_id>/', remove_food_plan, name='remove_food_plan'),
    path('food_plan_json/', food_plan_json, name='food_plan_json'),
    path('food_plan_detail_json/<uuid:food_plan_id>/', food_plan_detail_json, name='food_plan_detail_json'),
    path('food_plan_create_json/', food_plan_create_json, name='food_plan_create_json'), 
]