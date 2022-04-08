import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transactions.models import *
from distributor.models import *
from showroom.models import *


from stores.models import *


@login_required(login_url='login')
def dashboard(request):

    if request.user.is_superuser: 

        request_ = []
        stock_ = []
        inward_ = []
        outward_ = []

        stock_count = stock.objects.all()
        inward_data = inward.objects.all()
        outward_data = outward.objects.all()
        request_data1 = distributor_req.objects.all()
        request_data2 = showroom_request.objects.filter(distributor = None)

        for i in stock_count:
            stock_.append(i.total_bike)

        for i in outward_data:
            outward_.append(i.bike_qty)

        for i in request_data1:
            request_.append(i.bike_qty)

        for i in request_data2:
            request_.append(i.bike_qty)

        for i in inward_data:
            inward_.append(i.bike_qty)

        
        request_ = sum(request_)
        stock_ = sum(stock_)
        inward_ = sum(inward_)
        outward_ = sum(outward_)

    elif request.user.is_distributor:

        print('----------------------------data-----------------------')


        request_ = []
        stock_ = []
        inward_ = []
        outward_ = []

        stock_count = distributor_stock.objects.filter(user = request.user)
        inward_data = distributor_inward.objects.filter(user = request.user)
        outward_data = distributor_outward.objects.filter(user = request.user)
        distributor_data = distributor.objects.get(user = request.user)
        request_data1 = distributor_request.objects.filter(distributor = distributor_data)

        for i in stock_count:
            stock_.append(i.total_bike)

        for i in outward_data:
            outward_.append(i.bike_qty)
        for y in request_data1:

            z = distributor_req.objects.filter(distributor_request = y)

            for i in z:
                request_.append(i.bike_qty)


        for i in inward_data:
            inward_.append(i.company_outward.bike_qty)

        
        request_ = sum(request_)
        inward_ = sum(inward_)
        stock_ = sum(stock_)
        outward_ = sum(outward_)

    else:

        print('----------------------------data1-----------------------')

        request_ = []
        stock_ = []
        inward_ = []
        outward_ = []

        stock_count = showroom_stock.objects.filter(user = request.user)
        inward_data = showroom_inward.objects.filter(user = request.user)
        outward_data = showroom_outward.objects.filter(user = request.user)
        
        showroom_da = showroom.objects.get(user = request.user)
        request_data1 = showroom_request.objects.filter(showroom = showroom_da)


        for i in stock_count:
            stock_.append(i.total_bike)

        for i in outward_data:
            outward_.append(i.bike_qty)

        for y in request_data1:

            z = showroom_req.objects.filter(showroom_request = y)

            for i in z:
                request_.append(i.bike_qty)


        for i in inward_data:

            if i.distributor_outward != None:
                inward_.append(i.distributor_outward.bike_qty)
            else:
                inward_.append(i.company_outward.bike_qty)

        request_ = sum(request_)
        inward_ = sum(inward_)
        stock_ = sum(stock_)
        outward_ = sum(outward_)


    context = {
        
        'stock_count' : stock_,
        'outward_data' : outward_,
        'inward_' : inward_,
        'request_co' : request_,
        
    }

    return render(request, 'dashboard.html', context)