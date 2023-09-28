from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Theater)
admin.site.register(Seat)
admin.site.register(Booking)
admin.site.register(TimeSlot)
admin.site.register(Payment)