from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import redirect, render, get_object_or_404
from zoya.models import Makanan, TempatKuliner
from reviews.models import Review
from reksa.models import FoodPlan
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def get_restaurant(request, tempatKulinerId):
    tempat_kuliner = get_object_or_404(TempatKuliner, pk=tempatKulinerId)
    has_reviewed = Review.objects.filter(user=request.user.id,tempat_kuliner=tempat_kuliner).exists()
    context = {'restoran':tempat_kuliner, 'username':request.user.username, 'restaurant_id':tempat_kuliner.id, 'has_reviewed':has_reviewed}
    return render(request, "restaurant/index.html", context)


def get_restoran_json(request, tempatKulinerId):
    tempat_kuliner = TempatKuliner.objects.filter(id=tempatKulinerId)
    return HttpResponse(serializers.serialize("json", tempat_kuliner), content_type="application/json")

def get_makanan_json(request, tempatKulinerId):
    tempat_kuliner = TempatKuliner.objects.get(id=tempatKulinerId)
    semua_makanan = tempat_kuliner.makanan.all()
    return HttpResponse(serializers.serialize("json", semua_makanan), content_type="application/json")

@login_required(login_url='main:login_user')
def get_food_plans_json(request):
    data = FoodPlan.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='main:login')
def save_food_plan(request):
    if request.method == 'POST':
        current_resto = request.POST.get('currentResto')
        resto_obj = TempatKuliner.objects.get(id=current_resto)

        makanan_id = request.POST.get('makanan_id')
        makanan_obj = Makanan.objects.get(id=makanan_id)   
        
        food_plans_data = json.loads(request.POST.get('foodPlansData', '[]'))
        selected_plan_ids = [plan['id'] for plan in food_plans_data if plan['checked']]
        unselected_plan_ids = [plan['id'] for plan in food_plans_data if not plan['checked']]

        # Tambah relasi makanan dengan foodplan
        for plan_id in selected_plan_ids:
            food_plan = FoodPlan.objects.get(id=plan_id)
            if not food_plan.makanan.filter(id=makanan_obj.id).exists():
                food_plan.tempat_kuliner.add(resto_obj)
                food_plan.makanan.add(makanan_obj)

        # Hapus relasi jika sudah ada relasi makanan dan checkbox tidak dicentang
        for plan_id in unselected_plan_ids:
            food_plan = FoodPlan.objects.get(id=plan_id)
            food_plan.check
            if food_plan.makanan.filter(id=makanan_obj.id).exists():
                food_plan.makanan.remove(makanan_obj)

        for plan_id in selected_plan_ids + unselected_plan_ids:
            food_plan = FoodPlan.objects.get(id=plan_id)
            if not food_plan.makanan.filter(tempat_kuliner=resto_obj).exists():
                # Hapus restoran jika tidak ada relasi ke makanan
                food_plan.tempat_kuliner.remove(resto_obj)  

        return redirect(f'/restaurant/{current_resto}')

    # Jika method GET
    return render(request, 'index.html')

@csrf_exempt
@login_required(login_url='main:login')
def save_food_plan_flutter(request):
    if request.method == 'POST':
        try:
            current_resto = request.POST.get('currentResto')
            resto_obj = TempatKuliner.objects.get(id=current_resto)

            makanan_id = request.POST.get('makanan_id')
            makanan_obj = Makanan.objects.get(id=makanan_id)   
            
            food_plans_data = json.loads(request.POST.get('foodPlansData', '[]'))
            selected_plan_ids = [plan['id'] for plan in food_plans_data if plan['checked']]
            unselected_plan_ids = [plan['id'] for plan in food_plans_data if not plan['checked']]

            # Tambah relasi makanan dengan foodplan
            for plan_id in selected_plan_ids:
                food_plan = FoodPlan.objects.get(id=plan_id)
                if not food_plan.makanan.filter(id=makanan_obj.id).exists():
                    food_plan.tempat_kuliner.add(resto_obj)
                    food_plan.makanan.add(makanan_obj)

            # Hapus relasi jika sudah ada relasi makanan dan checkbox tidak dicentang
            for plan_id in unselected_plan_ids:
                food_plan = FoodPlan.objects.get(id=plan_id)
                food_plan.check
                if food_plan.makanan.filter(id=makanan_obj.id).exists():
                    food_plan.makanan.remove(makanan_obj)

            for plan_id in selected_plan_ids + unselected_plan_ids:
                food_plan = FoodPlan.objects.get(id=plan_id)
                if not food_plan.makanan.filter(tempat_kuliner=resto_obj).exists():
                    # Hapus restoran jika tidak ada relasi ke makanan
                    food_plan.tempat_kuliner.remove(resto_obj)  

            return JsonResponse({'message': 'Food plan updated successfully!'}, status=200)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)