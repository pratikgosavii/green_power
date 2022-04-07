from django.urls import path

from .views import *
from stores import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [


    path('get_outward_data/', get_outward_data, name='get_distributor_outward_data'),

    path('accept-inward/<inward_id>', accept_inward, name='distributor_accept_inward'),

    path('list-inward/', list_inward, name='distributor_list_inward'),
    path('view-inward/<inward_id>', view_inward, name='distributor_view_inward'),

    path('add-outward/', add_outward, name='distributor_add_outward'),
    path('update-outward/<outward_id>', update_outward, name='distributor_update_outward'),
    path('delete-outward/<outward_id>', delete_outward, name='distributor_delete_outward'),
    path('list-outward/', list_outward, name='distributor_list_outward'),
    
    path('add-request/', add_request, name='distributor_add_request'),
    path('update-request/<request_id>', update_request, name='distributor_update_request'),
    path('list-request', list_request, name='distributor_list_request'),
    path('details-request/<request_id>', details_request, name='distributor_details_request'),
    path('delete-request/<request_id>', delete_request, name='distributor_delete_request'),
    path('download-pr/<request_id>', download_pr, name='distributor_download'),
    path('distributor-send-payment-detials-pr/<request_id>', distributor_send_payment_detials, name='distributor_send_payment_detials'),
    path('distributor-update-payment-detialsr/<payment_id>', distributor_update_payment_detials, name='distributor_update_payment_detials'),
    
    path('view-request/', view_request, name='distributor_view_request'),

    path('detail-list-inward/', detail_list_inward, name='distributor_detail_list_inward'),
    path('detail-list-outward/', detail_list_outward, name='distributor_detail_list_outward'),

    path('list-stock/', list_stock, name='distributor_list_stock'),
    

    path('bill-generate-distributor-outward/<distributor_outward_id>', bill_generate_distributor_outward, name='bill_generate_distributor_outward'),



]
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)