from django.urls import path
from reviews.views import (
    create_review,
    get_reviews,
    delete_review,
    get_review_by_id,
    edit_review,
    user_owned_reviews,
    get_reviews_flutter,
    get_reviews_by_current_user_flutter,
    create_review_flutter,
    update_review_flutter,
    delete_review_flutter,
)

app_name = 'reviews'

urlpatterns = [
    path('<uuid:id>/create', create_review, name='create_review'),
    path('get-reviews/<str:id>/', get_reviews, name='get_reviews'),
    path('create-review-flutter/', create_review_flutter, name='create_review_flutter'),
    path('update-review-flutter/<int:id>/', update_review_flutter, name='update_review_flutter'),
    path('delete-review-flutter/<int:id>/', delete_review_flutter, name='delete_review_flutter'),
    path('get-reviews-flutter/<str:id>/', get_reviews_flutter, name='get_reviews_flutter'),
    path('get-reviews-by-current-user-flutter/', get_reviews_by_current_user_flutter, name='get_reviews_by_current_user_flutter'),
    path('delete/<int:id>/', delete_review, name='delete_review'),
    path('get-review-by-id/<int:id>/', get_review_by_id, name='get_review_by_id'),
    path('edit/<int:id>/', edit_review, name='edit_review'),
    path('', user_owned_reviews, name="my_reviews"),
    ]