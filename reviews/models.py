from django.db import models
from zoya.models import TempatKuliner
from django.contrib.auth.models import User
#
class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 star'),
        (2, '2 star'),
        (3, '3 star'),
        (4, '4 star'),
        (5, '5 star')
   ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tempat_kuliner = models.ForeignKey(TempatKuliner, null=True, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(null=False,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.tempat_kuliner}'




