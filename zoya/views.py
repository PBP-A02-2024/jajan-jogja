import json
from django.shortcuts import render, reverse
from zoya.models import TempatKuliner, CommunityForum, Makanan, Variasi
from zoya.forms import CommunityForumForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.http import JsonResponse

def show_main(request):
    makanan = Makanan.objects.all()[:15]
    variasi = Variasi.objects.all()

    context = {
        'makanan': makanan,
        'variasi': variasi,
    }

    return render(request, 'landing.html', context)

def show_json_tempat(request):
    data = TempatKuliner.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_makanan(request):
    data = Makanan.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_forum(request):
    data = CommunityForum.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_forum_by_id(request, id):
    try:
        forum = CommunityForum.objects.get(pk=id)
        return JsonResponse({"comment": forum.comment})
    except CommunityForum.DoesNotExist:
        return JsonResponse({"error": "Forum not found"}, status=404)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_forum_entry(request, id):
    if request.user.is_authenticated:
        try:
            forum_entry = CommunityForum.objects.get(pk=id, user=request.user)
            forum_entry.delete()
            return HttpResponse(status=204)
        except CommunityForum.DoesNotExist:
            return HttpResponse(status=404)
    return HttpResponse(status=403)

def edit_forum_entry(request, id):
    mood = CommunityForum.objects.get(pk = id)

    form = CommunityForumForm(request.POST or None, instance=mood)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('zoya:show_main'))

    context = {'form': form}
    return render(request, "edit_forum.html", context)

@csrf_exempt
@require_POST
def add_forum_entry_ajax(request):
    comment = strip_tags(request.POST.get("comment"))
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=403)

    new_forum = CommunityForum(
        comment=comment,
        user=user
    )
    new_forum.save()

    return HttpResponse(b"CREATED", status=201)

def get_user_by_id(request, user_id):
    user = User.objects.get(pk=user_id)
    data = {
        "username": user.username,
    }
    return JsonResponse(data)

def get_current_user_id(request):
    if request.user.is_authenticated:
        return JsonResponse({'user_id': request.user.id})
    else:
        return JsonResponse({'user_id': None})

def show_json_user_by_id(request, user_id, json=True):
    user = User.objects.get(pk=user_id)
    user_json = {
        "id": user_id,
        "username": user.username,
    }

    if json:
        return JsonResponse(user_json, safe=False, status=200)
    return user_json

def show_json_current_user(request, json=True):
    if request.user.is_authenticated:
        user_json = {
            "id": request.user.id,
            "username": request.user.username,
            "is_admin": request.user.is_staff or request.user.is_superuser
        }

        if json:
            return JsonResponse(user_json, safe=False, status=200)
        return user_json
    else:
        return JsonResponse({'id': None})

@csrf_exempt
def create_forum_flutter(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "You must be logged in to create a forum."}, status=403)

        data = json.loads(request.body)
        user=request.user
        comment=data["comment"]

        if not comment or comment == "":
            return JsonResponse({"status": "error", "message": "All fields must be filled."}, status=400)

        new_forum = CommunityForum.objects.create(
            user=user,
            comment=comment
        )

        new_forum.save()

        return JsonResponse({"status": "success", "message": "Comment successfully created."}, status=201)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)
    
@csrf_exempt
def edit_forum_flutter(request, forum_id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "You must be logged in to create a forum."}, status=403)

        data = json.loads(request.body)
        comment=data["comment"]
        print(comment)

        if not comment or comment == "":
            return JsonResponse({"status": "error", "message": "All fields must be filled."}, status=400)

        community_forum = CommunityForum.objects.get(id=forum_id)

        if community_forum.user != request.user:
            return JsonResponse({"status": "error", "message": "You are not authorized to edit this comment."}, status=403)
        
        community_forum.comment = comment
        community_forum.save()

        return JsonResponse({"status": "success", "message": "Comment successfully edited."}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

@csrf_exempt
def delete_forum_flutter(request, forum_id):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "You must be logged in to create a forum."}, status=403)

        community_forum = CommunityForum.objects.get(id=forum_id)

        if community_forum.user != request.user:
            return JsonResponse({"status": "error", "message": "You are not authorized to delete this comment."}, status=403)

        community_forum.delete()

        return JsonResponse({"status": "success", "message": "Comment successfully deleted."}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)