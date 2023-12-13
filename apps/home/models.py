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
    result = models.CharField(max_length=50)  # Assuming the result is a string

    def __str__(self):
        return f"{self.preg} - {self.gluc} - {self.blood} - {self.skin} - {self.ins} - {self.bmi} - {self.dbf} - {self.age} - {self.result}"
    
    def __str__(self):
        return f"DiabetesData - {self.result}"


class ProductData(models.Model):
    price = models.FloatField()
    radio = models.FloatField()
    in_store_spending = models.FloatField()
    discount = models.FloatField()
    tv_spending = models.FloatField()
    stock_rate = models.FloatField()
    online_ads_spending = models.FloatField()
    predicted_sale = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.price} - {self.radio} - {self.in_store_spending} - {self.discount} - {self.tv_spending} - {self.stock_rate} - {self.online_ads_spending} - {self.predicted_sale} - {self.created_at}"
    
    def __str__(self):
        return f"ProductData - {self.created_at}"  