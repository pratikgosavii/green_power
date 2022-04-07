from django import forms

from .models import *
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime



class variant_Form(forms.ModelForm):
    class Meta:
        model = variant
        fields = '__all__'
        widgets = {
            'company': forms.Select(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'pck_size'
            }),
            'hsn_sac': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'hsn_sac'
            }),
            'distributor_price': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'pck_size'
            }),
            'dealer_price': forms.NumberInput(attrs={
                'class': 'form-control cal', 'id': 'bag_size'
            }),
            
        }



class color_Form(forms.ModelForm):
    class Meta:
        model = Color
        fields = '__all__'
        widgets = {
            'color': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'pck_size'
            }),
            
        }



class showroom_Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(showroom_Form, self).__init__(*args, **kwargs)
        self.fields['Distributor'].queryset = distributor.objects.filter(status="active")



    class Meta:
        model = showroom
        fields = '__all__'
        exclude = ('user',)
        widgets = {

            'Distributor': forms.Select(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'GSTIN_no': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'GSTIN_no'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'pck_size'
            }),
            'taluka': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'pck_size'
            }),
            
            'mobile_number': forms.NumberInput(attrs={
                'class': 'form-control cal', 'id': 'bag_size'
            }),

            'place': forms.TextInput(attrs={
                'class': 'form-control cal', 'id': 'bag_size'
            }),
           
            'status': forms.Select(attrs={
                'class': 'form-control', 'id': 'status'
            }),
            
            
         }


class distributor_Form(forms.ModelForm):
    class Meta:
        model = distributor
        fields = '__all__'
        exclude = ('user',)

        widgets = {
          
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'company'
            }),
            'GSTIN_no': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'GSTIN_no'
            }),
            'taluka': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'taluka'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'taluka'
            }),
            'place': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'mobile_number'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'district'
            }),
            'mobile_number': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'mobile_number'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control', 'id': 'mobile_number'
            }),
            

        }
           



class prices_Form(forms.ModelForm):
    class Meta:
        model = prices
        fields = '__all__'
        widgets = {
           
            'variant': forms.Select(attrs={
                'class': 'form-control', 'id': 'pck_size'
            }),
            'distributor_price': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'distributor_price'
            }),
            'dealer_price': forms.NumberInput(attrs={
                'class': 'form-control cal', 'id': 'dealer_price'
            }),
           
            
        }

