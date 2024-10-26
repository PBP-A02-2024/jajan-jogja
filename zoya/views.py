from django.shortcuts import render, reverse
from zoya.models import TempatKuliner, CommunityForum, Makanan
from zoya.forms import CommunityForumForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.http import JsonResponse

def show_main(request):
    makanan = Makanan.objects.all()

    context = {'makanan': makanan}

    return render(request, 'landing.html', context)

def show_json_tempat(request):
    # data = TempatKuliner.objects.filter(user=request.user)
    data = TempatKuliner.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_forum(request):
    data = CommunityForum.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_forum_by_id(request, id):
    data = CommunityForum.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_forum_entry(request, id):
    if request.user.is_authenticated:
        try:
            # Ensure that only the owner can delete the entry
            forum_entry = CommunityForum.objects.get(pk=id, user=request.user)
            forum_entry.delete()
            return HttpResponse(status=204)  # No content
        except CommunityForum.DoesNotExist:
            return HttpResponse(status=404)  # Not found
    return HttpResponse(status=403)  # Forbidden

@csrf_exempt
@require_http_methods(["POST"])
def edit_forum_entry(request, id):
    if request.user.is_authenticated:
        try:
            forum_entry = CommunityForum.objects.get(pk=id, user=request.user)
            new_comment = request.POST.get("comment", "")
            forum_entry.comment = strip_tags(new_comment)  # Sanitize the input
            forum_entry.save()
            return HttpResponse(status=200)  # OK
        except CommunityForum.DoesNotExist:
            return HttpResponse(status=404)  # Not found
    return HttpResponse(status=403)  # Forbidden

@csrf_exempt
@require_POST
def add_forum_entry_ajax(request):
    comment = strip_tags(request.POST.get("comment"))
    user = request.user

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
        # Add other fields if needed, such as first_name, last_name, etc.
    }
    return JsonResponse(data)

def get_current_user_id(request):
    if request.user.is_authenticated:
        return JsonResponse({'user_id': request.user.id})
    else:
        return JsonResponse({'user_id': None})