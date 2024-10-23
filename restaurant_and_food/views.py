from django.shortcuts import render

# Create your views here.

def show_restaurant(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP D',
        'npm': '2306123456',
    }
      
    return render(request, "restaurant/index.html")