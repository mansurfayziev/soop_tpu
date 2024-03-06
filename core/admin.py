from django.contrib import admin

from .models import RoomNumber, Violation

admin.site.register(RoomNumber)
admin.site.register(Violation)

