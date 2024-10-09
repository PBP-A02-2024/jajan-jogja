from django.shortcuts import render

# Create your views here.
def show_main(request):
    return render(request, 'index.html')