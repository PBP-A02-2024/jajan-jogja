from django.shortcuts import render

def show_main(request):
    

    return render(request, 'landing.html')