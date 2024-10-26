from django.shortcuts import render, get_object_or_404
from zoya.models import TempatKuliner

# Create your views here.
def create_review(request, id):
    tempat_kuliner = get_object_or_404(TempatKuliner, pk=id)
    context = {'tempat_kuliner':tempat_kuliner}
    return render(request, 'review-page.html', context)