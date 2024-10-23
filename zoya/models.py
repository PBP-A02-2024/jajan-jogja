from django.db import models
import uuid

class CommunityForm(models.Model):
    nama = models.CharField(max_length=255)
    time = models.DateField(auto_now_add=True)
    comment = models.TextField()