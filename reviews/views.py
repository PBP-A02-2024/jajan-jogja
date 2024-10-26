from django.shortcuts import render, get_object_or_404, redirect
from zoya.models import TempatKuliner
from reviews.models import Review
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers

@login_required
def user_owned_reviews(request):
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "user_owned_reviews.html", {"reviews": reviews})

@csrf_protect
@login_required
def create_review(request, id):
    tempat_kuliner = get_object_or_404(TempatKuliner, pk=id)
    print(tempat_kuliner.id)

    # Check if the user has already submitted a review for this TempatKuliner
    existing_review = Review.objects.filter(user=request.user, tempat_kuliner=tempat_kuliner).first()
    if existing_review:
        messages.error(request, "You have already reviewed this place.")
        return redirect("marco:get_restaurant", tempatKulinerId=tempat_kuliner.id)

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
                return redirect("marco:get_restaurant",  tempatKulinerId=tempat_kuliner.id)
            except ValidationError as e:
                messages.error(request, "Error saving review: " + ", ".join(e.messages))
        else:
            if not rating:
                messages.error(request, "Rating is required.")
            if not comment:
                messages.error(request, "Comment cannot be empty.")

    return render(request, "review-page.html", {"tempat_kuliner": tempat_kuliner})

@csrf_protect
@login_required
def get_reviews(request, id):
    tempat_kuliner = get_object_or_404(TempatKuliner, pk=id)
    reviews = Review.objects.filter(tempat_kuliner=tempat_kuliner).order_by('-created_at')

    # Manually build the review data with the username
    review_data = [
        {
            "user": review.user.username,  # Retrieve the username
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at,
            "id": review.id,
            "pk" : review.pk
        }
        for review in reviews
    ]

    return JsonResponse(review_data, safe=False)

def get_review_by_id(request, id):
    review = get_object_or_404(Review, pk=id)
    review_data = [
        {
            "user": review.user.username,  # Retrieve the username
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at,
            "id": review.id,
            "pk" : review.pk
        }
        for review in reviews
    ]

    return JsonResponse(review_data, safe=False)

@csrf_protect
@login_required
def delete_review(request, id):
    review = get_object_or_404(Review, pk=id, user=request.user)
    tempat_kuliner = review.tempat_kuliner

    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            review.delete()
            tempat_kuliner.update_rating()
            return JsonResponse({"success": True, "message": "Review deleted successfully."})
        else:
            review.delete()
            tempat_kuliner.update_rating()
            messages.success(request, "Your review has been deleted successfully.")
            return redirect("marco:get_restaurant", id=tempat_kuliner.id)

    # Handle any disallowed methods or get requests
    return HttpResponseForbidden("Invalid request method.")

@csrf_protect
@login_required
def edit_review(request, id):
    review = get_object_or_404(Review, pk=id, user=request.user)

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data."}, status=400)

        rating = data.get("rating")
        comment = data.get("comment", "")
        if rating and int(rating) not in [choice[0] for choice in Review.RATING_CHOICES]:
            return JsonResponse({"success": False, "message": "Invalid rating value."}, status=400)
        review.rating = int(rating) if rating else review.rating
        review.comment = comment
        try:
            review.full_clean()
            review.save()
            review.tempat_kuliner.update_rating()
            return JsonResponse({"success": True, "message": "Review updated successfully."})
        except ValidationError as e:
            return JsonResponse({"success": False, "message": "Error updating review: " + ", ".join(e.messages)}, status=400)
    else:
        return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)