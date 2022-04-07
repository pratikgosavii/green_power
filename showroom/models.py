from django.db import models
from transactions.models import *
from users.models import User
from distributor.models import distributor_outward

# Create your models here.


company_CHOICES = (
    ("yes", "Yes"),
    ("no", "No"),

)



battery_CHOICES = (
    ('lithium','Lithium'),
    ('gel', 'Gel'),
)


class customer(models.Model):

    name = models.CharField(max_length=225)
    mobile_no = models.IntegerField()
    address = models.CharField(max_length=225)
    DC_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class showroom_inward(models.Model):
    
    distributor_outward = models.ForeignKey(distributor_outward, blank=True, null= True, on_delete=models.CASCADE)
    company_outward = models.ForeignKey(outward, on_delete=models.CASCADE, blank=True, null= True, related_name='sdfdfsdx')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class showroom_request(models.Model):
    
    variant = models.ForeignKey(variant, on_delete=models.CASCADE, related_name='xcxcsxcs')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='xcxcsxcs')
    bike_qty = models.IntegerField()
    showroom = models.ForeignKey(showroom, on_delete=models.CASCADE, related_name='dfdscf')
    date = models.DateTimeField(auto_now_add=True)
    distributor = models.ForeignKey(distributor, on_delete=models.CASCADE, related_name='sdsdsx', blank=True, null= True,)



class showroom_outward(models.Model):
    
    customer = models.ForeignKey(customer, blank = True, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    battery_no = models.CharField(max_length=550)
    battery_type =models.CharField(max_length=50, blank = False, null=False, choices=battery_CHOICES, default='lithium')
    bike_qty = models.IntegerField()
    customer_service_no = models.IntegerField()


class showroom_bike_number_outward(models.Model):

    bike_number = models.ForeignKey(bike_number, on_delete=models.CASCADE, unique=True)
    outward = models.ForeignKey(showroom_outward, on_delete=models.CASCADE)
    # battery_number = models.CharField(max_length=225)
    def __str__(self):
        return self.bike_number.chasis_no


class showroom_stock(models.Model):

    variant =  models.ForeignKey(variant, on_delete=models.CASCADE)
    color =  models.ForeignKey(Color, on_delete=models.CASCADE)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    total_bike = models.IntegerField()

