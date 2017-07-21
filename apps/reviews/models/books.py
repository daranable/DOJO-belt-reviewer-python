from __future__ import unicode_literals

from django.db import models
from .authors import Author
from django.core.validators import MinLengthValidator

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=512, unique=True, validators=[
        MinLengthValidator(4)
    ])
    author = models.ForeignKey(Author, related_name='books')
