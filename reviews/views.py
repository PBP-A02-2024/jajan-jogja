from django.shortcuts import render, get_object_or_404, redirect
from zoya.models import TempatKuliner
from reviews.models import Review
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
@csrf_protect
def create_review(request, id):
    tempat_kuliner = get_object_or_404(TempatKuliner, pk=id)

    # Check if the user has already submitted a review for this TempatKuliner
    existing_review = Review.objects.filter(user=request.user, tempat_kuliner=tempat_kuliner).first()
    if existing_review:
        messages.error(request, "You have already reviewed this place.")
        return redirect("marco:get_restaurant", id=tempat_kuliner.id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        # Validate rating
        if rating and int(rating) not in [choice[0] for choice in Review.RATING_CHOICES]:
            messages.error(request, "Rating is not valid")
            return render(request, "review-page.html", {"tempat_kuliner": tempat_kuliner})

        # Validate and save the review
        if rating:
            if comment is None:
                comment=""
            review = Review(
                user=request.user,
                tempat_kuliner=tempat_kuliner,
                rating=int(rating),
                comment=comment,
            )
            try:
                review.full_clean()  # Validate model fields
                review.save()
                tempat_kuliner.update_rating()  # Assuming a method to update the overall rating
                messages.success(request, "Your review has been submitted successfully.")
                return redirect("marco:get_restaurant", id=tempat_kuliner.id)
            except ValidationError as e:
                messages.error(request, "Error saving review: " + ", ".join(e.messages))
        else:
            if not rating:
                messages.error(request, "Rating is required.")
            if not comment:
                messages.error(request, "Comment cannot be empty.")

    return render(request, "review-page.html", {"tempat_kuliner": tempat_kuliner})


def get_reviews(request, id):
    tempat_kuliner = get_object_or_404(TempatKuliner, pk=id)
    reviews = Review.objects.filter(tempat_kuliner=tempat_kuliner).order_by('-created_at')

    # Manually build the review data with the username
    review_data = [
        {
            "user": review.user.username,  # Retrieve the username
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at.isoformat()  # Serialize date to ISO format
        }
        for review in reviews
    ]

    return JsonResponse(review_data, safe=False)