from enum import unique
from django.db import models

# Create your models here.



# from users.models import User
from datetime import datetime, timezone

from django.forms import IntegerField
from stores.models import *


agent_CHOICES = (
    ('dealer','Dealer'),
    ('distributor', 'Distributor'),
)

class inward(models.Model):

    variant =  models.ForeignKey(variant, on_delete=models.CASCADE)
    bike_qty =  models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    # showroom
    
    def __str__(self):
        return self.variant.name

    
    def natural_key(self):
        return (self.variant.name)

        


class bike_images(models.Model):

    bike = models.ForeignKey(inward , on_delete=models.CASCADE, related_name='sdsd')
    image = models.ImageField(upload_to = 'media')


class outward(models.Model):

    showroom = models.ForeignKey(showroom , blank = True, null=True, on_delete=models.CASCADE, related_name='vcvcxxzcv')
    distributor = models.ForeignKey(distributor, blank = True, null=True, on_delete=models.CASCADE, related_name='sdf')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    bike_qty = models.IntegerField()
    

class stock(models.Model):

    variant =  models.ForeignKey(variant, on_delete=models.CASCADE)
    color =  models.ForeignKey(Color, on_delete=models.CASCADE)
    total_bike = models.IntegerField()



class bike_number(models.Model):

    inward = models.ForeignKey(inward, on_delete=models.CASCADE)
    chasis_no = models.CharField(max_length=120, unique=True)
    motor_no= models.CharField(max_length=120, unique=True)
    controller_no = models.CharField(max_length=120, unique=True)
    color =  models.ForeignKey(Color, on_delete=models.CASCADE)


    def __str__(self):
        return self.chasis_no

    
    def natural_key(self):
        return (self.inward.variant.name)




class bike_number_outward(models.Model):

    bike_number = models.ForeignKey(bike_number, on_delete=models.CASCADE, unique = True)
    outward = models.ForeignKey(outward, on_delete=models.CASCADE)
    battery_number = models.CharField(max_length=225)

    
    def __str__(self):
        return self.bike_number.chasis_no