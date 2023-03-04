from django.contrib import admin
from .models import Patient, RegiUser, RegiStaff

class PatientModelAdmin(admin.ModelAdmin):
    list_display = ("sn", "first_name", "phone", "dob", "reg_num",)
    search_fields = ("sn", "first_name", "last_name")
    list_per_page = 50



admin.site.register(Patient, PatientModelAdmin)
admin.site.register([RegiUser, RegiStaff])