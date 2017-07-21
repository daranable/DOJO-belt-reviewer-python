from __future__ import unicode_literals

from django.db import models
from django.core.validators import MinLengthValidator

class Author(models.Model):
    first_name = models.CharField(max_length=255, validators=[
        MinLengthValidator(2)
    ])
    last_name = models.CharField(max_length=255, validators=[
        MinLengthValidator(2)
    ])
    full_name = property(lambda u: '{} {}'.format(u.first_name, u.last_name))

    class Meta:
        unique_together = ('first_name', 'last_name')
