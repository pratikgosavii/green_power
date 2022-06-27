from logging import PlaceHolder
from django import forms
from django.forms.widgets import DateTimeInput

from .models import *
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime





class distributor_outward_Form(forms.ModelForm):
    class Meta:
        model = distributor_outward
        fields = '__all__'
        exclude = ['user', 'date', 'inward']
        widgets = {
            
            
            'bike_number': forms.Select(attrs={
                'class': 'form-control', 'id': 'dealer'
            }),
           'outward': forms.Select(attrs={
                'class': 'form-control', 'id': 'distributor'
            }),
            'showroom': forms.Select(attrs={
                'class': 'form-control', 'id': 'showroom', 'required' : True
            }),


        }



class distributor_return_Form(forms.ModelForm):
    class Meta:
        model = distributor_return
        fields = '__all__'
        exclude = ['user', 'date']
       



class distributor_request_Form(forms.ModelForm):
    class Meta:
        model = distributor_req
        fields = '__all__'
        widgets = {
            
            'variant': forms.Select(attrs={
                'class': 'form-control', 'id': 'bike'
            }),
            'distributor_request': forms.Select(attrs={
                'class': 'form-control', 'id': 'distributor_request'
            }),
            'color': forms.Select(attrs={
                'class': 'form-control', 'id': 'bike'
            }),
            'bike_qty': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'bike_qty'
            }),

            
        }



class distributor_payment_details_From(forms.ModelForm):
    class Meta:
        model = distributor_payment_details
        fields = '__all__'
        widgets = {
            
            'distributor_request': forms.Select(attrs={
                'class': 'form-control', 'id': 'distributor_request'
            }),
            'payment_type': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'payment_type'
            }),
            'payment_id': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'payment_id'
            }),

            
        }



# class supply_return_Form(forms.ModelForm):
#     class Meta:
#         model = supply_return
#         fields = '__all__'
#         widgets = {
#             'bike': forms.Select(attrs={
#                 'class': 'form-control', 'id': 'bike'
#             }),
#             'showroom': forms.Select(attrs={
#                 'class': 'form-control', 'id': 'showroom'
#             }),
#             'distributor': forms.Select(attrs={
#                 'class': 'form-control', 'id': 'agent'
#             }),
#             'dealer': forms.Select(attrs={
#                 'class': 'form-control', 'id': 'agent'
#             }),
#             'bike_qty': forms.NumberInput(attrs={
#                 'class': 'form-control', 'id': 'bike_qty'
#             }),
            
#             'DC_date': DateTimeInput(attrs={ 'class': 'form-control', 'type': 'datetime-local'}, format = '%Y-%m-%dT%H:%M'),

#         }

