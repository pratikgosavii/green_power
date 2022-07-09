from enum import unique
from django.db import models

# Create your models here.



# from users.models import User
from datetime import datetime, timezone

from django.forms import IntegerField
from traitlets import default
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
    color =  models.ForeignKey(Color, on_delete=models.CASCADE)


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
    bill_number = models.CharField(max_length=50)



class stock(models.Model):

    variant =  models.ForeignKey(variant, on_delete=models.CASCADE)
    color =  models.ForeignKey(Color, on_delete=models.CASCADE)
    total_bike = models.IntegerField()



class bike_number(models.Model):

    inward = models.ForeignKey(inward, on_delete=models.CASCADE)
    chasis_no = models.CharField(max_length=120, unique=True, blank=True, null=True)
    motor_no= models.CharField(max_length=120, unique=True, blank=True, null=True)
    controller_no = models.CharField(max_length=120, unique=True, blank=True, null=True)
    color =  models.ForeignKey(Color, on_delete=models.CASCADE)
    status =  models.BooleanField(default = True, blank=True, null=True)


    def __str__(self):
        return self.color.name

    
    def natural_key(self):
        return (self.inward.variant.name)




class bike_number_outward(models.Model):

    bike_number = models.ForeignKey(bike_number, on_delete=models.CASCADE, unique = True)
    outward = models.ForeignKey(outward, on_delete=models.CASCADE, related_name="outward_related")
    battery_number = models.CharField(max_length=225)
    price = models.IntegerField()

                                                                                                                                                                                                                                                                                   
    
    def __str__(self):
        return self.bike_number.chasis_no



class file_csv(models.Model):

    file_data = models.FileField(upload_to='static/')


    def __str__(self):
        return self.file_data

