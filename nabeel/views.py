from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from zoya.models import Makanan, TempatKuliner, CommunityForm

from nabeel.models import Search
# import dari punya marco

# Create your views here.
@login_required(login_url='/login')
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
def search_by_keyword(request, keyword):
    list_resto = TempatKuliner.objects.filter(nama__contains=keyword) | TempatKuliner.objects.filter(variasi__contains=keyword) #filter lebih general
    context = {
        'user':request.user,
        'search_history':Search.objects.filter(user=request.user).order_by('-created_at'),
        'list_resto' : list_resto
    }
    if(request.method == "POST"):
        content = strip_tags(request.POST.get("content"))
        user = request.user
        if content:
            new_search = Search(content=content, user=user)
            new_search.save()
            return HttpResponseRedirect(reverse('nabeel:search_by_keyword', kwargs={'keyword':content}))
    return render(request, "search-page.html", context)

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
        content = request.POST.get('content')
        data.content = content
        data.save()
    return HttpResponse(b"EDITED", status=200)
