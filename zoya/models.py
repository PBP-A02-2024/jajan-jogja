from django.db import models
import uuid
from django.contrib.auth.models import User

class CommunityForum(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    jamBuka = models.TimeField()
    jamTutup = models.TimeField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    foto_link = models.TextField(default="https://cdn.britannica.com/36/123536-050-95CB0C6E/Variety-fruits-vegetables.jpg")
    variasi = models.ManyToManyField('Variasi', related_name='tempat_kuliner_set')

    def __str__(self):
        return self.nama

class Makanan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tempat_kuliner = models.ForeignKey(TempatKuliner, on_delete=models.CASCADE, related_name='makanan', null=True)
    nama = models.CharField(max_length=255)
    description = models.TextField()  
    harga = models.IntegerField()
    foto_link = models.TextField(default="https://cdn.britannica.com/36/123536-050-95CB0C6E/Variety-fruits-vegetables.jpg")

    def __str__(self):
        return self.nama
    

class Variasi(models.Model):
    nama = models.CharField(max_length=255)

    def __str__(self):
        return self.nama