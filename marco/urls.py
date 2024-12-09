from django.urls import path
from marco.views import get_restaurant, get_makanan_json, get_food_plans_json, save_food_plan, get_restoran_json

app_name = 'marco'

urlpatterns = [
    path('<uuid:tempatKulinerId>/', get_restaurant, name='get_restaurant'),
    path('get_makanan_json/<uuid:tempatKulinerId>/', get_makanan_json, name='get_makanan_json'),
    path('get_restoran_json/<uuid:tempatKulinerId>/', get_restoran_json, name='get_makanan_json'),
    path('get_food_plans_json', get_food_plans_json, name='get_food_plans_json'),
    path('save_food_plan', save_food_plan, name='save_food_plan')
]
