from django.shortcuts import render, redirect


# Create your views here.
def show_main(request):
    return render(request, 'index.html')
