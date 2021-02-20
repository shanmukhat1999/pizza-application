from django.contrib import admin

# Register your models here.
from .models import *

class OrderInline(admin.TabularInline):
    model = Order

class User_orderAdmin(admin.ModelAdmin):
    inlines = [
        OrderInline,
    ]

admin.site.register(Item)
admin.site.register(User_order,User_orderAdmin)
admin.site.register(Order)
admin.site.register(UserProfile)
