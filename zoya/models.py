from django.db import models
import uuid

class CommunityForm(models.Model):
    nama = models.CharField(max_length=255)
    time = models.DateField(auto_now_add=True)
    comment = models.TextField()

class TempatKuliner(models.Model):
    nama = models.CharField(max_length=255)
    description = models.TextField()
    alamat = models.CharField(max_length=255)  
    longitude = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    jamBuka = models.DateTimeField()
    jamTutup = models.DateTimeField()
    rating = models.IntegerField()
    foto = models.ImageField()
    variasi = models.CharField(max_length=255, default="")

class Makanan(models.Model):
    nama = models.CharField(max_length=255)
    description = models.TextField()  
    harga = models.IntegerField()
    foto = models.ImageField()
    tempat_kuliner = models.ForeignKey(TempatKuliner, on_delete=models.CASCADE, related_name='makanan', null=True)