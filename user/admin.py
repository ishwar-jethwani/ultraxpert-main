from django.contrib import admin

from .models import *

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
class UserAccountAdmin(UserAdmin):
    list_display = ["user_id","username","mobile","email","is_verified","is_expert","is_staff","is_superuser","is_active"]
    search_fields = ["email","username"]
    readonly_fields = ["date_joined","last_login"]
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register([Profile,Category,UserPlans,Services,Keywords,BankDetail])
admin.site.register(User,UserAccountAdmin)
