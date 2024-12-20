from django.shortcuts import render, get_object_or_404, redirect
from zoya.models import TempatKuliner
from reviews.models import Review
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.exceptions import ValidationError
import json
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User

@login_required(login_url='main:login_user')
def user_owned_reviews(request):
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "user_owned_reviews.html", {"reviews": reviews})

@csrf_protect
@login_required(login_url='main:login_user')
def create_review(request, id):
    tempat_kuliner = get_object_or_404(TempatKuliner, pk=id)
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
@login_required(login_url='main:login_user')
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

def get_reviews_flutter(request, id):
    tempat_kuliner = get_object_or_404(TempatKuliner, pk=id)
    reviews = Review.objects.filter(tempat_kuliner=tempat_kuliner).order_by('-created_at').values(
        'id','user__id', 'user__username', 'tempat_kuliner','tempat_kuliner__nama','rating','comment','created_at','pk'
    )
    return JsonResponse(list(reviews), safe=False)

def get_reviews_by_current_user_flutter(request):
    reviews = Review.objects.filter(user=request.user).order_by('-created_at').values(
        'id','user__username','tempat_kuliner','tempat_kuliner__nama','rating','comment','created_at','id','pk'
    )
    return JsonResponse(list(reviews), safe=False)

@login_required(login_url='main:login_user')
def get_review_by_id(request, id):
    review = get_object_or_404(Review, pk=id)
    review_data = {
        "user": review.user.username,
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at,
        "id": review.id,
        "pk": review.pk
    }
    return JsonResponse(review_data)

@csrf_protect
@login_required(login_url='main:login_user')
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
            return redirect("marco:get_restaurant", tempatKulinerId=tempat_kuliner.id)

    # Handle any disallowed methods or get requests
    return HttpResponseForbidden("Invalid request method.")

@csrf_protect
@login_required(login_url='main:login_user')
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

@csrf_exempt
def create_review_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tempat_kuliner_id = strip_tags(data.get("tempat_kuliner_id", ""))
            rating = data.get("rating", None)
            comment = strip_tags(data.get("comment", ""))
            if not (tempat_kuliner_id and rating and comment):
                return JsonResponse(
                    {"status": "error", "message": "All fields (tempat_kuliner_id, rating, comment) are required."},
                    status=400
                )
            try:
                rating = int(rating)
            except ValueError:
                return JsonResponse(
                    {"status": "error", "message": "Rating must be an integer."},
                    status= 400
                )
            
            if rating not in [1, 2, 3, 4, 5]:
                return JsonResponse(
                    {"status": "error", "message": "Rating must be between 1 and 5."},
                    status=400
                )
            tempat_kuliner = get_object_or_404(TempatKuliner, pk=tempat_kuliner_id)
            if not request.user.is_authenticated:
                return JsonResponse(
                    {"status": "error", "message": "User must be authenticated to create a review."},
                    status=401
                )
            existing_review = Review.objects.filter(user=request.user, tempat_kuliner=tempat_kuliner).first()
            if existing_review: 
                return JsonResponse({"status": "error", "message": "You already have one review for this restaurant."}, status = 400)
           
            Review.objects.create(
                user=request.user,
                tempat_kuliner=tempat_kuliner,
                rating=rating,
                comment=comment
            )
            
            return JsonResponse(
                {"status": "success", "message": "Review created successfully."},
                status=201
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON format."},
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
                status=500
            )
    else:
        return JsonResponse(
            {"status": "error", "message": "Only POST requests are allowed."},
            status=405
        )

@csrf_exempt
@login_required
def update_review_flutter(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rating = data.get("rating", None)
            comment = strip_tags(data.get("comment", ""))

            # Validate review existence
            review = get_object_or_404(Review, pk=id)

            # Check ownership or staff
            if review.user != request.user:
                return JsonResponse(
                    {"status": "error", "message": "You do not have permission to update this review."},
                    status=403
                )

            # Validate required fields
            if rating is None or comment == "":
                return JsonResponse(
                    {"status": "error", "message": "Both rating and comment are required."},
                    status=400
                )

            try:
                rating = int(rating)
            except ValueError:
                return JsonResponse(
                    {"status": "error", "message": "Rating must be an integer."},
                    status=400
                )

            if rating not in [1, 2, 3, 4, 5]:
                return JsonResponse(
                    {"status": "error", "message": "Rating must be between 1 and 5."},
                    status=400
                )

            # Update the review
            review.rating = rating
            review.comment = comment
            review.save()

            return JsonResponse(
                {"status": "success", "message": "Review updated successfully."},
                status=200
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON format."},
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
                status=500
            )
    else:
        return JsonResponse(
            {"status": "error", "message": "Only POST requests are allowed."},
            status=405
        )

@csrf_exempt
@login_required
def delete_review_flutter(request, id):
    if request.method == 'POST':
        try:
            # Validate review existence
            review = get_object_or_404(Review, pk=id)

            # Check ownership or staff
            if review.user != request.user:
                return JsonResponse(
                    {"status": "error", "message": "You do not have permission to delete this review."},
                    status=403
                )

            # Delete the review
            review.delete()

            return JsonResponse(
                {"status": "success", "message": "Review deleted successfully."},
                status=200
            )

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
                status=500
            )
    else:
        return JsonResponse(
            {"status": "error", "message": "Only POST requests are allowed."},
            status=405
        )