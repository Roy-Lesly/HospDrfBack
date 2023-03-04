from django.contrib import admin
from .models import Account, AccountName

class AccountModelAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "role", "account_name_id", "is_admin", "is_staff", "is_active", "is_superuser", "password", )
    search_fields = ("username", "role")
    list_per_page = 50

class AccountNameModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    search_fields = ("id", "name",)
    list_per_page = 30


admin.site.register(Account, AccountModelAdmin)
admin.site.register(AccountName, AccountNameModelAdmin)