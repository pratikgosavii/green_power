from email import message
import io
from multiprocessing import context
from statistics import variance
from tkinter.ttk import Style
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse, HttpResponse, JsonResponse
from distributor.models import distributor_inward
from showroom.models import *
from distributor.models import *
from django.db import IntegrityError
from showroom.models import *
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
from django.http import FileResponse, Http404
from itertools import chain

from django.contrib.auth.decorators import user_passes_test


def admin_required(login_url=None):
    return user_passes_test(lambda u: u.is_superuser, login_url=login_url)


#imports for bill generate

from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch,cm,mm
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
        chasis_no = str(chasis_no)

        print('chasis_no')
        print(chasis_no)

        inward_data = bike_number.objects.filter(chasis_no = chasis_no)

        if inward_data:
            print('in inward')

            inward_data_match1 = serializers.serialize('json', inward_data, use_natural_foreign_keys=True)
            print('-----------')
            print(inward_data_match1)
            print('-----------')

            return JsonResponse({'objectt' : inward_data_match1})
        
        else:

            print('not found')

@admin_required(login_url="login")
def add_inward(request):


    if request.method == 'POST':

       
        DC_date = request.POST.get('date')
        chasis_no = request.POST.getlist('chasis_no[]')
        motor_no = request.POST.getlist('motor_no[]')
        controller_no = request.POST.getlist('controller_no[]')
        color = request.POST.getlist('color[]')
        
        bike_qty = len(chasis_no)
        
        print(chasis_no)

        bike_number_data = bike_number.objects.all()

        for i in bike_number_data:

            if i.chasis_no in chasis_no:
                return JsonResponse({'status' : i.chasis_no + ' Chasis Number already exsist'}, safe=False)
            if i.motor_no in motor_no:
                return JsonResponse({'status' : i.motor_no + ' Motor Number already exsist'}, safe=False)
            if i.controller_no in controller_no:
                return JsonResponse({'status' : i.controller_no + ' Controller_no Number already exsist'}, safe=False)

           
        if DC_date:

            date_time = numOfDays(DC_date)
        else:
            date_time = datetime.now(IST)
        
        updated_request = request.POST.copy()
        updated_request.update({'date': date_time, 'bike_qty' : bike_qty})
        forms = inward_Form(updated_request)

        print('come to')

        if forms.is_valid():

            print('in valid')
            instance = forms.save(commit=False)
            instance.created_by = request.user
            instance.save()


            
            for a,b,c,d in zip(chasis_no, motor_no, controller_no, color):

                print('--')

                color_data = Color.objects.get(id = d)

                bike_number.objects.create(inward = instance, chasis_no = a,  motor_no = b, controller_no = c, color = color_data)
                
                try:

                    test = stock.objects.get(variant=instance.variant, color = color_data)

                    test.total_bike = test.total_bike + 1

                    test.save()

                except stock.DoesNotExist:

                    stock.objects.create(variant=instance.variant, color = color_data, total_bike = 1)


            return JsonResponse({'status' : 'done'}, safe=False)

            
        else:

            print('in else')


            error = forms.errors.as_json()
            print(error)
            return JsonResponse({'error' : error}, safe=False)

    else:


        forms = inward_Form()

        color_data = Color.objects.all()

        context = {
            'form': forms,
            'color_data': color_data,
        }
        return render(request, 'transactions/add_inward.html', context)

@admin_required(login_url="login")
def update_inward(request, inward_id ):


    instance = inward.objects.get(id = inward_id)



    data = bike_number.objects.filter(inward = instance)
    print('-----------')
    print(data)
    forms = inward_Form(instance = instance)

    
    context = {
        'form': forms,
        'data' : data,
        'instance' : instance,
    }
    return render(request, 'transactions/update_inward.html', context)

@admin_required(login_url="login")
def delete_inward(request, inward_id):

    try:
        con = inward.objects.get(id = inward_id)

    except inward.DoesNotExist:

        print('something went wrong')
        return redirect('list_inward')

    if con:

        data = bike_number.objects.filter(inward = con)

        for y in data:
            
            try:
                data1 = bike_number_outward.objects.get(bike_number = y)
            except bike_number_outward.DoesNotExist:
                data1 = None
                pass

            if data1:
                if y.chasis_no in data1.bike_number.chasis_no:

                    msg  = "Cant delete Inward, bike is already in outward"

                    data = inward.objects.all()

                    context = {
                        'data': data,
                        'msg' : msg
                    }

                    return render(request, 'transactions/list_inward.html', context)


        try:

            con1 = bike_number.objects.filter(inward = con)

            for z in con1:

                test = stock.objects.get(variant = con.variant, color = z.color)
                test.total_bike = test.total_bike - 1
                test.save()

            con.delete()
            con1.delete()

            return redirect('list_inward')



        except stock.DoesNotExist:

            print('something went wrong2')
            return redirect('list_inward')

@admin_required(login_url="login")
def list_inward(request):

    data = inward.objects.all()

    # inward_filter_data = inward_filter()

    context = {
        'data': data,
        # 'filter_inward' : inward_filter_data
    }

    return render(request, 'transactions/list_inward.html', context)

@admin_required(login_url="login")
def detail_list_inward(request):

    data = bike_number.objects.all()

    context = {
        'data': data,
        # 'filter_inward' : inward_filter_data
    }

    return render(request, 'transactions/detail_list_inward.html', context)

@admin_required(login_url="login")
def detail_list_outward(request):

    data = bike_number_outward.objects.all()

    context = {
        'data': data,
        # 'filter_inward' : inward_filter_data
    }

    return render(request, 'transactions/detail_list_outward.html', context)


@admin_required(login_url="login")
def view_dealer_request(request):

    data1 = showroom_request.objects.filter(distributor = None)


    context = {
        'data1': data1,
        
    }

    return render(request, 'transactions/view_dealer_request.html', context)

@admin_required(login_url="login")
def view_distributor_request(request):

    data = distributor_request.objects.all()

    payment_update = []

    for i in data:
        try:
            a = distributor_payment_details.objects.get(distributor_request = i)
            print('priting a ')
            print(a)
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

    return render(request, 'transactions/view_distributor_request.html', context)


@admin_required(login_url="login")
def detials_distributor_request(request, request_id, msg = None):

    instance = distributor_request.objects.get(id = request_id)
    data = distributor_req.objects.filter(distributor_request = instance)



    context = {
        'data': data,
        'instance': instance,
        'msg': msg,
    }

    return render(request, 'transactions/details_distributor_request.html', context)




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



@admin_required(login_url="login")
def  distributor_view_pr(request, request_id, pathneeded = None):


    request_data = distributor_request.objects.get(id=request_id)
    data = distributor_req.objects.filter(distributor_request = request_data)

    dfsdfs = 1

    if dfsdfs == 1:

        print(data)
        all_price = []

    
        
        for i in data:
            
            variant1 = i.variant
            p = prices.objects.get(variant = variant1)
            all_price.append(p.distributor_price)
            
            address = request_data.distributor.address
            mobile_no = request_data.distributor.mobile_number
            taker_name = request_data.distributor.name
            gst = request_data.distributor.GSTIN_no
            
       


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

            total = int(rate.distributor_price) * int(i.bike_qty)
            


            list_2 = []

            list_2.append(count)
            list_2.append(i.variant)
            list_2.append(rate.distributor_price)
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
                "Payment== NEFT/RTGS"
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




@admin_required(login_url="login")
def distributor_send_pr(request, request_id):


    a = distributor_view_pr(request, request_id, pathneeded = True)
    print('----path---')
    print(a)
    try:
        ins = distributor_request.objects.get(id = request_id)
        ins.pr_pdf = a
        ins.save()
    except distributor_request.DoesNotExist:
        distributor_request.objects.create(distributor_request = instance, pr_pdf = a)

    
    instance = distributor_request.objects.get(id = request_id)
    data = distributor_req.objects.filter(distributor_request = instance)

    msg = "PR send sucessfullly"
    data = distributor_request.objects.all()

    payment_update = []

    for i in data:
        try:
            a = distributor_payment_details.objects.get(distributor_request = i)
            print('priting a ')
            print(a)
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
        'msg': msg,
    }

    return render(request, 'transactions/view_distributor_request.html', context)

    



from distributor.forms import *

@admin_required(login_url="login")
def view_payment_detials(request, payment_id):

    data = distributor_payment_details.objects.get(id = payment_id)

    data = distributor_payment_details_From(instance = data)

    context = {
        'form' : data
    }

    return render(request, 'transactions/view_payment.html', context)




@admin_required(login_url="login")
def add_outward(request):

    if request.method == 'POST':

        chasis_no = request.POST.getlist('chasis_no[]')
        set_chasis_no = set(chasis_no)

        match_data = bike_number.objects.filter(chasis_no__in=chasis_no)
        print(match_data)

        if not len(chasis_no) == len(match_data):

            for i in match_data:
                i2 = i.chasis_no
                set_chasis_no.remove(i2)

            msgg = str(set_chasis_no) + ' not exist in inward'
            return JsonResponse({'status' : msgg}, safe=False)
        

      
        #checking in outward
        match_data_outward = outward.objects.all()
        for i in match_data_outward:
            match_data = bike_number_outward.objects.filter(outward = i, bike_number__chasis_no__in=list(set_chasis_no))
            
            if match_data:

                msgg = str(match_data) + ' already exist in outward'
                return JsonResponse({'status' : msgg}, safe=False)
            
                
        DC_date = request.POST.get('date')

        if DC_date:

            date_time = numOfDays(DC_date)
        else:
            date_time = datetime.now(IST)

        bike_qty = len(chasis_no)

       
        showroom_data = request.POST.get('showroom')
        distributor_data = request.POST.get('distributor')
        print('distributor_data')
        print(distributor_data)

        updated_request = request.POST.copy()
        updated_request.update({'date': date_time, 'bike_qty' : bike_qty, 'showroom' : showroom_data, 'distributor' : distributor_data})
        forms = outward_Form(updated_request)


        if forms.is_valid():

            instance = forms.save(commit=False)
            instance.created_by = request.user
            instance.save()

            print('---------dfdfdf------------')

            for i in chasis_no:

                print('in for')


                bike_data = bike_number.objects.get(chasis_no = i)

                company_stock = stock.objects.get(variant = bike_data.inward.variant, color = bike_data.color)
                company_stock.total_bike = company_stock.total_bike - 1
                company_stock.save()

                chasis_no = list(chasis_no)

            if distributor_data:

                print('-----------')

                user_data = distributor.objects.get(id = distributor_data)
                user_data = user_data.user

                distributor_inward.objects.create(company_outward = forms.instance, user = user_data)


                for i in chasis_no:

                    bike_data = bike_number.objects.get(chasis_no = i)

                    price_data = prices.objects.get(variant = bike_data.inward.variant)

                    print('bike data')
                    print(bike_data)

                   
                    

                   
                    bike_number_outward.objects.create(bike_number = bike_data, outward = instance, price = price_data.distributor_price)
                  

                    try: 
                        test = distributor_stock.objects.get(variant=bike_data.inward.variant, color = bike_data.color, user = user_data)

                        test.total_bike = test.total_bike + 1
                        test.save()

                        print('1')
                    
                    except distributor_stock.DoesNotExist:
                        distributor_stock.objects.create(variant=bike_data.inward.variant, color = bike_data.color, total_bike = 1, user = user_data)


                

                return JsonResponse({'status' : 'done'}, safe=False)

            elif showroom_data:

                print('in showroom')

                user_data = showroom.objects.get(id = showroom_data)
                user_data = user_data.user

                showroom_inward.objects.create(company_outward = forms.instance, user = user_data)
                for i in chasis_no:

                    print('in in for')

                    bike_data = bike_number.objects.get(chasis_no = i)
                    price_data = prices.objects.get(variant = bike_data.inward.variant)

                    print('bike_Data')
                    print(bike_data)


                    bike_number_outward.objects.create(bike_number = bike_data, outward = instance, price = price_data.dealer_price)

                
                    try: 



                        print('in try')
                        test = showroom_stock.objects.get(variant=bike_data.inward.variant, color = bike_data.color, user = user_data)

                        test.total_bike = test.total_bike + 1
                        test.save()

                        print('in try')

                    except showroom_stock.DoesNotExist:
                        print('in except')
                        a = showroom_stock.objects.create(variant=bike_data.inward.variant, color = bike_data.color, total_bike = 1, user = user_data)
                        print('created')
                        print(a)
                        return JsonResponse({'status' : 'done'}, safe=False)

                
                        



                return JsonResponse({'status' : 'done'}, safe=False)
        else:
            
            error = forms.errors.as_json()
            print(error)
            return JsonResponse({'error' : error}, safe=False)

    else:

        forms = outward_Form()

        showroom_data = showroom.objects.filter(Distributor=None, status = "active")

        bike_numbers = bike_number.objects.values_list('chasis_no', flat=True)
        bike_numbers1 = bike_number_outward.objects.values_list('bike_number__chasis_no', flat=True)

        print(bike_numbers)
        print(bike_numbers1)
        bike_numbers = list(bike_numbers)
        bike_numbers1 = list(bike_numbers1)
        print('--------------------------')
        print(bike_numbers)
        print(bike_numbers1)

        bike_numbers_final = bike_numbers.copy()




        for i in bike_numbers:

            print(i)
            print('---')

            

           

            if i in bike_numbers1:

                print(i)

               
                bike_numbers_final.remove(i)

        print('--------------------')
        print(bike_numbers_final)

        
       
        context = {
            'form': forms,
            'showroom_data' : showroom_data,
            'bike_numbers' : bike_numbers_final,
            
        }
        return render(request, 'transactions/add_outward.html', context)


# @login_required(login_url='login')
# def report_dashbord(request):

#     inward_filter_data = inward_filter()
#     outward_filter_data = outward_filter()



#     context = {
#             'filter_inward': inward_filter_data,
#             'filter_outward': outward_filter_data,
#         }

#     return render(request, 'transactions/report_dashbord.html', context)

@admin_required(login_url="login")
def list_outward(request):

    data = outward.objects.all()

    # outward_filter_data = outward_filter()



    context = {
        'data': data,
        # 'filter_outward' : outward_filter_data
    }

    return render(request, 'transactions/list_outward.html', context)
    

@admin_required(login_url="login")
def admin_list_return_distributor(request):

    data = distributor_return.objects.all()

    # outward_filter_data = outward_filter()



    context = {
        'data': data,
        # 'filter_outward' : outward_filter_data
    }

    return render(request, 'transactions/list_return.html', context)
    

@admin_required(login_url="login")
def view_admin_list_return_distributor(request, distributor_return_id):

    instance = distributor_return.objects.get(id = distributor_return_id)

    data = distributor_bike_number_return.objects.filter(distributor_return = instance)

    # outward_filter_data = outward_filter()



    context = {
        'data': data,
        'instance' : instance
        # 'filter_outward' : outward_filter_data
    }

    return render(request, 'transactions/view_distributor_return.html', context)
    

@admin_required(login_url="login")
def admin_list_return_showroom(request):

    data = showroom_bike_number_return.objects.filter(inward__company_outward__isnull = False)

    
    # outward_filter_data = outward_filter()



    context = {
        'data': data,
        # 'filter_outward' : outward_filter_data
    }

    return render(request, 'transactions/list_return_showroom.html', context)



  

@admin_required(login_url='login')
def admin_view_return_showroom(request, return_id):

    instance = showroom_return.objects.get(id = return_id)

    data = showroom_bike_number_return.objects.filter(showroom_return = instance)

    # outward_filter_data = outward_filter()



    context = {
        'data': data,
        'instance' : instance
        # 'filter_outward' : outward_filter_data
    }

    return render(request, 'showroom/view_showroom_return.html', context)
    
  

@admin_required(login_url="login")
def update_outward(request, outward_id):



    instance = outward.objects.get(id = outward_id)


    
    data = bike_number_outward.objects.filter(outward = instance)


    forms = outward_Form(instance = instance)

    showroom_data = showroom.objects.filter(Distributor=None)
    
    if instance.showroom:

        return_data = showroom_bike_number_return.objects.filter(outward_company = instance)

        showroom_id = instance.showroom.id

    else:

        return_data = distributor_bike_number_return.objects.filter(company_outward = instance)

        showroom_id = None

    context = {
        'form': forms,
        'data':data,
        'showroom_data' : showroom_data,
        'showroom_id' : showroom_id,
        'return_data' : return_data,
        'instance' : instance
    }
    return render(request, 'transactions/update_outward.html', context)

@admin_required(login_url="login")
def delete_outward(request, outward_id):

    try:

        con = outward.objects.get(id = outward_id)

    except outward.DoesNotExist:

        print('something went wrong')
        return redirect('list_outward')


    if con:

        data = bike_number_outward.objects.filter(outward = con).values_list('bike_number__chasis_no', flat=True)


        if con.distributor:

            a = distributor_bike_number_outward.objects.filter(bike_number__chasis_no__in = data).values_list('bike_number__chasis_no', flat=True)
            a = list(set(a))
            if a:

                msg  = ', '.join(a) + " Already sold by Distributor"

                data = outward.objects.all()

                context = {
                    'data': data,
                    'msg': msg,
                }

                return render(request, 'transactions/list_outward.html', context)

            
                                    
            b = distributor_bike_number_return.objects.filter(company_outward = con).values_list('bike_number__chasis_no', flat=True)
            print('-----------printing b 1-----------------')
            print(b)
            print(data)
            b = list(set(b))
            if b:

                msg  = ', '.join(b) + " Already Return to you by Distributor"

                data = outward.objects.all()

                context = {
                    'data': data,
                    'msg': msg,
                }

                return render(request, 'transactions/list_outward.html', context)
            
            print('----------h h --------------')
            try:

                con1 = bike_number_outward.objects.filter(outward = con)

                for z in con1:

                    test = stock.objects.get(variant = z.bike_number.inward.variant, color = z.bike_number.color)
                    test1 = distributor_stock.objects.get(variant = z.bike_number.inward.variant, color = z.bike_number.color, user = con.distributor.user)
                    test.total_bike = test.total_bike + 1
                    test.save()
                    test1.total_bike = test1.total_bike - 1
                    test1.save()

                con.delete()
                con1.delete()

                return redirect('list_outward')



            except stock.DoesNotExist:

                print('something went wrong2')
                return redirect('list_outward')

        else:

            
            a = showroom_bike_number_outward.objects.filter(bike_number__chasis_no__in = data).values_list('bike_number__chasis_no', flat=True)
            print('----------------------printing a---------')
            print(a)
            a = list(set(a))
            if a:

                msg  = ', '.join(a) + " Already sold by Showroom"

                data = outward.objects.all()

                context = {
                    'data': data,
                    'msg': msg,
                }

                return render(request, 'transactions/list_outward.html', context)
                                    
            b = showroom_bike_number_return.objects.filter(outward_company = con).values_list('bike_number__chasis_no', flat=True)
            print('-----------printing b-----------------')
            print(b)
            if b:

                b = list(set(b))


                msg  = ', '.join(b) + " Already Return to you by Showroom"

                data = outward.objects.all()

                context = {
                    'data': data,
                    'msg': msg,
                }

                return render(request, 'transactions/list_outward.html', context)

            try:

                con1 = bike_number_outward.objects.filter(outward = con)

                for z in con1:

                    test = stock.objects.get(variant = z.bike_number.inward.variant, color = z.bike_number.color)
                    test1 = showroom_stock.objects.get(variant = z.bike_number.inward.variant, color = z.bike_number.color, user = con.showroom.user)
                    test.total_bike = test.total_bike + 1
                    test.save()
                    test1.total_bike = test1.total_bike - 1
                    test1.save()

                con.delete()
                con1.delete()

                return redirect('list_outward')



            except stock.DoesNotExist:

                print('something went wrong2')
                return redirect('list_outward')









@login_required(login_url="login")
def list_stock(request):

    data = stock.objects.all().order_by('variant')

    # stock_filter_data = stock_filter()



    context = {
        'data': data,
        # 'stock_filter' : stock_filter_data
    }

    return render(request, 'transactions/list_stock.html', context)


@admin_required(login_url="login")
def bill_generate_outward(request, outward_id):


    outward_data = outward.objects.get(id=outward_id)
    print(outward_data)

    if outward_data.bike_qty > 1:

        bike_number_outward_data = bike_number_outward.objects.filter(outward=outward_data)

        print('bike_number_outward_data')
        print(bike_number_outward_data)

        all_price = []


        if outward_data.distributor:

            print('in dis')

            bike_detials_return = distributor_bike_number_return.objects.filter(company_outward = outward_data)

            for i in bike_number_outward_data:
                
                variant1 = i.bike_number.inward.variant
                p = prices.objects.get(variant = variant1)
                all_price.append(p.distributor_price)
                
                total_price = sum(all_price)
               
               
            for i in bike_detials_return:

                variant1 = i.bike_number.inward.variant
                p = prices.objects.get(variant = variant1)
                all_price.append(p.distributor_price)
                
                total_price = sum(all_price)
            address = outward_data.distributor.address
            mobile_no = outward_data.distributor.mobile_number
            taker_name = outward_data.distributor.name
            gst = outward_data.distributor.GSTIN_no
                    
        else:

            print('in show')


            bike_detials_return = showroom_bike_number_return.objects.filter(outward_company = outward_data)
            print('bike_detials_return')
            print(bike_detials_return)
            for i in bike_number_outward_data:


                print('in inward')

                variant1 = i.bike_number.inward.variant
                p = prices.objects.get(variant = variant1)
                all_price.append(p.dealer_price)
                
                total_price = sum(all_price)
                grand_total_price = ((total_price / 100) * 5) + total_price

            address = outward_data.showroom.address
            mobile_no = outward_data.showroom.mobile_number
            taker_name = outward_data.showroom.name
            gst = outward_data.showroom.GSTIN_no




            for i in bike_detials_return:


                print('in inward')

                variant1 = i.bike_number.inward.variant
                p = prices.objects.get(variant = variant1)
                all_price.append(p.dealer_price)
                
                total_price = sum(all_price)
                grand_total_price = ((total_price / 100) * 5) + total_price
              


        print(all_price)
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

        for i in bike_detials_return:


            if i.bike_number.inward.variant in Dict1:

                val = Dict1[i.bike_number.inward.variant]
                print('val')
                print(val)
                Dict1.update({ i.bike_number.inward.variant : (val + 1) })
            else:

                Dict1[i.bike_number.inward.variant] = 1

        
        print('Dict1')
        print(Dict1)

        for key, value in Dict1.items():


            rate = prices.objects.get(variant = key)

            hsc = key.hsn_sac

            total = int(rate.dealer_price) * int(value)
            


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

        DATA8.append(['0', 'Variant', 'Color', 'Chasis No', 'Motor No', 'Controller' '\n' 'No'])

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
        path = os.path.join(BASE_DIR) + '\static\csv\\bill.pdf'
        
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
        table8 = Table( DATA8 , style = style8, colWidths=(1*cm, 2*cm, 2*cm, 5.75*cm, 5.75*cm, 2*cm))


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

        outward_data = outward.objects.get(id=outward_id)
        try:
            bike_detials = bike_number_outward.objects.get(outward = outward_data)
        except:
            bike_detials = distributor_bike_number_return.objects.get(company_outward = outward_data)


        all_price = []

        if outward_data.distributor:


            print('in outward')

            variant1 = bike_detials.bike_number.inward.variant
            hsc = variant.hsn_sac
            p = prices.objects.get(variant = variant1)
            
            total_price = p.distributor_price
            grand_total_price = ((total_price / 100) * 5) + total_price
            inword_price = number_to_word(total_price)
            address = outward_data.distributor.address
            mobile_no = outward_data.distributor.mobile_number
            taker_name = outward_data.distributor.name

        else:

            variant1 = i.bike_number.inward.variant
            hsc = variant.hsn_sac
            p = prices.objects.get(variant = variant1)
            
            total_price = p.dealer_price
            grand_total_price = ((total_price / 100) * 5) + total_price
            address = outward_data.dealer.address
            mobile_no = outward_data.dealer.mobile_number
            taker_name = outward_data.dealer.name

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

        
        path = os.path.join(BASE_DIR) + '\static\csv\\bill.pdf'
        
        
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


        print('-------------------------')
        print('-------------------------')
        print('-------------------------')
        print('-------------------------')
        print('-------------------------')
        print('-------------------------')
        print('-------------------------')
        print('-------------------------')
        
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



from reportlab.lib.pagesizes import letter, landscape








def generate_gstr1(request):


    no_of_records = 0
    total_invoice_amount = 0
    total_taxable_amount = 0
    total_tax_libility = 0
    total_CGST_amount = 0
    total_SGST_amount = 0
    total_IGST_amount = 0
    total_CESS = 0
    
    return_data_no_of_records = 0
    return_data_total_invoice_amount = 0
    return_data_total_taxable_amount = 0
    return_data_total_tax_libility = 0
    return_data_total_CGST_amount = 0
    return_data_total_SGST_amount = 0
    return_data_total_IGST_amount = 0
    return_data_total_CESS = 0



    data = outward.objects.filter(date__range=["2022-06-01", "2022-06-30"])

    no_of_records =  data.count()

    bike_details = bike_number_outward.objects.filter(outward__in = data).values_list('price', flat = True)
   


    total_invoice_amount = sum(bike_details)
        
    print(bike_details)

    total_taxable_amount = total_invoice_amount - ((total_invoice_amount / 100) * 5)

    total_CGST_amount = ((total_invoice_amount / 100) * 5) / 2

    total_SGST_amount = total_CGST_amount

    # calcultions for return bike

    return_data = distributor_return.objects.filter(date__range=["2022-06-01", "2022-06-30"])
    return_data_no_of_records =  return_data.count()
    return_bike_details = distributor_bike_number_return.objects.filter(distributor_return__in = return_data).values_list('price', flat = True)
    print('return_bike_details') 
    print(return_bike_details) 
    return_data_total_invoice_amount = sum(return_bike_details)

    return_data_total_taxable_amount = return_data_total_invoice_amount - ((return_data_total_invoice_amount / 100) * 5)

    return_data_total_CGST_amount = ((return_data_total_invoice_amount / 100) * 5) / 2

    return_data_total_SGST_amount = return_data_total_CGST_amount


        
    

    path = os.path.join(BASE_DIR) + '\media\\' + 'GSTR1_report.pdf'
    
    pdf = SimpleDocTemplate(path)
    
    # standard stylesheet defined within reportlab itself
    pdf.pagesize = landscape(A4)
    styles = getSampleStyleSheet()
    # fetching the style of Top level heading (Heading1)
    title_style = styles[ "Heading1" ]
    
    # 0: left, 1: center, 2: right
    title_style.alignment = 1


    title = Paragraph( "PR" , title_style )
            
    frame1 = Frame(0.5 * inch, 0.5 * inch, 10 * inch, 7.5 * inch,
                    leftPadding=0, rightPadding=0,
                    topPadding=0, bottomPadding=0,)

    flow_obj = []

    flow_obj.append(title)



    style = TableStyle(
        [
            
            ( "BOX" , ( 0, 0 ), ( -1, -1 ), 0 , colors.black ),
            ( "GRID" , (0, 0), (-1, -1 ), 0, colors.black ),
            ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.black ),
            ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "CENTER" ),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTNAME', (0,0), (-1, 0), 'Times-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),


        ]
    )

    style1 = TableStyle(
        [
            
            ( "BOX" , ( 0, 0 ), ( -1, -1 ), 0 , colors.black ),
            ( "GRID" , (0, 0), (-1, -1 ), 0, colors.black ),
            ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.black ),
            ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "CENTER" ),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),


        ]
    )
    
    


    DATA = [[ "Section Name" , "No. of Record", "Total Invoice Amt", "Total Taxable Amt", "Total Tax Liability", "Total CGST Amt", "Total SGST Amt", "Total IGST Amt", "Total CESS" ]]



    DATA3 = [
        [
            "B2B Invoices 4A, 4B, 4C, 6B, 6C.",
            no_of_records,
            total_invoice_amount,
            total_taxable_amount,
            total_tax_libility,
            total_CGST_amount,
            total_SGST_amount, 
            total_IGST_amount,
            total_CESS
            
            
        ],
        [
            "B2C(Large) Invoices 5A, 58",
            no_of_records,
            total_invoice_amount,
            total_taxable_amount,
            total_tax_libility,
            total_CGST_amount,
            total_SGST_amount, 
            total_IGST_amount,
            total_CESS
            
            
        ],
        [
            "B2C(Small) Details 7",
            no_of_records,
            total_invoice_amount,
            total_taxable_amount,
            total_tax_libility,
            total_CGST_amount,
            total_SGST_amount, 
            total_IGST_amount,
            total_CESS
            
            
        ],
        [
            "Credit/Debit Notes(Registered)-98",

            return_data_no_of_records,
            return_data_total_invoice_amount,
            return_data_total_taxable_amount,
            return_data_total_tax_libility,
            return_data_total_CGST_amount,
            return_data_total_SGST_amount, 
            return_data_total_IGST_amount,
            return_data_total_CESS
            
            
        ],
        [
            "Credit/Debit Notes(Unegistered)-98",
            no_of_records,
            total_invoice_amount,
            total_taxable_amount,
            total_tax_libility,
            total_CGST_amount,
            total_SGST_amount, 
            total_IGST_amount,
            total_CESS
            
            
        ],
        [
            "Exports Invoices-6A",
            no_of_records,
            total_invoice_amount,
            total_taxable_amount,
            total_tax_libility,
            total_CGST_amount,
            total_SGST_amount, 
            total_IGST_amount,
            total_CESS
            
            
        ],
        [
            "Tax Liability(Advances Recieved)-11A(1), 11A(2)",
            no_of_records,
            total_invoice_amount,
            total_taxable_amount,
            total_tax_libility,
            total_CGST_amount,
            total_SGST_amount, 
            total_IGST_amount,
            total_CESS
            
            
        ],
        [
            "Adjustment of Advances - 118(1), 118(2)",
            no_of_records,
            total_invoice_amount,
            total_taxable_amount,
            total_tax_libility,
            total_CGST_amount,
            total_SGST_amount, 
            total_IGST_amount,
            total_CESS
            
            
        ],
        [
            "Nil rated, Exempted and Non GST (8)",
            no_of_records,
            total_invoice_amount,
            total_taxable_amount,
            total_tax_libility,
            total_CGST_amount,
            total_SGST_amount, 
            total_IGST_amount,
            total_CESS
            
            
        ],
        [
            "Total Nil Amt.                  :",
            no_of_records,
            total_invoice_amount,
            total_taxable_amount,
            total_tax_libility,
            total_CGST_amount,
            total_SGST_amount, 
            total_IGST_amount,
            total_CESS
            
            
        ],
        [
            "Total Exempted Amt.              :",
            no_of_records,
            total_invoice_amount,
            total_taxable_amount,
            total_tax_libility,
            total_CGST_amount,
            total_SGST_amount, 
            total_IGST_amount,
            total_CESS
            
            
        ],
        [
            "Total Non-GST Amt.                 :",
            no_of_records,
            total_invoice_amount,
            total_taxable_amount,
            total_tax_libility,
            total_CGST_amount,
            total_SGST_amount, 
            total_IGST_amount,
            total_CESS
            
            
        ],
        [
            "HSN-wise Summary of Outward Supplies - 12",
            10000000,
            total_invoice_amount,
            total_taxable_amount,
            total_tax_libility,
            total_CGST_amount,
            total_SGST_amount, 
            total_IGST_amount,
            total_CESS
            
            
        ],
        [
            "Summary of documents issued during the tax period (13)",
            no_of_records,
            total_invoice_amount,
            total_taxable_amount,
            total_tax_libility,
            total_CGST_amount,
            total_SGST_amount, 
            total_IGST_amount,
            total_CESS
            
            
        ],
        [
            "Total Docs",
            no_of_records,
            total_invoice_amount,
            total_taxable_amount,
            total_tax_libility,
            total_CGST_amount,
            total_SGST_amount, 
            total_IGST_amount,
            total_CESS
            
            
        ],
        [
            "Cancelled Docs",
            no_of_records,
            total_invoice_amount,
            total_taxable_amount,
            total_tax_libility,
            total_CGST_amount,
            total_SGST_amount, 
            total_IGST_amount,
            total_CESS
            
            
        ],
        [
            "Net Issued Docs",
            no_of_records,
            total_invoice_amount,
            total_taxable_amount,
            total_tax_libility,
            total_CGST_amount,
            total_SGST_amount, 
            total_IGST_amount,
            total_CESS
            
            
        ],
    ]


    table1 = Table( DATA , style = style, colWidths=(7*cm, 2.3*cm, 2.3*cm, 2.3*cm,2.3*cm,2.3*cm,2.3*cm,2.3*cm,2.3*cm))
    table2 = Table( DATA3 , style = style1, colWidths=(7*cm, 2.3*cm, 2.3*cm, 2.3*cm,2.3*cm,2.3*cm,2.3*cm,2.3*cm,2.3*cm))

    flow_obj.append(table1)
    flow_obj.append(table2)


    pdf1 = canvas.Canvas(path)
    pdf1.setPageSize( landscape(A4) )
    frame1.addFromList(flow_obj, pdf1)

    

    # building pdf
    pdf1.save()