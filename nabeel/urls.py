from django.urls import path
from nabeel.views import search_page

app_name = 'nabeel'

urlpatterns = [
    path('', search_page, name='search_page'),
]