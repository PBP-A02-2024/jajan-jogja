from django.urls import path
from zoya.views import show_main

app_name = 'zoya'

urlpatterns = [
    path('', show_main, name='show_main'),
]