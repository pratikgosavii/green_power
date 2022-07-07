from django.urls import path

from .views import *
from stores import views


from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [


    path('get_outward_data/', get_outward_data, name='get_outward_data'),

    path('add-inward/', add_inward, name='add_inward'),
    path('update-inward/<inward_id>', update_inward, name='update_inward'),
    path('delete-inward/<inward_id>', delete_inward, name='delete_inward'),
    path('list-inward/', list_inward, name='list_inward'),

    path('import-csv', import_code, name='import_code'),

    path('update-bike_number', update_bike_number, name='update_bike_number'),

    
    path('detail-list-inward/', detail_list_inward, name='detail_list_inward'),
    path('detail-list-outward/', detail_list_outward, name='detail_list_outward'),
    path('detail-list-distributor-return/', detail_list_distributor_return, name='detail_list_distributor_return'),
    path('detail-list-dealer-return/', detail_list_dealer_return, name='detail_list_dealer_return'),

    path('add-outward/', add_outward, name='add_outward'),
    path('update-outward/<outward_id>', update_outward, name='update_outward'),
    path('delete-outward/<outward_id>', delete_outward, name='delete_outward'),
    path('list-outward/', list_outward, name='list_outward'),
    
    path('list-return-distributor/', admin_list_return_distributor, name='admin_list_return_distributor'),
    path('view-return-distributor/<distributor_return_id>', view_admin_list_return_distributor, name='view_admin_list_return_distributor'),
    path('list-return-showroom/', admin_list_return_showroom, name='admin_list_return_showroom'),
    path('view-return-showroom/<return_id>', admin_view_return_showroom, name='admin_view_return_showroom'),
    
    
    path('demo', demo, name='demo'),
 

    


    path('list-stock/', list_stock, name='list_stock'),

   
    path('view-dealer-request/', view_dealer_request, name='company_dealer_view_request'),
    path('view-distributor-request/', view_distributor_request, name='company_distributor_view_request'),
    path('details-distributor-request/<request_id>', detials_distributor_request, name='detials_distributor_request'),
    
    path('distributor-view-PR/<request_id>', distributor_view_pr, name='distributor_view_pr'),
    path('distributor-send-PR/<request_id>', distributor_send_pr, name='distributor_send_pr'),
    path('view-payment-detials/<payment_id>', view_payment_detials, name='view_payment_detials'),

    
    path('bill-generate-outward/<outward_id>', bill_generate_outward, name='bill_generate_outward'),




    path('generate-gstr1', generate_gstr1, name='generate_gstr1'),



]
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)