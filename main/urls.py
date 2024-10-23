from django.urls import path, include
from main.views import show_main

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('', include('reksa.urls', namespace='reksa')),
]

