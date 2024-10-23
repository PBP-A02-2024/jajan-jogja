from django.shortcuts import render, redirect

# Create your views here.
def food_plans_list(request):
    context = {
        'items': range(10)  # Create a list with 10 elements
    }
    return render(request, 'food_plans_list.html', context)

def food_plan(request):
    context = {
        'food_items': range(10),
        'restaurants': range(3),
        'description': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, quos. Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, quos.'
    }
    return render(request, 'food_plan.html', context)
