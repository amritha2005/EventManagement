from django.contrib import admin
from EventMaster.models import CategoryDb, EventDb, BookingDb

admin.site.register(CategoryDb)
admin.site.register(EventDb)
admin.site.register(BookingDb)