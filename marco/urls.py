from django.urls import path
from marco.views import get_restaurant, get_makanan_json

app_name = 'marco'

urlpatterns = [
    path('<str:id>', get_restaurant, name='get_restaurant'),
    path('get_makanan_json/<str:tempatKulinerId>/', get_makanan_json, name='get_makanan_json')
]
