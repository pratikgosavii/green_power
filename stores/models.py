from email.mime import image
from pyexpat import model
from turtle import color
from django.db import models

# Create your models here.

# from users.models import User
from datetime import datetime, timezone

from django.forms import CharField
from users.models import User
from numpy import number

import pytz
ist = pytz.timezone('Asia/Kolkata')


status_CHOICES = (
    ('cash','Cash'),
    ('outofstock', 'Out of Stock'),
)

agent_status_CHOICES = (
    ('active','Active'),
    ('deactive', 'Deactive'),
)    
    

class Color(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name)
                


class variant(models.Model):

    name = models.CharField(max_length=120, unique=True)
    hsn_sac = models.CharField(max_length=120, unique=False)
    

        
    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name)





class distributor(models.Model):

    name = models.CharField(max_length=120, unique=True)
    GSTIN_no = models.CharField(max_length=120, unique=False)
    address = models.CharField(max_length=120, unique=False, blank = True, null=True)
    taluka  = models.CharField(max_length=120, unique=False, blank = False, null=False)
    district = models.CharField(max_length=120, unique=False, blank = True, null=True, )
    mobile_number =  models.IntegerField(blank = True, null=True )
    place =  models.CharField(max_length=120, blank = True, null=True, unique=False)
    status = models.CharField(max_length=50, blank = True, null=True, choices=agent_status_CHOICES, default='active')
    user = models.ForeignKey(User, unique=True, blank = False, null=False, on_delete=models.CASCADE)
    
        
    def __str__(self):
        return self.name



class showroom(models.Model):

    Distributor = models.ForeignKey(distributor , on_delete=models.CASCADE, related_name='sdsd', blank=True, null= True)
    name = models.CharField(max_length=120, unique=True)
    GSTIN_no = models.CharField(max_length=120, unique=False)
    address = models.CharField(max_length=120, unique=False, blank = False, null=False)
    taluka  = models.CharField(max_length=120, unique=False, blank = True, null=True)
    district = models.CharField(max_length=120, unique=False, blank = True, null=True, )
    mobile_number =  models.IntegerField(blank = True, null=True )
    place =  models.CharField(max_length=120, blank = True, null=True, unique=False)
    status = models.CharField(max_length=50, blank = True, null=True, choices=agent_status_CHOICES, default='active')
    user = models.ForeignKey(User, unique=True, blank = False, null=False, on_delete=models.CASCADE)
    

    
    def __str__(self):
        return self.name

    
        




class prices(models.Model):

    variant = models.ForeignKey(variant, on_delete=models.CASCADE,  unique = True, related_name='sdsdsdcxdsx')
    distributor_price = models.IntegerField(blank = False, null=False)
    dealer_price = models.IntegerField(blank = False, null=False)


