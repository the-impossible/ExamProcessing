from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# My app imports
from SIMS_Authentication.models import Accounts

class AccountsAdmin(UserAdmin):
    list_display = ('email', 'schNo', 'firstname', 'lastname', 'date_joined', 'last_login', 'is_active', 'is_staff', )
    search_fields = ('email', 'firstname', 'schNo',)
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Register your models here.
admin.site.register(Accounts, AccountsAdmin)