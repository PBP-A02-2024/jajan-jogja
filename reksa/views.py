from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from reksa.models import FoodPlan
from zoya.models import TempatKuliner

# Create your views here.
@login_required(login_url='main:login')
def food_plans_list(request):
    food_plans = FoodPlan.objects.filter(user=request.user)
    for food_plan in food_plans:
        print(f"FoodPlan ID: {food_plan.id}")  # Debugging
    context = {
        'food_plans': food_plans
    }
    return render(request, 'food_plans_list.html', context)

@login_required(login_url='main:login')
def food_plan(request):
    context = {
        'food_items': range(10),
        'restaurants': range(3),
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, quos. Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, quos.'
    }
    return render(request, 'food_plan.html', context)

@login_required(login_url='main:login')
def food_plan_detail_view(request, food_plan_id):
    food_plan = get_object_or_404(FoodPlan, pk=food_plan_id)
    restaurants = list(food_plan.tempat_kuliner.all())

    distances = []
    for i in range(len(restaurants) - 1):
        distance = food_plan.calculate_distance(restaurants[i], restaurants[i + 1])
        distances.append(distance)

    context = {
        'food_plan': food_plan,
        'restaurants': [
            {
                'restaurant': restaurant,
                'food_items': food_plan.makanan.filter(tempat_kuliner=restaurant),
                'distance_to_next': distances[i] if i < len(distances) else None
            } for i, restaurant in enumerate(restaurants)
        ]
    }

    return render(request, 'food_plan.html', context)

@login_required(login_url='main:login')
def food_plan_create(request):
    new_food_plan = FoodPlan.objects.create(nama="Food Plan", user=request.user)
    return redirect('reksa:food_plan_detail_view', food_plan_id=new_food_plan.id)

