from django.urls import path, include
from main.views import show_main

app_name = 'main'

urlpatterns = [
    path('', include('reksa.urls', namespace='reksa')),
]

