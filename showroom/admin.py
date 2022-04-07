from django.contrib import admin

# Register your models here.


from .models import *


admin.site.register(showroom_inward)
admin.site.register(showroom_outward)
admin.site.register(showroom_bike_number_outward)
admin.site.register(showroom_stock)
admin.site.register(showroom_request)
admin.site.register(customer)