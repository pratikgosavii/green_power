from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

# from users.models import User
from .models import *
from .forms import *
from .models import *

from datetime import date

from datetime import datetime
from django.urls import reverse
from django.http.response import HttpResponseRedirect, JsonResponse
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from users.views import register_distributor, register_showroom


import pytz
ist = pytz.timezone('Asia/Kolkata')

def admin_required(login_url=None):
    return user_passes_test(lambda u: u.is_superuser, login_url=login_url)

def numOfDays(date1):

    dt1 = date1.split('T')

    time = dt1[1]
    time1 = time.split(':')

    dt1 = dt1[0]
    
    dt1 = dt1.split('-')
    

    year = int(dt1[0])
    month = int(dt1[1])
    day = int(dt1[2])

    date1 = datetime(year,month, day , int(time1[0]), int(time1[1]), tzinfo=ist)

    return date1



@admin_required(login_url="login")
def add_variant(request):

    if request.method == 'POST':

        forms = variant_Form(request.POST)

        if forms.is_valid():
            form_instance = forms.save()
            request.POST = request.POST.copy()
            request.POST.update({
                "variant": form_instance
            })
            form_price = prices_Form(request.POST)
            if form_price.is_valid():
                form_price.save()
            else:
                print(form_price.errors)
            return redirect('list_variant')
        else:
            

            context = {
                'form': forms,
            }
            return render(request, 'store/add_variant.html', context)

    
    else:

        forms = variant_Form()
        form2 = prices_Form()

        context = {
            'form': forms,
            'form2': form2,
        }
        return render(request, 'store/add_variant.html', context)

        
@admin_required(login_url="login")
def update_variant(request, variant_id):

    if request.method == 'POST':

        instance = variant.objects.get(id=variant_id)

        forms = variant_Form(request.POST, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_variant')
        else:
            

            context = {
                'form': forms,
            }
            return render(request, 'store/add_variant.html', context)

    
    else:

        instance = variant.objects.get(id=variant_id)
        forms = variant_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'store/add_variant.html', context)

        
@admin_required(login_url="login")
def delete_variant(request, variant_id):

    variant.objects.get(id=variant_id).delete()

    return HttpResponseRedirect(reverse('list_variant'))


        
@admin_required(login_url="login")
def list_variant(request):

    data = variant.objects.all()

    context = {
        'data': data
    }

    return render(request, 'store/list_variant.html', context)








@admin_required(login_url="login")
def add_bike_color(request):

    if request.method == 'POST':

        forms = color_Form(request.POST)

        if forms.is_valid():
            forms.save()
            return redirect('list_bike_color')
        else:
            
            context = {
                'form': forms,
            }
            return render(request, 'store/add_bike_color.html', context)

    else:

        forms = color_Form()

        context = {
            'form': forms
        }
        return render(request, 'store/add_bike_color.html', context)

        


@admin_required(login_url="login")
def update_bike_color(request, color_id):

    if request.method == 'POST':

        instance = Color.objects.get(id=color_id)

        forms = color_Form(request.POST, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_bike_color')
        else:
            

            context = {
                'form': forms,
            }
            return render(request, 'store/add_bike_color.html', context)

    
    else:

        instance = Color.objects.get(id=color_id)
        forms = color_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'store/add_bike_color.html', context)

        
@admin_required(login_url="login")
def delete_bike_color(request, color_id):

    Color.objects.get(id=color_id).delete()

    return HttpResponseRedirect(reverse('list_bike_color'))


        
@admin_required(login_url="login")
def list_bike_color(request):

    data = Color.objects.all()

    context = {
        'data': data
    }

    return render(request, 'store/list_bike_color.html', context)


@admin_required(login_url="login")
def add_showroom(request):
    
    if request.method == 'POST':

        print('1')


        forms = showroom_Form(request.POST)


        if forms.is_valid():

            print('valid')

        
            
            print('2')

            username = request.POST.get('username')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'username exsist')
                print('exist')
                return redirect('add_showroom')

            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 == password2:

                print('3')


                test = register_showroom(request, username, password1)
                if test:
                    instance = forms.save(commit=False)
                    instance.user = test
                    instance.save()

                    return redirect('list_showroom')
                else:

                    print('4')

                    messages.error(request, test)
                    return redirect('add_showroom')
            else:
                messages.error(request, 'password does not match')
                return redirect('add_showroom')
            
        else:
            

            context = {
                'form': forms,
                # 'form_error' : form_error
            }

            return render(request, 'store/add_showroom.html', context)

    
    else:

        forms = showroom_Form()

        context = {
            'form': forms
        }

        return render(request, 'store/add_showroom.html', context)


@admin_required(login_url="login")
def update_showroom(request, showroom_id):

    if request.method == 'POST':

        instance = showroom.objects.get(id=showroom_id)

        forms = showroom_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_showroom')

        else:
            
            context = {
                'form': forms,
            }

            return render(request, 'store/update_showroom.html', context)

            
    else:

        instance = showroom.objects.get(id=showroom_id)

        forms = showroom_Form(instance = instance)

        context = {
            'form': forms
        }

        return render(request, 'store/update_showroom.html', context)

@admin_required(login_url="login")
def delete_showroom(request, showroom_id):
    
    showroom.objects.get(id=showroom_id).delete()

    return HttpResponseRedirect(reverse('list_showroom'))

@admin_required(login_url="login")
def list_showroom(request):
    
    data = showroom.objects.all()

    context = {
            'data': data
        }


    return render(request, 'store/list_showroom.html', context)




@admin_required(login_url="login")
def add_distributor(request):
    
    if request.method == 'POST':

        forms = distributor_Form(request.POST)
        if forms.is_valid():

            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'username exsist')
                print('exist')
                return redirect('add_distributor')

            if password1 == password2:

                test = register_distributor(request, username, password1)
                if test:
                    instance = forms.save(commit=False)
                    instance.user = test
                    instance.save()
                    return redirect('list_distributor')
                else:
                    messages.error(request, test)
                    return redirect('add_distributor')
            else:
                messages.error(request, 'password does not match')
                return redirect('add_distributor')


        else:

           
            showroom_data = distributor.objects.all()

            context = {
                'form': forms,
                'showroom_data' : showroom_data,
            }

            return render(request, 'store/add_distributor.html', context)


    else:

        forms = distributor_Form()

        print(forms)

        showroom_data = distributor.objects.all()

        context = {
            'form': forms,
            'showroom_data' : showroom_data
        }

        return render(request, 'store/add_distributor.html', context)

@admin_required(login_url="login")
def update_distributor(request, distributor_id):

    if request.method == 'POST':

        instance = distributor.objects.get(id=distributor_id)

        forms = distributor_Form(request.POST, instance = instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_distributor')
    
        else:

            
            context = {
                'form': forms,
            }

            return render(request, 'store/update_distributor.html', context)


    else:

        instance = distributor.objects.get(id=distributor_id)

        forms = distributor_Form(instance = instance)

        context = {
            'form': forms
        }

        return render(request, 'store/update_distributor.html', context)

@admin_required(login_url="login")
def delete_distributor(request, distributor_id):
    
    distributor.objects.get(id=distributor_id).delete()

    return HttpResponseRedirect(reverse('list_distributor'))

@admin_required(login_url="login")
def list_distributor(request):
    
    data = distributor.objects.all()

    context = {
            'data': data
        }


    return render(request, 'store/list_distributor.html', context)




@admin_required(login_url="login")
def add_prices(request):

    if request.method == 'POST':

        form = prices_Form(request.POST)
         
        if form.is_valid():
            print('save')
            form.save()

            return redirect('list_prices')
        else:

            context = {
                'form': form,
            }
            return render(request, 'store/add_prices.html', context)


    else:

        forms = prices_Form()

        context = {
            'form': forms
        }
        return render(request, 'store/add_prices.html', context)

        


        
@admin_required(login_url="login")
def update_prices(request, prices_id):

    if request.method == 'POST':

        instance = prices.objects.get(id = prices_id)

        print('in post')

        form = prices_Form(request.POST, instance=instance)
         
        if form.is_valid():
            print('save')
            form.save()
        else:
            print(form.errors)
        return redirect('list_prices')

    else:

        print('in else')

        instance = prices.objects.get(id = prices_id)

        form = prices_Form(instance = instance)

        context = {
            'form': form
        }
        return render(request, 'store/add_prices.html', context)

        
        
@admin_required(login_url="login")
def delete_prices(request, prices_id):

    prices.objects.get(id = prices_id).delete()

    return redirect('list_prices')
        
@admin_required(login_url="login")
def list_prices(request):

    data = prices.objects.all()

    context = {
        'data': data
    }

    return render(request, 'store/list_prices.html', context)



# #