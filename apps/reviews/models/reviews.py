from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator

class Review(models.Model):
    RATING_CHOICES = (
        (0,0),
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    )
    review = models.TextField(validators=[
        MinLengthValidator(10),
    ])
    rating = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(5),
    ],
    choices=RATING_CHOICES,
    )
    user = models.ForeignKey('log_reg.User', related_name='reviews', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', related_name='reviews', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stars = property(lambda u: ''.join("*" for i in range(u.rating)))
