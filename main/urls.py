from django.urls import path
from main.views import login_user, logout_user, show_main, register

app_name = 'main'

urlpatterns = [
    path('login/', login_user, name='login_user'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
]

