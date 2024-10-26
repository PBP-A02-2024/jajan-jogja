from django.urls import path
from marco.views import get_restaurant, get_makanan_json, get_food_plans_json

app_name = 'marco'

urlpatterns = [
    path('<uuid:tempatKulinerId>', get_restaurant, name='get_restaurant'),
    path('get_makanan_json/<uuid:tempatKulinerId>/', get_makanan_json, name='get_makanan_json'),
    path('get_food_plans_json', get_food_plans_json, name='get_food_plans_json')
]
