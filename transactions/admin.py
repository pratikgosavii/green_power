from django.contrib import admin

# Register your models here.


from .models import *


admin.site.register(inward)
admin.site.register(stock)
admin.site.register(outward)
admin.site.register(bike_number)
admin.site.register(bike_number_outward)