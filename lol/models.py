from django.db import models

# Create your models here.
class Chopdi(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

class kopdi(models.Model):
    title1 = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField()