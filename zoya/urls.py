from django.urls import path
from zoya.views import show_main, show_json_tempat

app_name = 'zoya'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('json-tempat/', show_json_tempat, name='show_json_tempat'),
]