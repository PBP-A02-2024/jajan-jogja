from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from zoya.models import Makanan, TempatKuliner
from reviews.models import Review
# Create your views here.

def get_restaurant(request, id):
    tempat_kuliner = get_object_or_404(TempatKuliner, pk=id)
    has_reviewed = Review.objects.filter(user=request.user).exists()
    context = {'tempat_kuliner':tempat_kuliner, 'username':request.user.username, 'restaurant_id':tempat_kuliner.id, 'has_reviewed':has_reviewed}
    return render(request, "restaurant/index.html", context)

def get_makanan_json(request, tempatKulinerId):
    tempat_kuliner = TempatKuliner.objects.get(id=tempatKulinerId)
    semua_makanan = tempat_kuliner.makanan.all()
    return HttpResponse(serializers.serialize("json", semua_makanan), content_type="application/json")