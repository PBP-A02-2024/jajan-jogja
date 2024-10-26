from django.urls import path
from reviews.views import create_review, get_reviews


app_name = 'reviews'

urlpatterns = [
    path('<str:id>/create', create_review, name='create_review'),
    path('get-reviews/<str:id>/', get_reviews, name='get_reviews'),
    ]