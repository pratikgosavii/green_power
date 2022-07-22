from logging import PlaceHolder
from django import forms
from django.forms.widgets import DateTimeInput

from .models import *
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime



class inward_Form(forms.ModelForm):
    class Meta:
        model = inward
        fields = '__all__'
        exclude = ['created_by', 'date']

        widgets = {

           'variant': forms.Select(attrs={
                'class': 'form-control', 'id': 'variant'
            }),
           
            'bike_qty': forms.NumberInput(attrs={
                'class': 'form-control modified', 'id': 'bike_qty',
            }),
            
            
        }



class outward_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(outward_Form, self).__init__(*args, **kwargs)
        self.fields['distributor'].queryset = distributor.objects.filter(status="active")
        self.fields['showroom'].queryset = showroom.objects.filter(status="active")


    class Meta:
        model = outward
        fields = '__all__'
        exclude = ['created_by', 'date']
        widgets = {
            
           'distributor': forms.Select(attrs={
                'class': 'form-control', 'id': 'distributor'
            }),

           'bike_qty': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'bike_qty', 'readonly':'readonly'
            }),
           'showroom': forms.Select(attrs={
                'class': 'form-control', 'id': 'showroom'
            }),
            

            
        }




class other_inward_Form(forms.ModelForm):

    class Meta:
        model = other_inward
        fields = '__all__'
        exclude = ['date']
        widgets = {
            
           'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'distributor'
            }),

           'price': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'bike_qty'
            }),
           'GST_rate': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'showroom'
            }),
            

            
        }

      

