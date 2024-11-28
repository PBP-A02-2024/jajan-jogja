from math import radians, sin, cos, sqrt, atan2
from uuid import uuid4
from django.db import models
from zoya.models import TempatKuliner, Makanan
from django.contrib.auth.models import User
# Create your models here.
class FoodPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    tempat_kuliner = models.ManyToManyField(TempatKuliner)
    makanan = models.ManyToManyField(Makanan)

    def __str__(self):
        return self.nama
    
    def calculate_distance(self, restoran1, restoran2):
        # Hitung jarak
        if restoran1 and restoran2:
            lon1, lat1 = radians(float(restoran1.longitude)), radians(float(restoran1.latitude))
            lon2, lat2 = radians(float(restoran2.longitude)), radians(float(restoran2.latitude))
            dlon = lon2 - lon1
            dlat = lat2 - lat1

            # Rumus ngitung jarak pake latitude dan longitude
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            radius_of_earth_km = 6371  # Radius bumi
            distance = radius_of_earth_km * c

            return round(distance, 2)
        return None
    
    @property
    def jarak(self):
        restoran = self.tempat_kuliner.all()
        if not restoran.exists():
            return 0

        restoran_list = list(restoran)
        total_distance = 0

        # Ensure the restaurants are ordered. You might need to add an ordering field.
        # For this example, we'll order them by their name. Adjust as needed.
        restoran_list.sort(key=lambda x: x.nama)

        for i in range(len(restoran_list) - 1):
            distance = self.calculate_distance(restoran_list[i], restoran_list[i + 1])
            if distance:
                total_distance += distance

        return total_distance

