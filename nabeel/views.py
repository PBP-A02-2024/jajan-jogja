from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from zoya.models import Makanan, TempatKuliner, Variasi
import json
from nabeel.models import Search
# import dari punya marco

# Create your views here.
@login_required(login_url='main:login_user')
@csrf_exempt
def search_page(request):
    context = {
        'user':request.user,
        'list_resto':TempatKuliner.objects.all()
    }
    if(request.method == "POST"):
        content = strip_tags(request.POST.get("content"))
        user = request.user
        if content:
            new_search = Search(content=content, user=user)
            new_search.save()
            return HttpResponseRedirect(reverse('nabeel:search_by_keyword', kwargs={'keyword':content}))
    return render(request, 'search-page.html', context)

@csrf_exempt
@login_required(login_url='main:login_user')
def search_by_keyword(request, keyword):
    list_resto = TempatKuliner.objects.filter(nama__contains=keyword) #filter lebih general
    list_variasi = Variasi.objects.all()
    context = {
        'user':request.user,
        'search_history':Search.objects.filter(user=request.user).order_by('-created_at'),
        'list_resto' : list_resto,
        'keyword' : keyword,
        'list_variasi' : list_variasi
    }
    if(request.method == "POST"):
        content = strip_tags(request.POST.get("content"))
        user = request.user
        if content:
            new_search = Search(content=content, user=user)
            new_search.save()
            return HttpResponseRedirect(reverse('nabeel:search_by_keyword', kwargs={'keyword':content}))
    return render(request, "search-page.html", context)

@csrf_exempt
def delete_search_history(request, id):
    search = Search.objects.get(pk = id)
    search.delete()
    return HttpResponse(b"DELETED", status=200)

def show_search_history(request):
    data = Search.objects.filter(user=request.user).order_by('-created_at')
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_search_history_by_id(request, id):
    data = Search.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def edit_search_history(request, id):
    data = Search.objects.get(id=id)
    if request.method == "POST" and data:
        content = json.loads(request.body)["content"]
        data.content = content
        data.save()
    return HttpResponse(b"EDITED", status=200)

def show_tempat_kuliner_by_category(request, keyword, id):
    data = TempatKuliner.objects.filter(nama__contains=keyword)
    variasi = Variasi.objects.get(pk=id)
    data = data.filter(variasi=variasi)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_tempat_kuliner_by_keyword(request, keyword):
    data = TempatKuliner.objects.filter(nama__contains=keyword)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def create_search_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_search = Search.objects.create(
            user=request.user,
            content = data["content"]
        )
        new_search.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

def show_variasi(request):
    data = Variasi.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")