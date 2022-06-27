from django.urls import path

from .views import *
from stores import views


from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    path('get_outward_data/', get_outward_data, name='get_showroom_outward_data'),
    
    path('accept-inward/<inward_id>', accept_inward, name='showroom_accept_inward'),

    path('add-customer/', add_customer, name='add_customer'),
    path('update-customer/<customer_id>', update_customer, name='update_customer'),
    # path('delete-customer/<customer_id>', delete_customer, name='delete_customer'),
    path('list-customer/', list_customer, name='list_customer'),
    
    path('list-inward/', list_inward, name='showroom_list_inward'),
    path('view-inward/<inward_id>', view_inward, name='showroom_view_inward'),

    path('detail-list-inward/', detail_list_inward, name='showroom_detail_list_inward'),
    path('detail-list-outward/', detail_list_outward, name='showroom_detail_list_outward'),

    path('add-outward/', add_outward, name='showroom_add_outward'),
    path('update-outward/<outward_id>', update_outward, name='showroom_update_outward'),
    path('delete-outward/<outward_id>', delete_outward, name='showroom_delete_outward'),
    path('list-outward/', list_outward, name='showroom_list_outward'),

    
    path('add-return/', add_return, name='showroom_add_return'),
    path('list-return/', list_return, name='showroom_list_return'),
    path('view-return/', view_return, name='view_showroom_list_return'),

    path('add-request/', add_request, name='showroom_add_request'),
    path('update-request/<request_id>', update_request, name='showroom_update_request'),
    path('details-request/<request_id>', details_request, name='showroom_details_request'),
    path('delete-request/<request_id>', delete_request, name='showroom_delete_request'),
    path('list-request/', list_request, name='showroom_list_request'),
    path('download-pr/<request_id>', download_pr, name='showroom_download'),
    path('showroom-send-payment-detials-pr/<request_id>', showroom_send_payment_detials, name='showroom_send_payment_detials'),
    path('showroom-update-payment-detialsr/<payment_id>', showroom_update_payment_detials, name='showroom_update_payment_detials'),



    path('list-stock/', list_stock, name='showroom_list_stock'),

    path('bill-generate-distributor-outward/<showroom_outward_id>', bill_generate_showroom_outward, name='bill_generate_showroom_outward'),


]
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)