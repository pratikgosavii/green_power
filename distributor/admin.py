from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(distributor_inward)
admin.site.register(distributor_outward)
admin.site.register(distributor_bike_number_outward)
admin.site.register(distributor_stock)
admin.site.register(distributor_request)
admin.site.register(distributor_payment_details)