from email import charset
from django.db import models
from transactions.models import *
from users.models import User


# Create your models here.


class distributor_inward(models.Model):
    
    company_outward = models.ForeignKey(outward, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



class distributor_request(models.Model):
    
    distributor = models.ForeignKey(distributor, on_delete=models.CASCADE, related_name='dfdscf')
    date = models.DateTimeField(auto_now_add=True)
    pr_pdf = models.CharField(max_length=500)


class distributor_req(models.Model):

    distributor_request = models.ForeignKey(distributor_request, on_delete=models.CASCADE)
    variant = models.ForeignKey(variant, on_delete=models.CASCADE, related_name='sdssfsfdf')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='dcdxcdvfes')
    bike_qty = models.IntegerField()


class distributor_payment_details(models.Model):


    distributor_request = models.ForeignKey(distributor_request, on_delete=models.CASCADE, unique = True)
    payment_type = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=200)


class distributor_outward(models.Model):
    
    showroom = models.ForeignKey(showroom , blank = True, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike_qty = models.IntegerField()


class distributor_bike_number_outward(models.Model):

    bike_number = models.ForeignKey(bike_number, on_delete=models.CASCADE, unique=True)
    outward = models.ForeignKey(distributor_outward, on_delete=models.CASCADE, related_name="related")
    # battery_number = models.CharField(max_length=225)
    def __str__(self):
        return self.bike_number.chasis_no




class distributor_stock(models.Model):

    variant =  models.ForeignKey(variant, on_delete=models.CASCADE)
    color =  models.ForeignKey(Color, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_bike = models.IntegerField()

