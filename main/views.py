import datetime
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from zoya.views import show_main
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("zoya:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
       form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login_user')
    context = {'form':form}
    return render(request, 'register.html', context)

def logout_user(request):
    response = HttpResponseRedirect(reverse('zoya:show_main'))
    response.delete_cookie('last_login')
    logout(request)
    return response

@login_required(login_url='main:login_user')
def profile(request):
    user = request.user
    
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        if username:
            if User.objects.filter(username=username).exclude(pk=user.pk).exists():
                messages.error(request, "Username already taken.")
            else:
                if email:
                    user.username = username
                    user.email = email
                    user.save()
                    return redirect('main:profile')

    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)

@csrf_exempt
def edit_profile_flutter(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "You must be logged in to create a forum."}, status=403)

        data = json.loads(request.body)
        username=data["username"]
        email=data["email"]

        if not username or username == "" or not email or email == "":
            return JsonResponse({"status": "error", "message": "All fields must be filled."}, status=400)

        user = request.user

        if username:
            if User.objects.filter(username=username).exclude(pk=user.pk).exists():
                return JsonResponse({"status": "error", "message": "Username already taken."}, status=402)
            else:
                if email:
                    user.username = username
                    user.email = email
                    user.save()
                    return JsonResponse({"status": "success", "message": "Comment successfully edited."}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)