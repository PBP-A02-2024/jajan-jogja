from django.shortcuts import get_object_or_404, redirect, render, reverse
from zoya.models import TempatKuliner, CommunityForum, Makanan, Variasi
from zoya.forms import CommunityForumForm
from .forms import TempatKulinerForm, MakananForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

@staff_member_required
@login_required(login_url='main:login_user')
def show_main(request):
    makanan = Makanan.objects.all()[:15]
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
@login_required(login_url='main:login_user')
@staff_member_required
def delete_forum_entry(request, id):
    if request.user.is_authenticated:
        try:
            forum_entry = CommunityForum.objects.get(pk=id, user=request.user)
            forum_entry.delete()
            return HttpResponse(status=204)
        except CommunityForum.DoesNotExist:
            return HttpResponse(status=404)
    return HttpResponse(status=403)

@login_required(login_url='main:login_user')
@staff_member_required
def edit_forum_entry(request, id):
    mood = CommunityForum.objects.get(pk=id)
    form = CommunityForumForm(request.POST or None, instance=mood)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('alfian:show_main'))

    context = {'form': form}
    return render(request, "edit_forum.html", context)

@csrf_exempt
@require_POST
@login_required(login_url='main:login_user')
@staff_member_required
def add_forum_entry_ajax(request):
    comment = strip_tags(request.POST.get("comment"))
    user = request.user

    new_forum = CommunityForum(
        comment=comment,
        user=user
    )
    new_forum.save()

    return HttpResponse(b"CREATED", status=201)

@login_required(login_url='main:login_user')
@staff_member_required
def get_user_by_id(request, user_id):
    user = User.objects.get(pk=user_id)
    data = {
        "username": user.username,
    }
    return JsonResponse(data)

@login_required(login_url='main:login_user')
@staff_member_required
def get_current_user_id(request):
    if request.user.is_authenticated:
        return JsonResponse({'user_id': request.user.id})
    else:
        return JsonResponse({'user_id': None})

@require_POST
@login_required(login_url='main:login_user')
@staff_member_required
def add_tempat_kuliner_ajax(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to perform this action.")
    
    nama = strip_tags(request.POST.get("nama"))
    description = strip_tags(request.POST.get("description"))
    alamat = strip_tags(request.POST.get("alamat"))
    longitude = request.POST.get("longitude")
    latitude = request.POST.get("latitude")
    jamBuka = request.POST.get("jamBuka")
    jamTutup = request.POST.get("jamTutup")
    rating = request.POST.get("rating")
    foto_link = request.POST.get("foto_link")

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


@staff_member_required
@login_required(login_url='main:login_user')
@staff_member_required
def edit_tempat_kuliner(request, id):
    tempat = get_object_or_404(TempatKuliner, pk=id)
    form = TempatKulinerForm(request.POST or None, instance=tempat)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('alfian:show_main')
    else:
        print("Form is not valid")
        print(form.errors)
    context = {
        'form': form,  # Ensure this is a form object
        'tempat_kuliner': tempat,
    }
    return render(request, "edit_tempat_kuliner.html", context)

@require_http_methods(["DELETE"])
@login_required(login_url='main:login_user')
@staff_member_required
def delete_tempat_kuliner(request, id):
    try:
        tempat = TempatKuliner.objects.get(pk=id)

        if not (request.user.is_staff or request.user.is_superuser) :
            return HttpResponse(status=403)
        
        tempat.delete()
        return HttpResponse(status=204)
    except TempatKuliner.DoesNotExist:
        return HttpResponse(status=404)
    
@require_POST
@login_required(login_url='main:login_user')
@staff_member_required
def add_makanan_ajax(request):
    tempat_kuliner = strip_tags(request.POST.get("tempat_kuliner")) 
    nama = strip_tags(request.POST.get("nama"))
    description = strip_tags(request.POST.get("description"))
    harga = request.POST.get("harga")
    foto_link = request.POST.get("foto_link")

    new_makanan = Makanan (
        tempat_kuliner=tempat_kuliner,
        nama=nama,
        description=description,
        harga=harga,
        foto_link=foto_link
    )
    new_makanan.save()
    return HttpResponse(b"CREATED", status=201)

@login_required(login_url='main:login_user')
@staff_member_required
def edit_makanan(request, id):
    makanan = get_object_or_404(Makanan, pk=id)
    form = MakananForm(request.POST or None, instance=makanan)


    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('alfian:show_main'))
    
    else:
        print("Form is not valid")
        print(form.errors)

    context = {'form': form,
               'makanan': makanan,
               }
    return render(request, "edit_makanan.html", context)


@login_required(login_url='main:login_user')
@staff_member_required
def delete_makanan(request, id):
    makanan = get_object_or_404(Makanan, pk=id)
    makanan.delete()
    return redirect('alfian:show_main')
    
@login_required(login_url='main:login_user')
@staff_member_required
def view_tempat_makanan_admin(request, id):
    tempat = get_object_or_404(TempatKuliner, pk=id)
    return render(request, 'index_admin.html', {'restoran': tempat})

@login_required(login_url='main:login_user')
@staff_member_required
def get_restaurant(request, tempatKulinerId):
    tempat_kuliner = get_object_or_404(TempatKuliner, pk=tempatKulinerId)
    has_reviewed = Review.objects.filter(user=request.user.id,tempat_kuliner=tempat_kuliner).exists()
    context = {'restoran':tempat_kuliner, 'username':request.user.username, 'restaurant_id':tempat_kuliner.id, 'has_reviewed':has_reviewed}
    return render(request, "restaurant/index.html", context)


@login_required(login_url='main:login_user')
@staff_member_required
def get_makanan_json(request, tempatKulinerId):
    tempat_kuliner = get_object_or_404(TempatKuliner, pk=tempatKulinerId)
    semua_makanan = Makanan.objects.filter(tempat_kuliner=tempat_kuliner)
    return HttpResponse(serializers.serialize("json", semua_makanan), content_type="application/json")

@csrf_exempt
def create_resto_flutter(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "You must be logged in to create a resto."}, status=403)
        if not request.user.is_superuser:
            return JsonResponse({"status": "error", "message": "You must be an admin to create a resto."}, status=403)

        data = json.loads(request.body)
        user=request.user
        comment=data["comment"]

        if not comment or comment == "":
            return JsonResponse({"status": "error", "message": "All fields must be filled."}, status=400)

        new_resto = TempatKuliner.objects.create(
            user=user,
            comment=comment
        )

        new_resto.save()

        return JsonResponse({"status": "success", "message": "Resto successfully created."}, status=201)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)
    
@csrf_exempt
def edit_resto_flutter(request, forum_id):
    if request.method == "PUT":
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "You must be logged in to edit a resto."}, status=403)
        if not request.user.is_superuser:
            return JsonResponse({"status": "error", "message": "You must be an admin to edit a resto."}, status=403)

        data = json.loads(request.body)
        comment=data["comment"]

        if not comment or comment == "":
            return JsonResponse({"status": "error", "message": "All fields must be filled."}, status=400)

        resto = TempatKuliner.objects.get(id=forum_id)

        if resto.user != request.user:
            return JsonResponse({"status": "error", "message": "You are not authorized to edit this resto."}, status=403)
        
        resto.comment = comment
        resto.save()

        return JsonResponse({"status": "success", "message": "Resto successfully edited."}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

@csrf_exempt
def delete_resto_flutter(request, forum_id):
    if request.method == "DELETE":
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "You must be logged in to create a forum."}, status=403)

        resto = TempatKuliner.objects.get(id=forum_id)

        if resto.user != request.user:
            return JsonResponse({"status": "error", "message": "You are not authorized to delete this resto."}, status=403)

        resto.delete()

        return JsonResponse({"status": "success", "message": "Resto successfully deleted."}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)