from django.db import models

#data Create your models here.
class diffQuery(models.Model):
    unitnv = models.CharField(max_length=100)
    seccode = models.CharField(max_length=100)
    trustFee = models.CharField(max_length=100)
    accumulatedUnitnv = models.CharField(max_length=100)
    manageFee = models.CharField(max_length=100)
    

