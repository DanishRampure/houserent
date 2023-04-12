from django.contrib import admin
from .models import User,Property, Reviews, RentedTable

# Register your models here.
admin.site.register(User)
admin.site.register(Property)
admin.site.register(Reviews)
admin.site.register(RentedTable)
