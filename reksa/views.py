import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.http import HttpResponse, JsonResponse
from django.core import serializers
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


def food_plan_json(request):
    food_plans = FoodPlan.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", food_plans), content_type="application/json")

def add_food_plan_item(request, food_plan_id):
    food_plan = get_object_or_404(FoodPlan, pk=food_plan_id)
    food_plan.makanan.add(request.POST.get('food_item_id'))
    return redirect('reksa:food_plan_detail_view', food_plan_id=food_plan.id)

def remove_food_plan_item(request, food_plan_id):
    food_plan = get_object_or_404(FoodPlan, pk=food_plan_id)
    food_plan.makanan.remove(request.POST.get('food_item_id'))
    return redirect('reksa:food_plan_detail_view', food_plan_id=food_plan.id)

@require_POST
def update_food_plan_title(request, food_plan_id):
    food_plan = get_object_or_404(FoodPlan, pk=food_plan_id)
    data = json.loads(request.body)
    new_title = data.get('new_title', '')
    if new_title:
        food_plan.nama = new_title
        food_plan.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@require_http_methods(["DELETE"])
def remove_food_plan_item(request, food_plan_id):
    food_plan = get_object_or_404(FoodPlan, pk=food_plan_id)
    data = json.loads(request.body)
    food_item_id = data.get('food_item_id')
    if food_item_id:
        food_plan.makanan.remove(food_item_id)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@require_http_methods(["DELETE"])
def remove_food_plan_restaurant(request, food_plan_id):
    food_plan = get_object_or_404(FoodPlan, pk=food_plan_id)
    data = json.loads(request.body)
    restaurant_id = data.get('restaurant_id')
    if restaurant_id:
        food_plan.tempat_kuliner.remove(restaurant_id)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@require_http_methods(["DELETE"])
def remove_food_plan(request, food_plan_id):
    food_plan = get_object_or_404(FoodPlan, pk=food_plan_id)
    food_plan.delete()
    return JsonResponse({'success': True})

