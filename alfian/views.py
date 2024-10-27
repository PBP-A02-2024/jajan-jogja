from django.shortcuts import render, reverse
from zoya.models import TempatKuliner, CommunityForum, Makanan, Variasi
from zoya.forms import CommunityForumForm
from .forms import TempatKulinerForm, MakananForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.http import JsonResponse

def show_main(request):
    makanan = Makanan.objects.all()
    variasi = Variasi.objects.all()

    context = {
        'makanan': makanan,
        'variasi': variasi,
    }

    return render(request, 'landing_admin.html', context)

def show_json_tempat(request):
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
            forum_entry = CommunityForum.objects.get(pk=id, user=request.user)
            forum_entry.delete()
            return HttpResponse(status=204)
        except CommunityForum.DoesNotExist:
            return HttpResponse(status=404)
    return HttpResponse(status=403)

def edit_forum_entry(request, id):
    mood = CommunityForum.objects.get(pk=id)
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

@require_POST
def add_tempat_kuliner_ajax(request):
    nama = strip_tags(request.POST.get("nama"))
    description = strip_tags(request.POST.get("description"))
    alamat = strip_tags(request.POST.get("alamat"))
    longitude = strip_tags(request.POST.get("longitude"))
    latitude = strip_tags(request.POST.get("latitude"))
    jamBuka = strip_tags(request.POST.get("jamBuka"))
    jamTutup = strip_tags(request.POST.get("jamTutup"))
    rating = strip_tags(request.POST.get("rating"))
    foto_link = strip_tags(request.POST.get("foto_link"))

    new_tempat_kuliner = TempatKuliner(
        nama=nama,
        description=description,
        alamat=alamat,
        longitude=longitude,
        latitude=latitude,
        jamBuka=jamBuka,
        jamTutup=jamTutup,
        rating=rating,
        foto_link=foto_link
    )
    new_tempat_kuliner.save()

    return HttpResponse(b"CREATED", status=201)

def edit_tempat_kuliner(request, id):
    tempat = TempatKuliner.objects.get(pk=id)
    form = TempatKulinerForm(request.POST or None, instance=tempat)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('zoya:show_main'))

    context = {'form': form}
    return render(request, "edit_tempat_kuliner.html", context)

@require_http_methods(["DELETE"])
def delete_tempat_kuliner(request, id):
    try:
        tempat = TempatKuliner.objects.get(pk=id)

        if not request.user.is_staff:
            return HttpResponse(status=403)
        
        tempat.delete()
        return HttpResponse(status=204)
    except TempatKuliner.DoesNotExist:
        return HttpResponse(status=404)