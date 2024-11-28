from django.urls import path
from authentication.views import login, register

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
]