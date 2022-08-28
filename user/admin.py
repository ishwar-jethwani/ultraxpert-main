from django.contrib import admin

from .models import *

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
class UserAccountAdmin(UserAdmin):
    list_display = ["id","user_id","username","mobile","email","is_verified","is_expert","is_staff","is_superuser","is_active"]
    search_fields = ["id","email","username","user_id"]
    readonly_fields = ["date_joined","last_login"]
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class ProfileAccountAdmin(admin.ModelAdmin):
    list_display = ["id","profile","first_name","last_name"]
    search_fields = ["id","first_name","last_name"]
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register([Category,UserPlans,Services,Keywords,BankDetail,Comment])
admin.site.register(User,UserAccountAdmin)
admin.site.register(Profile,ProfileAccountAdmin)