# detections/models.py
from django.db import models

class Detection(models.Model):
    detected_disease = models.CharField(max_length=100)
    user_contacted_doctor = models.BooleanField(default=False)
    user_rewarded = models.BooleanField(default=False)
    doctor_rewarded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact_details = models.CharField(max_length=200)
    stellar_address = models.CharField(max_length=56,unique=True,blank=True, null=True)  # Length of Stellar public keys
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=100)
    stellar_address = models.CharField(max_length=56,unique=True,blank=True, null=True)  # Length of Stellar public keys
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
