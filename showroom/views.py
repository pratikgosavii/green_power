from email import message
from email.headerregistry import Address
from genericpath import samefile
import io
from itertools import chain
from datetime import datetime
from dateutil.relativedelta import relativedelta
from logging import exception
from statistics import variance
from tabnanny import check
from tkinter import EXCEPTION
from tkinter.ttk import Style
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse, HttpResponse, JsonResponse
from transactions.forms import *
from distributor.models import *
from stores.views import numOfDays
# from transactions.filters import inward_filter, outward_filter, stock_filter
from .forms import *
from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import date
from django.urls import reverse
from datetime import date

from django.contrib.auth.decorators import user_passes_test


def showroom_required(login_url=None):
    return user_passes_test(lambda u: u.is_showroom, login_url=login_url)


#imports for bill generate

from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch,cm,mm
from django.db import IntegrityError

from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Frame, Paragraph, Spacer
import pdfkit


import csv
import mimetypes

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


from datetime import datetime
import pytz

IST = pytz.timezone('Asia/Kolkata')




# Create your views here.

@csrf_exempt
def get_outward_data(request):

    if request.method == 'POST':

        chasis_no = request.POST.get('chasis_no')
        inward_data = showroom_inward.objects.filter(user = request.user)
        print('1')
        print(inward_data)
        print('------------')
        search_data = None 

        for i in inward_data:
            
            check_outward = i.company_outward

            if check_outward == None:

                check_outward = i.distributor_outward
                
                try:
                    search_data = distributor_bike_number_outward.objects.get(outward = check_outward, bike_number__chasis_no = chasis_no)
                except distributor_bike_number_outward.DoesNotExist:
                    pass
                if search_data:
                    print('inward_match_data')
                    print(search_data)
                    break

            else:

                try:
                    search_data = bike_number_outward.objects.get(outward = check_outward, bike_number__chasis_no = chasis_no)
                except bike_number_outward.DoesNotExist:
                    pass

                if search_data:
                    print('inward_match_data')
                    print(search_data)
                    break


                    
        if search_data:

            inward_data_match = search_data.bike_number

            inward_data_match = serializers.serialize('json', [inward_data_match,], use_natural_foreign_keys=True, use_natural_primary_keys=True)

            return JsonResponse({'objectt' : inward_data_match}, safe=False)
            
        else:
            
            print('none')

            return JsonResponse({'objectt' : None}, safe=False)



@showroom_required(login_url='login')
def accept_inward(request, inward_id):

    

    data_inward = showroom_inward.objects.get(id=inward_id)
    print(data_inward)

    check_outward = data_inward.company_outward
    if check_outward:

        data = data_inward.company_outward

        print(data)


        bike_numberdata = bike_number_outward.objects.filter(outward = data)
        print('----------------------')
        print(data)
        for i in bike_numberdata:
            data = i.bike_number.chasis_no

            print(data)

            try:

                bike_data = bike_number.objects.get(chasis_no = i)

                test = showroom_stock.objects.get(bike=bike_data.inward.bike)

                test.total_bike = test.total_bike + 1
                test.save()

            except showroom_stock.DoesNotExist:

                test = showroom_stock.objects.create(bike = bike_data.inward.bike, total_bike = 1)

    else:

        data = data_inward.distributor_outward

        data = distributor_bike_number_outward.objects.filter(outward = data)
        print(data)
        for i in data:
            print('in for')
            data = i.bike_number.chasis_no

            print(data)

            try:

                bike_data = bike_number.objects.get(chasis_no = i)

                test = showroom_stock.objects.get(bike=bike_data.inward.bike)

                test.total_bike = test.total_bike + 1
                test.save()

                print('here')

            except showroom_stock.DoesNotExist:
                print('her1e')

                test = showroom_stock.objects.create(bike = bike_data.inward.bike, total_bike = 1)



    data_inward.save()

    return redirect('showroom_list_inward')



@showroom_required(login_url='login')
def add_customer(request):

    if request.method == 'POST':


        date_time = datetime.now(IST)

        updated_request = request.POST.copy()
        updated_request.update({'DC_date': date_time})
        forms = customer_Form(updated_request)

        if forms.is_valid():

            instance = forms.save(commit=False)
            instance.DC_date = date_time
            instance.save()

            return redirect('list_customer')


        else:

            
            context = {
                'form': forms,
                
            }
            return render(request, 'showroom/add_customer.html', context)


    else:

        forms = customer_Form()

        context = {
            'form': forms,
            
        }
        return render(request, 'showroom/add_customer.html', context)


@showroom_required(login_url='login')
def list_customer(request):

    data = customer.objects.all()

    context = {
            'data': data,
            
        }
    
    return render(request, 'showroom/list_customer.html', context)

@showroom_required(login_url='login')
def update_customer(request, customer_id):

    if request.method == 'POST':

        instance = customer.objects.get(id = customer_id)


        
        forms = customer_Form(request.POST, instance = instance)

        if forms.is_valid():

            forms.save()

            return redirect('list_customer')

        else:

            

            context = {
                'form': forms,
                
            }
            return render(request, 'showroom/add_customer.html', context)


    else:

        instance = customer.objects.get(id = customer_id)
        forms = customer_Form(instance = instance)

        context = {
            'form': forms,
            
        }
        return render(request, 'showroom/add_customer.html', context)


@showroom_required(login_url='login')
def add_outward(request):

    if request.method == 'POST':

        print('---------------------request.POST')
        print(request.POST)
        chasis_no = request.POST.get('chasis_no')

        print('-------cbasisis no')
        print(chasis_no)

        #checking chasiss in iwnard
        inward_data = showroom_inward.objects.filter(user = request.user)
        print('1')
        check_condition = None

        for i in inward_data:
            
            check_outward = i.company_outward

            print(check_outward)

            if check_outward == None:

                print('--------distributor--------')
                check_outward = i.distributor_outward


                check_data = distributor_bike_number_outward.objects.filter(outward = check_outward, bike_number__chasis_no=chasis_no)
                print(check_data)

                if check_data:
                   check_condition = True
                   break

            else:

                check_outward = i.company_outward

                check_data = bike_number_outward.objects.filter(outward = check_outward,  bike_number__chasis_no__in=chasis_no)

                check_condition = None

                if check_data:

                    check_condition = True
                    break

                    
        if check_condition != True:
            return JsonResponse({'status' : 'Chasis No Not exsist in inward'}, safe=False)
                

        print(' i am here')
        bike_qty = 1

        DC_date = request.POST.get('date')

        if DC_date:
            
            date_time = numOfDays(DC_date)
        else:
            date_time = datetime.now(IST)


        print('bike_qty')
        print(bike_qty)

        updated_request = request.POST.copy()
        print('0----------------------------------------')
        print(updated_request)
        updated_request.update({'date': date_time, 'bike_qty': bike_qty})
        forms = showroom_outward_Form(updated_request)

        if forms.is_valid():

            print('in valid')

            instance = forms.save(commit=False)
            print('1')

            instance.user = request.user
            print('2')

            instance.save()

            

            bike_instance = bike_number.objects.get(chasis_no = chasis_no )
            print('---biike insatancd-------')
            print(bike_instance)
            try:
                showroom_bike_number_outward.objects.create(bike_number = bike_instance, outward = instance)
                stock_instance = showroom_stock.objects.get(variant = bike_instance.inward.variant, color =  bike_instance.color, user = request.user)
                stock_instance.total_bike = stock_instance.total_bike - 1
                stock_instance.save()
            except IntegrityError as e: 
                print('in except')
                # if 'unique constraint' in e.message: # or e.args[0] from Django 1.10
                print('in if')
                return JsonResponse({'other_error' : 'Already in outward'}, safe=False)
                    
            return JsonResponse({'status' : 'done'}, safe=False)
                
        else:
            error = forms.errors.as_json()
            print(error)
            return JsonResponse({'error' : error}, safe=False)


    else:

        forms = showroom_outward_Form()

        context = {
            'form': forms,
            
        }
        return render(request, 'showroom/add_outward.html', context)


# @showroom_required(login_url='login')
# def report_dashbord(request):

#     inward_filter_data = inward_filter()
#     outward_filter_data = outward_filter()



#     context = {
#             'filter_inward': inward_filter_data,
#             'filter_outward': outward_filter_data,
#         }

#     return render(request, 'transactions/report_dashbord.html', context)


@showroom_required(login_url='login')
def list_inward(request):

   
    data = showroom_inward.objects.filter(user = request.user)

    z = showroom.objects.get(user = request.user)
    distributor = z.Distributor.name

    context = {
        'data': data,
        'distributor': distributor,
        # 'filter_outward' : outward_filter_data
    }

    return render(request, 'showroom/list_inward.html', context)


@showroom_required(login_url='login')
def view_inward(request, inward_id):

    instance = showroom_inward.objects.get(id = inward_id)
    
    if instance.company_outward != None:
        outward = instance.company_outward
        data = bike_number_outward.objects.filter(outward = outward)

    else:
        outward = instance.distributor_outward
        data = distributor_bike_number_outward.objects.filter(outward = outward)


    form = outward_Form(instance=outward)
    bike_data = []

    for i in data:
        chasis_no = i.bike_number
        li_data = bike_number.objects.get(chasis_no = chasis_no)
        bike_data.append(li_data.inward)

    data = zip(bike_data, data)
    
    context = {
        'data': data,
        'instance': instance,
        'form' : form,
        'bike_data' : bike_data
        # 'filter_outward' : outward_filter_data
    }

    
    return render(request, 'showroom/view_inward.html', context)


@showroom_required(login_url='login')
def detail_list_inward(request):

    data1 = []

    data = showroom_inward.objects.filter(user = request.user)
    for i in data:
        check = i.company_outward

        if check:
            a = bike_number_outward.objects.filter(outward = check)
            data1.append(a)
        else:
            check = i.distributor_outward
            a = distributor_bike_number_outward.objects.filter(outward = check)
            data1.append(a)

    z = showroom.objects.get(user = request.user)
    distributor = z.Distributor.name

    data = list(chain.from_iterable(data1))
    
    context = {
        'data': data,
        'distributor': distributor,
        # 'filter_inward' : inward_filter_data
    }

    return render(request, 'showroom/detail_list_inward.html', context)


@showroom_required(login_url='login')
def detail_list_outward(request):

    data1 = []

    data = showroom_outward.objects.filter(user = request.user)
    
    for i in data:

        a =  showroom_bike_number_outward.objects.filter(outward = i)

        data1.append(a)

    data = list(chain.from_iterable(data1))

    context = {
        'data': data,
        # 'filter_inward' : inward_filter_data
    }

    return render(request, 'showroom/detail_list_outward.html', context)


@showroom_required(login_url='login')
def list_outward(request):

    data = showroom_outward.objects.filter(user = request.user)

    # outward_filter_data = outward_filter()



    context = {
        'data': data,
        # 'filter_outward' : outward_filter_data
    }

    return render(request, 'showroom/list_outward.html', context)




@showroom_required(login_url='login')
def add_request(request):

    if request.method == 'POST':

        variant_get = request.POST.getlist("variant[]")
        color = request.POST.getlist("color[]")
        bike_qty = request.POST.getlist("bike_qty[]")

        print(variant_get)
        print(color)

        showroom_data = showroom.objects.get(user = request.user)
        distributor_data = showroom_data.Distributor

        instance = showroom_request.objects.create(distributor = distributor_data, showroom = showroom_data)

        print('priting instance-------------------')

        print(instance)

        updated_request = request.POST.copy()

        print(request.POST)

        for a,b,c in zip(variant_get, color, bike_qty):

            variant_data = variant.objects.get(name = a)
            color_data = Color.objects.get(name = b)

            
            updated_request.update({'variant': variant_data, 'color' : color_data, 'bike_qty' : c, 'showroom_request' : instance})
            forms = showroom_request_Form(updated_request)        
            
            
            if forms.is_valid():

                forms.save()

                print('savng')

            else:

                error = forms.errors.as_json()
                print(error)
                return JsonResponse({'error' : error}, safe=False)

        return JsonResponse({'status' : 'done'}, safe=False)

       
    else:

        forms = showroom_request_Form()

        stock_data = stock.objects.all()

        list1 = []
        list2 = []
        list3 = []
        main_list = []

        for i in stock_data:

            if i.total_bike > 0:
                list1.append(i)

       

        context = {
            'form': forms,
            'data' : list1
            
        }
        return render(request, 'showroom/add_request.html', context)

@showroom_required(login_url='login')
def update_request(request, request_id):

    instance = showroom_request.objects.get(id = request_id)

    if request.method == 'POST':

        DC_date = request.POST.get('date')

        if DC_date:
            
            date_time = numOfDays(DC_date)
        else:
            date_time = datetime.now(IST)

        updated_request = request.POST.copy()
        updated_request.update({'date': date_time})
        forms = showroom_request_Form(updated_request, instance = instance)

        if forms.is_valid():

            instance = forms.save(commit=False)
            instance.user = request.user
            instance.save()

            print('sdsdsdssd')

            return redirect('showroom_list_request')

        else:

            context = {
                'form': forms,
                
            }
            return render(request, 'showroom/add_request.html', context)


    else:

        forms = showroom_request_Form(instance = instance)

        context = {
            'form': forms,
            
        }
        return render(request, 'showroom/add_request.html', context)






@showroom_required(login_url='login')
def update_request(request, request_id):

    instance = showroom_request.objects.get(id = request_id)

    if request.method == 'POST':

        DC_date = request.POST.get('date')

        if DC_date:
            
            date_time = numOfDays(DC_date)
        else:
            date_time = datetime.now(IST)

        updated_request = request.POST.copy()
        updated_request.update({'date': date_time})
        forms = showroom_request_Form(updated_request, instance = instance)

        if forms.is_valid():

            instance = forms.save(commit=False)
            instance.user = request.user
            instance.save()

            print('sdsdsdssd')

            return redirect('showroom_list_request')

        else:

            context = {
                'form': forms,
                
            }
            return render(request, 'showroom/add_request.html', context)


    else:

        forms = showroom_request_Form(instance = instance)

        context = {
            'form': forms,
            
        }
        return render(request, 'showroom/add_request.html', context)




@showroom_required(login_url='login')
def details_request(request, request_id):

    showroom_request_instance = showroom_request.objects.get(id = request_id)
    data = showroom_req.objects.filter(showroom_request = showroom_request_instance)
    
    print(showroom_request_instance)
    print(data)

    context = {
        'data': data,
        
    }
    return render(request, 'showroom/details_request.html', context)




@showroom_required(login_url='login')
def delete_request(request, request_id):

    showroom_request.objects.get(id = request_id).delete()
    

    return redirect('showroom_list_request')


@showroom_required(login_url='login')
def list_request(request):

    showroom_data = showroom.objects.get(user = request.user)
    data = showroom_request.objects.filter(showroom = showroom_data)

    payment_update = []

    for i in data:
        try:
            a = showroom_payment_details.objects.get(showroom_request = i)
        except showroom_payment_details.DoesNotExist:
            a = None
        if a:
            payment_update.append(a)
        else:
            payment_update.append('')
    
    data = zip(data, payment_update)
    data = list(data)

    context = {
        'data': data,
        
    }


    return render(request, 'showroom/list_request.html', context)



@showroom_required(login_url='login')
# @showroom_required(login_url='login')
def download_pr(request, request_id):


    
    path = os.path.join(BASE_DIR)
    print(path)

    instance = showroom_request.objects.get(id = request_id)

    print('i am')

    return FileResponse(open(instance.pr_pdf, 'rb'), content_type='application/pdf')






@showroom_required(login_url="login")
def showroom_send_payment_detials(request, request_id):


    if request.method == 'POST':

        instance = showroom_request.objects.get(id = request_id)

        updated_request = request.POST.copy()
        updated_request.update({'showroom_request': instance})
        forms = showroom_payment_details_From(updated_request)

        if forms.is_valid():
            forms.save()

            print('saveeeeeeeeeeee')

            return redirect('showroom_list_request')

        else:

            print(forms.errors)

            

            context = {
                'form': forms,
                
            }
            
            return render(request, 'showroom/payment_details.html', context)




    else:

        form = showroom_payment_details_From()

        context = {
            'form': form,
            
        }
        
        return render(request, 'showroom/payment_details.html', context)




@showroom_required(login_url='login')
def showroom_update_payment_detials(request, payment_id):

    instance = distributor_payment_details.objects.get(id = payment_id)
    data = instance.showroom_request

    if request.method == 'POST':


        updated_request = request.POST.copy()
        updated_request.update({'showroom_request': data})
        forms = showroom_payment_details_From(updated_request, instance = instance)

        if forms.is_valid():
            forms.save()

            print('saveeeeeeeeeeee')

            return redirect('showroom_list_request')

        else:

            print(forms.errors)

            

            context = {
                'form': forms,
                
            }
            
            return render(request, 'showroom/payment_details.html', context)



    else:

        form = showroom_payment_details_From(instance = instance)

        context = {
            'form': form,
            
        }
        
        return render(request, 'showroom/payment_details.html', context)







@showroom_required(login_url='login')
# @showroom_required(login_url='login')
def update_outward(request, outward_id):


    instance = showroom_outward.objects.get(id = outward_id)
    data = showroom_bike_number_outward.objects.filter(outward = instance)

    forms = showroom_outward_Form(instance = instance)

    

    context = {
        'form': forms,
        'instance' : instance,
        'data':data,
    }
    return render(request, 'showroom/update_outward.html', context)

@showroom_required(login_url='login')
def delete_outward(request, outward_id):

    try:
        con = showroom_outward.objects.filter(id = outward_id).first()
        print('1')
        print(con)
    except distributor_outward.DoesNotExist:

        print('something went wrong')
        return HttpResponseRedirect(reverse('showroom_list_outward'))
    
    if con:

        try:

            con1 = showroom_bike_number_outward.objects.filter(outward = con)
            print('rpting con')
            print(con1)
            for z in con1:

                test = showroom_stock.objects.get(variant = z.bike_number.inward.variant, color = z.bike_number.color)
                test.total_bike = test.total_bike + 1
                test.save()
            con.delete()
            con1.delete()

            return HttpResponseRedirect(reverse('showroom_list_outward'))


        except:
            print('something went wrong')
            return HttpResponseRedirect(reverse('showroom_list_outward'))

@showroom_required(login_url='login')
def list_stock(request):

    data = showroom_stock.objects.filter(user = request.user).order_by('variant')

    # stock_filter_data = stock_filter()



    context = {
        'data': data,
        # 'stock_filter' : stock_filter_data
    }

    return render(request, 'transactions/list_stock.html', context)


def number_to_word(number):
    def get_word(n):
        words={ 0:"", 1:"One", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six", 7:"Seven", 8:"Eight", 9:"Nine", 10:"Ten", 11:"Eleven", 12:"Twelve", 13:"Thirteen", 14:"Fourteen", 15:"Fifteen", 16:"Sixteen", 17:"Seventeen", 18:"Eighteen", 19:"Nineteen", 20:"Twenty", 30:"Thirty", 40:"Forty", 50:"Fifty", 60:"Sixty", 70:"Seventy", 80:"Eighty", 90:"Ninty" }
        if n<=20:
            return words[n]
        else:
            ones=n%10
            tens=n-ones
            return words[tens]+" "+words[ones]
            
    def get_all_word(n):
        d=[100,10,100,100]
        v=["","Hundred And","Thousand","lakh"]
        w=[]
        for i,x in zip(d,v):
            t=get_word(n%i)
            if t!="":
                t+=" "+x
            w.append(t.rstrip(" "))
            n=n//i
        w.reverse()
        w=' '.join(w).strip()
        if w.endswith("And"):
            w=w[:-3]
        return w

    arr=str(number).split(".")
    number=int(arr[0])
    crore=number//10000000
    number=number%10000000
    word=""
    if crore>0:
        word+=get_all_word(crore)
        word+=" crore "
    word+=get_all_word(number).strip()+" Rupees"
    if len(arr)>1:
         if len(arr[1])==1:
            arr[1]+="0"
         word+=" and "+get_all_word(int(arr[1]))+" paisa"
    return word

@showroom_required(login_url='login')
def bill_generate_showroom_outward(request, showroom_outward_id):


    outward_data = showroom_outward.objects.get(id=showroom_outward_id)

    bike_detials = showroom_bike_number_outward.objects.get(outward=outward_data)

    all_price = []
    
    variant1 = bike_detials.bike_number.inward.variant
    hsc = variant1.hsn_sac

    p = prices.objects.get(variant = variant1)
    all_price.append(p.distributor_price)
    
    total_price = sum(all_price)
    inword_price = number_to_word(total_price)
    address = outward_data.customer.address
    mobile_no = outward_data.customer.mobile_no
    taker_name = outward_data.customer.name
    

    bike_nu = outward_data.bike_qty
    date_data = outward_data.date
    str1 = address

    if len(address) > 30:
        address = [address[i:i+30] for i in range(0, len(address), 30)]

        # initialize an empty string
        str1 = "" 
        
        # traverse in the string  
        for ele in address: 
            str1 += (ele + '\n')
    date_li = str(date_data).split(' ')
    date_data = "Date:- " + date_li[0]
    
    # data which we are going to display as tables

    DATA = [
        [ "SR NO" , "Particulars", "Rate", "Qty", "HSN/SAC", "TOTAL" ],
        [
            "01",
            "Green Power",
            total_price,
            bike_nu,
            hsc,
            total_price,
        ],
    ]

    

    DATA3 = [
        [
            "ANITA MOTORS",
            "Invoice no:-3434",
            date_data,
            
            
        ],
        [
            "Rahate complex, Jawahar Nagar,",
            "Consignee",
            "MOB NO:- " + str(mobile_no),
            
        ],
        [
            "Akola 444001.Contact:- 7020753206.",
            taker_name,
            str1,
            
        ],
        [
            "GSTIN NO=27CSZPR0818J1ZX",
            "",
            "",
            
        ],
    ]

    DATA2 = [
        [   "02",
            "MOTOR NO",
            bike_detials.bike_number.motor_no,
            

        
        ],
        [   "03",
            "CHASSIS NO",
            bike_detials.bike_number.chasis_no,


        
        ],
        [
            "04",
            "BATTERY NO",
            outward_data.battery_no,
        
        ],
        [   "05",
            "CONTROLLER NO",
            bike_detials.bike_number.controller_no,

        ],
    ]


    DATA4 = [
        [   "CGST 2.5%:-INC",
            "SGST 2.5%:-INC",

        
        ],
    ]

    DATA5 = [
        [   inword_price,
            "",
            "",
            "",
            

        
        ],
        [
            "CUSTOMER SIGNATURE",
            "FOR ANITA MOTORS",
            "TOTAL",
            total_price,
        
        ],
        [   "",
            "",
            "GST 5%",
            "INC",


        ],

        [   "",
            "Proprietor",
            "GRAND TOTAL",
            total_price,
        ],
    ]

    DATA6 = [
        [ 
            "> Battery should not be over charged, if it is seen that the battery is bulging then the warranty will be terminated.",
        ] ,

        [
            "> Get all the batteries balanced by rotating in every 3 months from your nearest dealer.",
        ],
        [  
            "> Keep the batteries away from water. Do not wash batteries. Batteries are sealed do not attempt to add acid. ",
        ],

        [  
            "> Do not accelerate and brake abruptly. Do not over load the scooter. Keep batteries cool. Charge under shade.",
        ],

        [  
            "> Once a month, Dischargebattery fully and Chargebattery fully. Charge after at-least 30 minutes of a long drive.",
        ],
    ]


    DATA7 = [
        [ 
            "> BATTERY 8+4 GAREENTY/WAREENTY.",
        ] ,

        [
            "> CONTROLLER AND MOTOR COMPLETE 1 YEAR GAREENTY.",
        ],
        
    ]

    import datetime
    import calendar

    def add_months(sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year,month)[1])
        return datetime.date(year, month, day)


    
    da_main = outward_data.date
    da = da_main.date()
    print("---------------da")
    print(da)
    d1 = add_months(da, 3)
    d2 = add_months(da, 6)
    

    DATA8 = [
        [ 

           " FOR SERVICE RELATED ISSUE CALL "
        ],
        [
            str(outward_data.customer_service_no)
        ],
        [

            "1: FIRST SERVICE 1500KM OR 3 MONTHS"
        ],
        [
            "WHICHEVER COMES FIRST " + str(d1)
        ],
        [
            "2-SECOND SERVICE 3500KM 6 MONTHS"
        ],
        [
            "WHICHEVER COMES FIRST " + str(d2)
        ] ,

        
        
    ]


    


    
    
    # creating a Base Document Template of page size A4
    from datetime import datetime


    time =  str(datetime.now(ist))
    time = time.split('.')
    time = time[0].replace(':', '-')
    name = "Bill " + time + ".pdf"
    path = os.path.join(BASE_DIR) + '\static\csv\\' + name
    
    pdf = SimpleDocTemplate(path , pagesize = A4 )
    
    # standard stylesheet defined within reportlab itself
    styles = getSampleStyleSheet()
    
    # fetching the style of Top level heading (Heading1)
    title_style = styles[ "Heading1" ]
    
    # 0: left, 1: center, 2: right
    title_style.alignment = 1
    
    # creating the paragraph with
    # the heading text and passing the styles of it
    title = Paragraph( "Tax Invoice" , title_style )
    
    # creates a Table Style object and in it,
    # defines the styles row wise
    # the tuples which look like coordinates
    # are nothing but rows and columns
    

    style = TableStyle(
        [
            
            ( "BOX" , ( 0, 0 ), ( -1, -1 ), 0 , colors.black ),
            ( "GRID" , (0, 0), ( 5, 2 ), 0, colors.black ),
            ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.black ),
            ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "CENTER" ),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTNAME', (0,0), (-1, 0), 'Times-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),


        ]
    )

    style2 = TableStyle(
        [
            
            ( "BOX" , ( 0, 0 ), ( -1, -1 ), 0 , colors.black ),
            ( "GRID" , (0, 0), ( 2 , 3 ), 0, colors.black ),
            ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.black ),
            ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "CENTER" ),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTNAME', (1,0), (1, -1), 'Times-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),



        ]
    )

    style3 = TableStyle(
        [
            
            ( "BOX" , ( 0, 0 ), ( -1, -1 ), 0 , colors.black ),
            ( "GRID" , (1, 0), (2 , 0), 0, colors.black ),
            ( "GRID" , (2, 1), (2 , 1), 0, colors.black ),
            ( 'BOX',   (1 , 0),  (1 , 3),  1,colors.black),
            ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.black ),
            ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "CENTRE" ),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('VALIGN',(-1,2),(-1,2),'TOP'),
            ('FONTNAME', (0,0), (0,0), 'Times-Bold'),
            ('FONTNAME', (0,3), (0,3), 'Times-Bold'),
            ('FONTSIZE', (0, 0), (0, 0), 11),


        ]
    )

    style4 = TableStyle(
        [
            
            ( "BOX" , ( 0, 0 ), ( -1, -1 ), 0 , colors.black ),
            ( "GRID" , (0, 0), (-1 , -1), 0, colors.black ),
            ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.black ),
            ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "CENTRE" ),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTNAME', (0,0), (-1,-1), 'Times-Bold'),



        ]
    )

    style5 = TableStyle(
        [
            
            ( "BOX" , ( 0, 0 ), ( -1, -1 ), 0 , colors.black ),
            ( "GRID" , (2, 1), (-1 , -1), 0, colors.black ),
            ( "BOX" , (0, 0), (4 , 0), 0, colors.black ),
            ( 'BOX',   (1 , 1),  (1 , 3),  1,colors.black),
            ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.black ),
            ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "LEFT" ),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTNAME', (1,1), (2,-1), 'Times-Bold'),



        ]
    )

    style6 = TableStyle(
        [
            
            ( "BOX" , ( 0, 0 ), ( -1, -1 ), 0 , colors.black ),
            ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.black ),
            ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "LEFT" ),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE')


        ]
    )
    
    style7 = TableStyle(
        [
            
            ( "BOX" , ( 0, 0 ), ( -1, -1 ), 0 , colors.black ),
            ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.black ),
            ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "CENTRE" ),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTNAME', (0,0), (-1,-1), 'Times-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 13),

        ]
    )

    style8 = TableStyle(
        [
            
            ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.black ),
            ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "CENTER" ),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 20),
        ]
    )

    
    # creates a table object and passes the style to it
    table1 = Table( DATA , style = style, colWidths=(1.5*cm, 4.5*cm, 2*cm, 2*cm, 2*cm, 6*cm), rowHeights=(1*cm, 1*cm,))
    table2 = Table( DATA2 , style = style2, colWidths=(1.5*cm, 4.5*cm, 12*cm), rowHeights=(1*cm, 1*cm, 1*cm, 1*cm,))
    table3 = Table( DATA3 , style = style3, colWidths=(6*cm, 6*cm, 6*cm), rowHeights=(1*cm, 1*cm, 1*cm, 1*cm,))
    table4 = Table( DATA4 , style = style4, colWidths=(9*cm, 9*cm), rowHeights=(1*cm))
    table5 = Table( DATA5 , style = style5, colWidths=(6.4*cm, 6.4*cm, 2.9*cm, 2.3*cm), rowHeights=(1*cm, 1*cm, 1*cm, 1*cm))
    table6 = Table( DATA6 , style = style6, colWidths=(18*cm))
    table7 = Table( DATA7 , style = style7, colWidths=(18*cm),  rowHeights=(1*cm, 1*cm))
    table8 = Table( DATA8 , style = style8, colWidths=(18*cm),  rowHeights=(2*cm, 2*cm, 3*cm, 2*cm, 3*cm, 2*cm))


    # table = [ title , table3, table1, table2, table4, table5, table6, table7, table8])
    # table.set(Style)
    flow_obj = []
    frame1 = Frame(0,10,600,800)
    frame2 = Frame(0,10,600,800)
    
    flow_obj.append(title)
    flow_obj.append(table3)
    flow_obj.append(table1)
    flow_obj.append(table2)
    flow_obj.append(table4)
    flow_obj.append(table5)
    flow_obj.append(table6)
    flow_obj.append(table7)
    pdf1 = canvas.Canvas(path)
    frame1.addFromList(flow_obj, pdf1)

    # starts page 2

    pdf1.showPage()
    flow_obj2 = []
    flow_obj2.append(table8)
    frame2.addFromList(flow_obj2, pdf1)

    # building pdf
    pdf1.save()
    with open(path, 'rb') as fh:
        mime_type  = mimetypes.guess_type('receipt.pdf')
        response = HttpResponse(fh.read(), content_type=mime_type)
        response['Content-Disposition'] = 'attachment; filename=receipt.pdf'

    return response