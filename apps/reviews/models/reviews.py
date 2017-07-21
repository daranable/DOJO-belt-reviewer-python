from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator

class Review(models.Model):
    review = models.TextField(validators=[
        MinLengthValidator(10),
    ])
    rating = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(5),
    ])
    user = models.ForeignKey('log_reg.User', related_name='reviews', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', related_name='reviews', on_delete=models.CASCADE)
