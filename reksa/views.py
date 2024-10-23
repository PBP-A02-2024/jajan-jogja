from django.shortcuts import render, redirect

# Create your views here.
def food_plans(request):
    return render(request, 'food_plans.html')

