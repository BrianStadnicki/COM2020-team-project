from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from main.models import Consumer
from main.models import Seller

class ConsumerInline(admin.StackedInline):
    model = Consumer
    can_delete = False
    verbose_name_plural = "consumer"

class SellerInline(admin.StackedInline):
    model = Seller
    can_delete = False
    verbose_name_plural = "seller"

class UserAdmin(BaseUserAdmin):
    inlines = (ConsumerInline, SellerInline)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
