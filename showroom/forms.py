from logging import PlaceHolder
from django import forms
from django.forms.widgets import DateTimeInput

from .models import *
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime





class showroom_outward_Form(forms.ModelForm):
    class Meta:
        model = showroom_outward
        fields = '__all__'
        exclude = ['user', 'date']
        widgets = {
            
            
            'customer': forms.Select(attrs={
                'class': 'form-control', 'id': 'customer', 'required' : True
            }),
           
            'bike_qty': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'bike_qty'
            }),

            'customer_service_no': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'customer_service_no'
            }),

            'battery_no': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'battery_no'
            }),

            'battery_type': forms.Select(attrs={
                'class': 'form-control', 'id': 'battery_type'
            }),


        }

class showroom_request_Form(forms.ModelForm):
    class Meta:
        model = showroom_request
        fields = '__all__'
        exclude = ['showroom']
        widgets = {
            
            
            'variant': forms.Select(attrs={
                'class': 'form-control', 'id': 'bike'
            }),
            'color': forms.Select(attrs={
                'class': 'form-control', 'id': 'bike'
            }),
            'bike_qty': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'bike_qty'
            }),

            'distributor': forms.Select(attrs={
                'class': 'form-control', 'id': 'distributor'
            }),
            

        }


class customer_Form(forms.ModelForm):
    class Meta:
        model = customer
        fields = '__all__'
        exclude = [ 'date']
        widgets = {
            
            
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
           'mobile_no': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'mobile_no'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'address'
            }),


        }



