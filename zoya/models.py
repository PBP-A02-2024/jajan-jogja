from django.db import models
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
    rating = models.IntegerField()
    foto_link = models.TextField(default="https://cdn.britannica.com/36/123536-050-95CB0C6E/Variety-fruits-vegetables.jpg")
    variasi = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.nama

class Makanan(models.Model):
    tempat_kuliner = models.ForeignKey(TempatKuliner, on_delete=models.CASCADE, related_name='makanan', null=True)
    nama = models.CharField(max_length=255)
    description = models.TextField()  
    harga = models.IntegerField()
    foto_link = models.TextField(default="https://cdn.britannica.com/36/123536-050-95CB0C6E/Variety-fruits-vegetables.jpg")
    tempat_kuliner = models.ForeignKey(TempatKuliner, on_delete=models.CASCADE, related_name='makanan', null=True)

    def __str__(self):
        return self.nama