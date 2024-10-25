from django.shortcuts import render
from zoya.models import TempatKuliner
from django.http import HttpResponse
from django.core import serializers

def show_main(request):
    return render(request, 'landing.html')

def show_json_tempat(request):
    # data = TempatKuliner.objects.filter(user=request.user)
    data = TempatKuliner.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")