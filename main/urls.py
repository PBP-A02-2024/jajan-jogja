from django.urls import path, include
from main.views import show_main
from django.urls import path
from main.views import login_user, logout_user, show_main, register, profile, edit_profile_flutter

app_name = 'main'

urlpatterns = [
    path('login/', login_user, name='login_user'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile-flutter/', edit_profile_flutter, name='profile'),
]

