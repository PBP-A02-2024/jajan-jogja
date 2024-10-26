from django.urls import path
from reviews.views import create_review


app_name = 'reviews'

urlpatterns = [
    path('<str:id>/create', create_review, name='create_review'),

    ]