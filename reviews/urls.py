from django.urls import path
from reviews.views import create_review, get_reviews, delete_review,get_review_by_id, edit_review, user_owned_reviews


app_name = 'reviews'

urlpatterns = [
    path('<uuid:id>/create', create_review, name='create_review'),
    path('get-reviews/<str:id>/', get_reviews, name='get_reviews'),
    path('delete/<int:id>/', delete_review, name='delete_review'),
    path('get-review-by-id/<int:id>/', get_review_by_id, name='get_review_by_id'),
    path('edit/<int:id>/', edit_review, name='edit_review'),
    path('', user_owned_reviews, name="my_reviews"),
    ]