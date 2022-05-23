from email import message
from email.headerregistry import Address
from genericpath import samefile
import io
from itertools import chain
from statistics import variance
from tkinter.ttk import Style
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import FileResponse, Http404
from django.http import FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse, HttpResponse, JsonResponse

from stores.views import numOfDays
# from transactions.filters import inward_filter, outward_filter, stock_filter
from .forms import *
from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from .models import *
from django.db import IntegrityError
from datetime import date
from django.urls import reverse
from datetime import date
from showroom.models import *

from django.contrib.auth.decorators import user_passes_test


def distributor_required(login_url=None):
    return user_passes_test(lambda u: u.is_distributor, login_url=login_url)


#imports for bill generate

from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch,cm,mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Frame, Paragraph, Spacer
import pdfkit

from  transactions.forms import outward_Form

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

        inward_data_match = None
       
        chasis_no = request.POST.get('chasis_no')
        
        print('chasis_no')
        print(chasis_no)

        inward_data = distributor_inward.objects.filter(user = request.user)
        print('inward_data')
        print(inward_data)
        print('--------------')

        search_data = None

        for y in inward_data:

            try:
                search_data = bike_number_outward.objects.get(outward = y.company_outward, bike_number__chasis_no = chasis_no)
            
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
            

@distributor_required(login_url='login')
def accept_inward(request, inward_id):

    data_inward = distributor_inward.objects.get(id=inward_id)
    data = data_inward.company_outward
    data = bike_number_outward.objects.filter(outward = data)

    for i in data:
        data = i.bike_number.chasis_no

        print(data)

        try:

            bike_data = bike_number.objects.get(chasis_no = i)

            test = distributor_stock.objects.get(bike=bike_data.inward.bike)

            test.total_bike = test.total_bike + 1
            test.save()

        except distributor_stock.DoesNotExist:

            test = distributor_stock.objects.create(bike = bike_data.inward.bike, total_bike = 1)

    data_inward.save()
            

    return redirect('distributor_list_inward')


@distributor_required(login_url='login')
def add_outward(request):

    if request.method == 'POST':

        chasis_no = request.POST.getlist('chasis_no[]')
        set_chasis_no = set(chasis_no)
        
        #checking for inward
        match_inward_data = distributor_inward.objects.filter(user = request.user)

        for i in match_inward_data:
            match_data = bike_number_outward.objects.filter(outward = i.company_outward, bike_number__chasis_no__in=list(set_chasis_no))
            
            if match_data:
                for i in match_data:
                    i2 = i.bike_number.chasis_no
                    set_chasis_no.remove(i2)
        if set_chasis_no:
            msgg = str(set_chasis_no) + ' not exist in inward'
            return JsonResponse({'status' : msgg}, safe=False)
        
        #checking for outward
        match_outward_data = distributor_outward.objects.filter(user = request.user)
        print('match_outward_data')
        outward_exist = []
        print(match_outward_data)
        for i in match_outward_data:
            match_data = distributor_bike_number_outward.objects.filter(outward = i, bike_number__chasis_no__in=chasis_no)
            print('---------------------')
            print(match_data)
            if match_data:
                for z in match_data:
                    outward_exist.append(z.bike_number.chasis_no)
        if outward_exist:
            msgg = str(outward_exist) + ' already exist in outward'
            return JsonResponse({'status' : msgg}, safe=False)
                
        print('outside of loop')

        DC_date = request.POST.get('date')

        if DC_date:
            
            date_time = numOfDays(DC_date)
        else:
            date_time = datetime.now(IST)

        bike_qty = len(chasis_no)

        updated_request = request.POST.copy()
        updated_request.update({'date': date_time, 'bike_qty': bike_qty})
        forms = distributor_outward_Form(updated_request)

        if forms.is_valid():

            instance = forms.save(commit=False)
            instance.user = request.user
            instance.save()


            showroom_data = forms.cleaned_data['showroom']

            chasis_no = list(chasis_no)

            print(chasis_no)

            for i in chasis_no:
              
                bike_instance = bike_number.objects.get(chasis_no = i)
                print('------------')
                print(i)
                print(bike_instance)
                try:
                    
                    distributor_bike_number_outward.objects.create(bike_number = bike_instance, outward = instance)
                    print('----------')
                    print(bike_instance)
                    test = distributor_stock.objects.get(variant = bike_instance.inward.variant, color = bike_instance.color, user = request.user)

                    if test.total_bike > 0:

                        test.total_bike = test.total_bike - 1
                        test.save()

                    # else:
                    #     messages.error(request, "Outward is more than Stock")
                    #     print('Outward is more than Stock')
                    #     return JsonResponse({'status' : 'Outward is more than Stock'}, safe=False)

                except IntegrityError as e: 
                    return JsonResponse({'other_error' : 'Unique contraint fail'}, safe=False)

                user_data = showroom.objects.get(id = showroom_data.id)
                user_data = user_data.user


                try:

                    test = showroom_stock.objects.get(variant=bike_instance.inward.variant, color = bike_instance.color, user = user_data)

                    test.total_bike = test.total_bike + 1
                    test.save()

                except showroom_stock.DoesNotExist:

                    test = showroom_stock.objects.create(variant = bike_instance.inward.variant, color = bike_instance.color, total_bike = 1, user = user_data)

            
            showroom_inward.objects.create(distributor_outward = forms.instance, company_outward = None, user = user_data)

            return JsonResponse({'status' : 'done'}, safe=False)

        else:

            error = forms.errors.as_json()
            print(error)
            return JsonResponse({'error' : error}, safe=False)


    else:

        forms = distributor_outward_Form()

        distributor_data = distributor.objects.get(user=request.user)
  
        showroom_data = showroom.objects.filter(Distributor = distributor_data)
        print(showroom_data)





        bike_numbers = []

        distributor_in_ = outward.objects.filter(distributor = distributor_data)
        
        for i in distributor_in_:
            bike_number_ = bike_number_outward.objects.filter(outward = i)

            for y in bike_number_:
                bike_numbers.append(y.bike_number)

        match_inward_data = distributor_inward.objects.filter(user = request.user)

       
        bike_numbers1 = distributor_bike_number_outward.objects.all()

        bike_numbers = list(bike_numbers)
        bike_numbers1 = list(bike_numbers1)

        data = zip(bike_numbers, bike_numbers1)
        for i,y in data:

            if i.chasis_no in y.bike_number.chasis_no:

                bike_numbers.remove(i)

        context = {
            'form': forms,
            'showroom_data' : showroom_data,
            'bike_numbers' : bike_numbers,
            
        }
        return render(request, 'distributor/add_outward.html', context)



@distributor_required(login_url='login')
def view_inward(request, inward_id):

    instance = distributor_inward.objects.get(id = inward_id)
    
    outward = instance.company_outward
    data = bike_number_outward.objects.filter(outward = outward)
    form = outward_Form(instance=outward)
    bike_data = []

    for i in data:
        chasis_no = i.bike_number
        li_data = bike_number.objects.get(chasis_no = chasis_no)
        bike_data.append(li_data.inward)

    data1 = zip(bike_data, data)
    
    context = {
        'data': data1,
        'instance': instance,
        'form' : form,
        'bike_data' : bike_data
        # 'filter_outward' : outward_filter_data
    }

    
    return render(request, 'distributor/view_inward.html', context)



@distributor_required(login_url='login')
def list_inward(request):


    
    data = distributor_inward.objects.filter(user = request.user)
    

    context = {
        'data': data,
        # 'filter_outward' : outward_filter_data
    }

    return render(request, 'distributor/list_inward.html', context)



@distributor_required(login_url='login')
def list_outward(request):

    data = distributor_outward.objects.filter(user = request.user)

    # outward_filter_data = outward_filter()



    context = {
        'data': data,
        # 'filter_outward' : outward_filter_data
    }

    return render(request, 'distributor/list_outward.html', context)



@distributor_required(login_url='login')
def detail_list_inward(request):

    data = []

    check = distributor_inward.objects.filter(user = request.user)

    for i in check:

        a = bike_number_outward.objects.filter(outward = i.company_outward)
        data.append(a)

    data = list(chain.from_iterable(data))

    print(data)


    context = {
        'data': data,
        # 'filter_inward' : inward_filter_data
    }

    return render(request, 'distributor/detail_list_inward.html', context)


@distributor_required(login_url='login')
def detail_list_outward(request):

    details = []
    data1 = []

    data = distributor_outward.objects.filter(user = request.user)
    print(data)
    for i in data:


        number_data =  distributor_bike_number_outward.objects.filter(outward = i)
        print(number_data)
        for n in number_data:

            data1.append(n.bike_number.inward.variant)
            data1.append(n.bike_number.color)
            data1.append(n.bike_number.chasis_no)
            data1.append(n.bike_number.motor_no)
            data1.append(n.bike_number.controller_no)
            data1.append(i.showroom)
            data1.append(i.date)
            data1.append(i.id)

            details.append(data1)

            data1 = []

    print(details)

    context = {
        'data': details,
        # 'filter_inward' : inward_filter_data
    }

    return render(request, 'distributor/detail_list_outward.html', context)




@distributor_required(login_url='login')
def update_outward(request, outward_id):


    # if request.method == 'POST':

    #     instance = distributor_outward.objects.get(id = outward_id)

    #     DC_date = request.POST.get('date')

    #     if DC_date:

    #         date_time = numOfDays(DC_date)
    #     else:
    #         date_time = datetime.now(IST)

    #     updated_request = request.POST.copy()
    #     updated_request.update({'date': date_time})

    #     forms = distributor_outward_Form(updated_request, instance = instance)

    #     if forms.is_valid():
    #         forms.save()

    #         return redirect('distributor_list_outward')

    #     else:
    #         form_error = forms.errors

    #         instance = distributor_outward.objects.get(id = outward_id)
    #         data = distributor_bike_number_outward.objects.filter(outward = instance)

    #         forms = distributor_outward_Form(instance = instance)

    #         context = {
    #             'form': forms,
    #             'data':data,
    #             'form_error' : form_error
    #         }
    #         return render(request, 'distributor/update_outward.html', context)

    # else:

    instance = distributor_outward.objects.get(id = outward_id)
    data = distributor_bike_number_outward.objects.filter(outward = instance)

    forms = distributor_outward_Form(instance = instance)

    distributor_data = distributor.objects.get(user=request.user)
    showroom_data = showroom.objects.filter(Distributor = distributor_data)
    showroom_id = instance.showroom.id


    context = {
        'form': forms,
        'data':data,
        'instance':instance,
        'showroom_data' : showroom_data,
        'showroom_id' : showroom_id
    }
    return render(request, 'distributor/update_outward.html', context)



@distributor_required(login_url='login')
def delete_outward(request, outward_id):

    print('in delte')
    try:
        con = distributor_outward.objects.filter(id = outward_id).first()
        print('1')
        print(con)
    except distributor_outward.DoesNotExist:

        print('something went wrong')
        return HttpResponseRedirect(reverse('distributor_list_outward'))
    
    if con:


        data = distributor_bike_number_outward.objects.filter(outward = con)

        for y in data:
                    
            try:
                data1 = bike_number_outward.objects.get(bike_number = y.bike_number)
            except bike_number_outward.DoesNotExist:
                data1 = None
                pass
            

            if data1:

                a = showroom_bike_number_outward.objects.all()

                for y in a:

                    if y.bike_number.chasis_no in data1.bike_number.chasis_no:

                        msg  = "Cant delete Outward, bike is already in outward of distributor hn"

                        data = distributor_outward.objects.filter(user = request.user)

                        context = {
                            'data': data,
                            'msg': msg,
                            # 'filter_outward' : outward_filter_data
                        }

                        return render(request, 'distributor/list_outward.html', context)

                     

        try:

            con1 = distributor_bike_number_outward.objects.filter(outward = con)
            print('printing con')
            print(con1)
            for z in con1:

                test = distributor_stock.objects.get(variant = z.bike_number.inward.variant, color = z.bike_number.color)
                test.total_bike = test.total_bike + 1
                test.save()
            con.delete()
            con1.delete()

            return HttpResponseRedirect(reverse('distributor_list_outward'))


        except distributor_stock.DoesNotExist:

            print('something went wrong')
            return HttpResponseRedirect(reverse('distributor_list_outward'))



@distributor_required(login_url='login')
def list_stock(request):

    data = distributor_stock.objects.filter(user = request.user).order_by('variant')

    context = {
        'data': data,
        # 'stock_filter' : stock_filter_data
    }

    return render(request, 'transactions/list_stock.html', context)


@distributor_required(login_url='login')
def add_request(request):

    if request.method == 'POST':

      
        variant_get = request.POST.getlist("variant[]")
        color = request.POST.getlist("color[]")
        bike_qty = request.POST.getlist("bike_qty[]")

        distributor_data = distributor.objects.get(user = request.user)

        instance = distributor_request.objects.create(distributor = distributor_data)

        for a,b,c in zip(variant_get, color, bike_qty):

            variant_data = variant.objects.get(name = a)
            color_data = Color.objects.get(name = b)

            updated_request = request.POST.copy()
            updated_request.update({'variant': variant_data, 'color' : color_data, 'bike_qty' : c, 'bike_qty' : c, 'distributor_request' : instance})
            forms = distributor_request_Form(updated_request)        


            if forms.is_valid():

                forms.save()

                print('saveeee')

            else:

                error = forms.errors.as_json()
                print(error)
                return JsonResponse({'error' : error}, safe=False)

            
        return JsonResponse({'data' : 'done'}, safe=False)



       

    else:

        forms = distributor_request_Form()

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
        return render(request, 'distributor/add_request.html', context)

@distributor_required(login_url='login')
def update_request(request, request_id):

    instance = distributor_request.objects.get(id = request_id)

    if request.method == 'POST':

        DC_date = request.POST.get('date')

        if DC_date:
            
            date_time = numOfDays(DC_date)
        else:
            date_time = datetime.now(IST)

        updated_request = request.POST.copy()
        updated_request.update({'date': date_time})
        forms = distributor_request_Form(updated_request, instance = instance)

        if forms.is_valid():

            instance = forms.save(commit=False)
            instance.user = request.user
            instance.save()

            print('sdsdsdssd')

            return redirect('distributor_list_request')

        else:

            context = {
                'form': forms,
                
            }
            return render(request, 'distributor/add_request.html', context)


    else:

        forms = distributor_request_Form(instance = instance)

        context = {
            'form': forms,
            
        }
        return render(request, 'distributor/add_request.html', context)


@distributor_required(login_url='login')
def list_request(request):

    distributor_data = distributor.objects.get(user = request.user)
    data = distributor_request.objects.filter(distributor = distributor_data)

    payment_update = []

    for i in data:
        try:
            a = distributor_payment_details.objects.get(distributor_request = i)
        except distributor_payment_details.DoesNotExist:
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
    return render(request, 'distributor/list_request.html', context)


@distributor_required(login_url='login')
def details_request(request, request_id):

    request_instance = distributor_request.objects.get(id = request_id)
    data = distributor_req.objects.filter(distributor_request = request_instance)
    

    context = {
        'data': data,
        
    }
    return render(request, 'distributor/details_request.html', context)


@distributor_required(login_url='login')
def delete_request(request, request_id):

    data = distributor_request.objects.get(id = request_id).delete()
    

    return redirect('distributor_list_request')


@distributor_required(login_url='login')
def download_pr(request, request_id):

    
    path = os.path.join(BASE_DIR)
    print(path)

    instance = distributor_request.objects.get(id = request_id)

    print('i am')

    return FileResponse(open(instance.pr_pdf, 'rb'), content_type='application/pdf')




@distributor_required(login_url="login")
def distributor_send_payment_detials(request, request_id):


    if request.method == 'POST':

        instance = distributor_request.objects.get(id = request_id)

        updated_request = request.POST.copy()
        updated_request.update({'distributor_request': instance})
        forms = distributor_payment_details_From(updated_request)

        if forms.is_valid():
            forms.save()

            print('saveeeeeeeeeeee')

            return redirect('distributor_list_request')

        else:

            print(forms.errors)

            

            context = {
                'form': forms,
                
            }
            
            return render(request, 'distributor/payment_details.html', context)




    else:

        form = distributor_payment_details_From()

        context = {
            'form': form,
            
        }
        
        return render(request, 'distributor/payment_details.html', context)




@distributor_required(login_url='login')
def distributor_update_payment_detials(request, payment_id):

    instance = distributor_payment_details.objects.get(id = payment_id)
    data = instance.distributor_request

    if request.method == 'POST':


        updated_request = request.POST.copy()
        updated_request.update({'distributor_request': data})
        forms = distributor_payment_details_From(updated_request, instance = instance)

        if forms.is_valid():
            forms.save()

            print('saveeeeeeeeeeee')

            return redirect('distributor_list_request')

        else:

            print(forms.errors)

            

            context = {
                'form': forms,
                
            }
            
            return render(request, 'distributor/payment_details.html', context)



    else:

        form = distributor_payment_details_From(instance = instance)

        context = {
            'form': form,
            
        }
        
        return render(request, 'distributor/payment_details.html', context)





@distributor_required(login_url='login')
def view_request(request):

    instance = distributor.objects.get(user =  request.user)
    
    data = showroom_request.objects.filter(distributor = instance)

    payment_update = []

    for i in data:
        try:
            a = showroom_payment_details.objects.get(showroom_request = i)
            print('priting a ')
            print(a)
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
    return render(request, 'distributor/view_request.html', context)



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





@distributor_required(login_url="login")
def  showroom_view_pr(request, request_id, pathneeded = None):


    request_data = showroom_request.objects.get(id=request_id)
    
    
    data = showroom_req.objects.filter(showroom_request = request_data)


    print('data')
    print(data)

    dfsdfs = 1

    if dfsdfs == 1:

        print(data)
        all_price = []

    
        
        for i in data:
            
            variant1 = i.variant
            p = prices.objects.get(variant = variant1)
            all_price.append(p.dealer_price)
            
            address = request_data.showroom.address
            taker_name = request_data.showroom.name
            gst = request_data.showroom.GSTIN_no
            
       
        print(all_price)
       
        date_data = request_data.date
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


        
        list_1 = []
        list_2 = []
        grand_total = []
        list_1.append([ "SR NO" , "Particulars", "Rate", "Qty", "HSN/SAC", "TOTAL" ])

        count = 1

        for i in data:

            rate = prices.objects.get(variant = i.variant)

            hsc = i.variant.hsn_sac

            total = int(rate.dealer_price) * int(i.bike_qty)
            


            list_2 = []

            list_2.append(count)
            list_2.append(i.variant)
            list_2.append(rate.dealer_price)
            list_2.append(i.bike_qty)
            list_2.append(hsc)
            list_2.append(total)
            grand_total.append(total)
            list_1.append(list_2)

            count = count + 1

        print(list_1)

        grand_total = sum(grand_total)

        grand_total_price = ((grand_total / 100) * 5) + grand_total

        inword_price = number_to_word(grand_total_price)



        DATA = list_1


        
        

        DATA3 = [
            [
                "ANITA MOTORS",
                "Invoice no:-3434",
                date_data,
                
                
            ],
            [
                "Rahate complex, Jawahar Nagar,",
                "Consignee",
                "Payment= NEFT/RTGS"
            ],
            [
                "Akola 444001.Contact:- 7020753206.",
                taker_name,
                str1 + '\n' +  "GSTIN NO=" + gst,
                
            ],
            [
                "GSTIN NO=27CSZPR0818J1ZX",
                "",
                "",
                
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
                grand_total,
            
            ],
            [   "",
                "",
                "GST 5%",
                "INC",


            ],

            [   "",
                "Proprietor",
                "GRAND TOTAL",
                grand_total_price,
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


        
        
        # creating a Base Document Template of page size A4

        time =  str(datetime.now(ist))
        time = time.split('.')
        time = time[0].replace(':', '-')
        name = "Bill " + time + ".pdf"
        path = os.path.join(BASE_DIR) + '\media\\' + name
        
        pdf = SimpleDocTemplate(path , pagesize = A4 )
        
        # standard stylesheet defined within reportlab itself
        styles = getSampleStyleSheet()
        
        # fetching the style of Top level heading (Heading1)
        title_style = styles[ "Heading1" ]
        
        # 0: left, 1: center, 2: right
        title_style.alignment = 1
        
        # creating the paragraph with
        # the heading text and passing the styles of it
        title = Paragraph( "PR" , title_style )
        
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
                
                ( "BOX" , ( 0, 0 ), ( -1, -1 ), 0 , colors.black ),
                ( "GRID" , (0, 0), ( -1, -1 ), 0, colors.black ),
                ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.black ),
                ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "CENTER" ),
                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
            
            ]
        )

        
        # creates a table object and passes the style to it
        table1 = Table( DATA , style = style, colWidths=(1.5*cm, 4.5*cm, 2*cm, 2*cm, 2*cm, 6*cm), rowHeights=(1*cm, 1*cm,))
        table3 = Table( DATA3 , style = style3, colWidths=(6*cm, 6*cm, 6*cm), rowHeights=(1*cm, 1*cm, 1*cm, 1*cm,))
        table4 = Table( DATA4 , style = style4, colWidths=(9*cm, 9*cm), rowHeights=(1*cm))
        table5 = Table( DATA5 , style = style5, colWidths=(6.4*cm, 6.4*cm, 2.9*cm, 2.3*cm), rowHeights=(1*cm, 1*cm, 1*cm, 1*cm))
        table6 = Table( DATA6 , style = style6, colWidths=(18*cm))
        table7 = Table( DATA7 , style = style7, colWidths=(18*cm),  rowHeights=(1*cm, 1*cm))


        # table = [ title , table3, table1, table2, table4, table5, table6, table7, table8])
        # table.set(Style)
        flow_obj = []
        frame1 = Frame(0,10,600,800)
        frame2 = Frame(0,10,600,800)
        flow_obj.append(title)
        flow_obj.append(table3)
        flow_obj.append(table1)
        flow_obj.append(table4)
        flow_obj.append(table5)
        flow_obj.append(table6)
        flow_obj.append(table7)
        pdf1 = canvas.Canvas(path)
        frame1.addFromList(flow_obj, pdf1)

       

        # building pdf
        pdf1.save()

        if pathneeded == True:

            return path


        print('-')
        print('-')
        print('-')
        print('-')
        print('-')

        print(path)



        
        return FileResponse(open(path, 'rb'), content_type='application/pdf')







@distributor_required(login_url='login')
def showroom_send_pr(request, request_id):

    a = showroom_view_pr(request, request_id, pathneeded = True)
    print('----path---')
    print(a)
    try:
        ins = showroom_request.objects.get(id = request_id)
        ins.pr_pdf = a
        ins.save()
    except showroom_request.DoesNotExist:
        showroom_request.objects.create(showroom_request = instance, pr_pdf = a)

    
    instance = showroom_request.objects.get(id = request_id)
    data = showroom_req.objects.filter(showroom_request = instance)

    msg = "PR send sucessfullly"
    data = showroom_request.objects.all()

    payment_update = []

    for i in data:
        try:
            a = showroom_payment_details.objects.get(showroom_request = i)
            print('priting a ')
            print(a)
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
        'msg': msg,
    }

    return render(request, 'distributor/view_request.html', context)

    




from showroom.forms import *

@distributor_required(login_url="login")
def view_payment_detials(request, payment_id):

    data = showroom_payment_details.objects.get(id = payment_id)

    data = showroom_payment_details_From(instance = data)

    context = {
        'form' : data
    }

    return render(request, 'distributor/view_payment.html', context)







@distributor_required(login_url='login')
def bill_generate_distributor_outward(request, distributor_outward_id):


    
    outward_data = distributor_outward.objects.get(id=distributor_outward_id)

    if outward_data.bike_qty > 1:

        bike_number_outward_data = distributor_bike_number_outward.objects.filter(outward=outward_data)
        print(bike_number_outward_data)
        all_price = []

        

        print('in outward')

        for i in bike_number_outward_data:
            variant1 = i.bike_number.inward.variant
            p = prices.objects.get(variant = variant1)
            all_price.append(p.dealer_price)
            
        total_price = sum(all_price)
        address = outward_data.showroom.address
        mobile_no = outward_data.showroom.mobile_number
        taker_name = outward_data.showroom.name
        gst = outward_data.showroom.GSTIN_no


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


        list_1 = []
        list_2 = []
        grand_total = []
        list_1.append([ "SR NO" , "Particulars", "Rate", "Qty", "HSN/SAC", "TOTAL" ])

        count = 1


        Dict1 = {}
        
        for i in bike_number_outward_data:


            if i.bike_number.inward.variant in Dict1:

                val = Dict1[i.bike_number.inward.variant]
                print('val')
                print(val)
                Dict1.update({ i.bike_number.inward.variant : (val + 1) })
            else:

                Dict1[i.bike_number.inward.variant] = 1

        
        print(Dict1)

        for key, value in Dict1.items():


            rate = prices.objects.get(variant = key)

            hsc = key.hsn_sac

            total = int(rate.dealer_price) * int(value)
            grand_total.append(total)


            list_2 = []

            list_2.append(count)
            list_2.append(key)
            list_2.append(rate.dealer_price)
            list_2.append(value)
            list_2.append(hsc)
            list_2.append(total)
            grand_total.append(total)
            list_1.append(list_2)

            count = count + 1

        print(list_1)

        grand_total = sum(grand_total)

        grand_total_price = ((grand_total / 100) * 5) + grand_total

        inword_price = number_to_word(grand_total_price)


        DATA = list_1


        

        DATA3 = [
            [
                "ANITA MOTORS",
                "Invoice no:-3434",
                date_data,
                
                
            ],
            [
                "Rahate complex, Jawahar Nagar,",
                "Consignee",
                "M0B NO:- " + str(mobile_no),
                
            ],
            [
                "Akola 444001.Contact:- 7020753206.",
                taker_name,
                str1 + '\n' +  "GSTIN NO=" + gst,
                
            ],
            [
                "GSTIN NO=27CSZPR0818J1ZX",
                "",
                "",
                
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
                grand_total,
            
            ],
            [   "",
                "",
                "GST 5%",
                "INC",


            ],

            [   "",
                "Proprietor",
                "GRAND TOTAL",
                grand_total_price,
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


        next_data = []
        DATA8 = []
        DATA9 = []
        cou = 1

        a = ['0', 'Chasis No', 'Motor No', 'Controller No']

        DATA8.append(['0', 'Variant', 'Color', 'Chasis No', 'Motor No', 'Controller No'])

        for i in bike_number_outward_data:

            next_data.append(cou)
            next_data.append(i.bike_number.inward.variant)
            next_data.append(i.bike_number.color)
            next_data.append(i.bike_number.chasis_no)
            next_data.append(i.bike_number.motor_no)
            next_data.append(i.bike_number.controller_no)

            cou = cou + 1

            DATA8.append(next_data)

            next_data = []



        
        
        # creating a Base Document Template of page size A4

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
                
                ( "BOX" , ( 0, 0 ), ( -1, -1 ), 0 , colors.black ),
                ( "GRID" , (0, 0), ( -1, -1 ), 0, colors.black ),
                ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.black ),
                ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "CENTER" ),
                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
            
            ]
        )

        
        # creates a table object and passes the style to it
        table1 = Table( DATA , style = style, colWidths=(1.5*cm, 4.5*cm, 2*cm, 2*cm, 2*cm, 6*cm), rowHeights=(1*cm, 1*cm,))
        table3 = Table( DATA3 , style = style3, colWidths=(6*cm, 6*cm, 6*cm), rowHeights=(1*cm, 1*cm, 1*cm, 1*cm,))
        table4 = Table( DATA4 , style = style4, colWidths=(9*cm, 9*cm), rowHeights=(1*cm))
        table5 = Table( DATA5 , style = style5, colWidths=(6.4*cm, 6.4*cm, 2.9*cm, 2.3*cm), rowHeights=(1*cm, 1*cm, 1*cm, 1*cm))
        table6 = Table( DATA6 , style = style6, colWidths=(18*cm))
        table7 = Table( DATA7 , style = style7, colWidths=(18*cm),  rowHeights=(1*cm, 1*cm))
        table8 = Table( DATA8 , style = style8, colWidths=(1*cm, 2*cm, 2*cm, 5.75*cm, 5.75*cm, 2.5*cm))



        # table = [ title , table3, table1, table2, table4, table5, table6, table7, table8])
        # table.set(Style)
        flow_obj = []
        frame1 = Frame(0,10,600,800)
        frame2 = Frame(0,10,600,800)
        flow_obj.append(title)
        flow_obj.append(table3)
        flow_obj.append(table1)
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

    

    else:

        outward_data = distributor_outward.objects.get(id=distributor_outward_id)
        bike_number_outward_data = distributor_bike_number_outward.objects.filter(outward=outward_data)



        print('in outward')

        bike_detials = distributor_bike_number_outward.objects.get(outward = outward_data)
        variant = bike_detials.bike_number.inward.variant
        hsc = variant.hsn_sac

        p = prices.objects.get(variant = variant)
       
        total_price = p.dealer_price
        address = outward_data.showroom.address
        mobile_no = outward_data.showroom.mobile_number
        taker_name = outward_data.showroom.name
       

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

        
        list_1 = []
        list_2 = []

        list_1.append([ "SR NO" , "Particulars", "Rate", "Qty", "HSN/SAC", "TOTAL" ])


        list_2.append("1")
        list_2.append(bike_detials.bike_number.inward.variant)
        p = prices.objects.get(variant = bike_detials.bike_number.inward.variant)
        list_2.append(p.dealer_price)
        list_2.append("1")
        list_2.append(bike_detials.bike_number.inward.variant.hsn_sac)
        list_2.append(p.dealer_price)
        grand_total = p.dealer_price
        list_1.append(list_2)


        grand_total_price = ((grand_total / 100) * 5) + grand_total

        inword_price = number_to_word(grand_total_price)


        DATA = list_1
        

        DATA3 = [
            [
                "ANITA MOTORS",
                "Invoice no:-3434",
                date_data,
                
                
            ],
            [
                "Rahate complex, Jawahar Nagar,",
                "Consignee",
                "Payment= NEFT/RTGS",
                
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
                grand_total_price,
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


       


        
        
        # creating a Base Document Template of page size A4

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
                
                ( "BOX" , ( 0, 0 ), ( -1, -1 ), 0 , colors.black ),
                ( "GRID" , (0, 0), ( -1, -1 ), 0, colors.black ),
                ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.black ),
                ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "CENTER" ),
                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
            
            ]
        )

        
        # creates a table object and passes the style to it
        table1 = Table( DATA , style = style, colWidths=(1.5*cm, 4.5*cm, 2*cm, 2*cm, 2*cm, 6*cm), rowHeights=(1*cm, 1*cm,))
        table3 = Table( DATA3 , style = style3, colWidths=(6*cm, 6*cm, 6*cm), rowHeights=(1*cm, 1*cm, 1*cm, 1*cm,))
        table4 = Table( DATA4 , style = style4, colWidths=(9*cm, 9*cm), rowHeights=(1*cm))
        table5 = Table( DATA5 , style = style5, colWidths=(6.4*cm, 6.4*cm, 2.9*cm, 2.3*cm), rowHeights=(1*cm, 1*cm, 1*cm, 1*cm))
        table6 = Table( DATA6 , style = style6, colWidths=(18*cm))
        table7 = Table( DATA7 , style = style7, colWidths=(18*cm),  rowHeights=(1*cm, 1*cm))


        # table = [ title , table3, table1, table2, table4, table5, table6, table7, table8])
        # table.set(Style)
        flow_obj = []
        frame1 = Frame(0,10,600,800)
        
        flow_obj.append(title)
        flow_obj.append(table3)
        flow_obj.append(table1)
        flow_obj.append(table4)
        flow_obj.append(table5)
        flow_obj.append(table6)
        flow_obj.append(table7)
        pdf1 = canvas.Canvas(path)
        frame1.addFromList(flow_obj, pdf1)

        # starts page 2

       

        # building pdf
        pdf1.save()
        with open(path, 'rb') as fh:
            mime_type  = mimetypes.guess_type('receipt.pdf')
            response = HttpResponse(fh.read(), content_type=mime_type)
            response['Content-Disposition'] = 'attachment; filename=receipt.pdf'

        return response