from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from main.models import Consumer, User
from main.models import Seller
from main.models import Bundle_posting
from main.models import IssueReport
from main.models import Forecast_output
from main.models import Reservation

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


admin.site.register(User, UserAdmin)
admin.site.register(Reservation)
admin.site.register(Forecast_output)
admin.site.register(IssueReport)
admin.site.register(Bundle_posting)