from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from zoya.models import Makanan, TempatKuliner
from reksa.models import FoodPlan
from django.contrib.auth.decorators import login_required
# Create your views here.

def get_restaurant(request, tempatKulinerId):
    tempat_kuliner = TempatKuliner.objects.get(id=tempatKulinerId)
    context = {'restoran': tempat_kuliner}
    return render(request, "restaurant/index.html", context)

def get_makanan_json(request, tempatKulinerId):
    tempat_kuliner = TempatKuliner.objects.get(id=tempatKulinerId)
    semua_makanan = tempat_kuliner.makanan.all()
    return HttpResponse(serializers.serialize("json", semua_makanan), content_type="application/json")

# @login_required(login_url='main:login')
def get_food_plans_json(request):
    print(request.user)
    data = FoodPlan.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")