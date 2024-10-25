from django.db import models
from zoya.models import TempatKuliner
# Create your mode here.

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 star'),
        (2, '2 star'),
        (3, '3 star'),
        (4, '4 star'),
        (5, '5 star')
   ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # place = models.ForeignKey()
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(null=False,blank=True)

