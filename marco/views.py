from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from zoya.models import Makanan, TempatKuliner
# Create your views here.

def get_restaurant(request):
    return render(request, "restaurant/index.html")

def get_makanan_json(request, tempatKulinerId):
    tempat_kuliner = TempatKuliner.objects.get(id=tempatKulinerId)
    semua_makanan = tempat_kuliner.makanan.all()
    return HttpResponse(serializers.serialize("json", semua_makanan), content_type="application/json")