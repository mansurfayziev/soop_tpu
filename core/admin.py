from django.contrib import admin

from .models import RoomNumber, Violation, Akt

admin.site.register(RoomNumber)
admin.site.register(Violation)
admin.site.register(Akt)
