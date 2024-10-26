from django.db import models
from decimal import Decimal
import uuid
from django.contrib.auth.models import User

class CommunityForum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return self.comment

class TempatKuliner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=255)
    description = models.TextField()
    alamat = models.CharField(max_length=255)  
    longitude = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    jamBuka = models.DateTimeField()
    jamTutup = models.DateTimeField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, default=None)
    foto = models.ImageField()
    variasi = models.CharField(max_length=255, default="")

    def update_rating(self):
        result = self.reviews.aggregate(average=Avg('rating'))
        self.rating = Decimal(result['average']) if result['average'] is not None else None
        self.save()

    def __str__(self):
        return self.nama


class Makanan(models.Model):
    tempat_kuliner = models.ForeignKey(TempatKuliner, on_delete=models.CASCADE, related_name='makanan', null=True)
    nama = models.CharField(max_length=255)
    description = models.TextField()  
    harga = models.IntegerField()
    foto = models.ImageField()

    def __str__(self):
        return self.nama