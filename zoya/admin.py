from django.contrib import admin
from .models import CommunityForum, TempatKuliner, Makanan, Variasi

# Register your models here.
admin.site.register(CommunityForum)
admin.site.register(TempatKuliner)
admin.site.register(Makanan)
admin.site.register(Variasi) 