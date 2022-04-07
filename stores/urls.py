from django.urls import path

from .views import *
from stores import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('add-variant/', add_variant, name='add_variant'),
    path('update-variant/<variant_id>', update_variant, name='update_variant'),
    path('delete-variant/<variant_id>', delete_variant, name='delete_variant'),
    path('list-variant/', list_variant, name='list_variant'),

    path('add-bike-color/', add_bike_color, name='add_bike_color'),
    path('update-bike-color/<color_id>', update_bike_color, name='update_bike_color'),
    path('delete-bike-color/<color_id>', delete_bike_color, name='delete_bike_color'),
    path('list-bike-color/', list_bike_color, name='list_bike_color'),

    path('add-showroom/', add_showroom, name='add_showroom'),
    path('update-showroom/<showroom_id>', update_showroom, name='update_showroom'),
    path('delete-showroom/<showroom_id>', delete_showroom, name='delete_showroom'),
    path('list-showroom/', list_showroom, name='list_showroom'),

    path('add-distributor/', add_distributor, name='add_distributor'),
    path('update-distributor/<distributor_id>', update_distributor, name='update_distributor'),
    path('delete-distributor/<distributor_id>', delete_distributor, name='delete_distributor'),
    path('list-distributor/', list_distributor, name='list_distributor'),


    path('add-prices/', add_prices, name='add_prices'),
    path('update-prices/<prices_id>', update_prices, name='update_prices'),
    path('delete-prices/<prices_id>', delete_prices, name='delete_prices'),
    path('list-prices/', list_prices, name='list_prices'),


    # #delete urls 

    # path('list-company-delete/', list_bike_delete, name='list_bike_delete'),
    # path('list-company-goods-delete/', list_company_goods_delete, name='list_company_goods_delete'),
    # path('list-goods-company-delete/', list_goods_company_delete, name='list_goods_company_delete'),
    # path('list-agent-delete/', list_agent_delete, name='list_agent_delete'),






    # 
    # 
    # 
    # 
    # 

]
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)