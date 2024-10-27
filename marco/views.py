from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from zoya.models import Makanan, TempatKuliner
from reviews.models import Review
from reksa.models import FoodPlan
from django.contrib.auth.decorators import login_required
# Create your views here.

def get_restaurant(request, tempatKulinerId):
    tempat_kuliner = get_object_or_404(TempatKuliner, pk=tempatKulinerId)
    has_reviewed = Review.objects.filter(user=request.user.id).exists()
    context = {'restoran':tempat_kuliner, 'username':request.user.username, 'restaurant_id':tempat_kuliner.id, 'has_reviewed':has_reviewed}
    return render(request, "restaurant/index.html", context)

def get_makanan_json(request, tempatKulinerId):
    tempat_kuliner = TempatKuliner.objects.get(id=tempatKulinerId)
    semua_makanan = tempat_kuliner.makanan.all()
    return HttpResponse(serializers.serialize("json", semua_makanan), content_type="application/json")

@login_required(login_url='main:login')
def get_food_plans_json(request):
    data = FoodPlan.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")