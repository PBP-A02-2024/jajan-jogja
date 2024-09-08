from django.shortcuts import render

def show_main(request):
    context = {
        'name' : 'Rak Sepatu Stainless Steel 5 Susun',
        'price': 35000,
        'description': 'Rak sepatu stainless steel 5 susun, minus tingkat ke 3 patah jadi sisa 4 susun, harga beli 99000 ',
        'address': 'Jl. Masjid Al-Farouq (Kos Pondok Ananda)',
    }

    return render(request, "main.html", context)