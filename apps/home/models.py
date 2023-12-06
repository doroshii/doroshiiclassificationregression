# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DiabetesData(models.Model):
    preg = models.FloatField()
    gluc = models.FloatField()
    blood = models.FloatField()
    skin = models.FloatField()
    ins = models.FloatField()
    bmi = models.FloatField()
    dbf = models.FloatField()
    age = models.FloatField()
    result = models.CharField(max_length=255)


