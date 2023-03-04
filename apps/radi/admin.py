from django.contrib import admin
from .models import *
from apps.regi.models import Patient

# Register your models here.
admin.site.register([RadiUser, RadiDept, RadiTestType,  RadiTestCategory,])
admin.site.register([XPatient, XExam, XFinding, XExamItem])


@admin.register(UPatient)
class UPatientAdmin(admin.ModelAdmin):
    list_display = ("un", "sn", "fn", "sex", "dob", "date_created",)
    list_filter = ("un", "date_created")
    search_fields = ("un__startswith",)

@admin.register(RadiStaff)
class UPatientAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "sex", "dob", "age", "date_created",)
    # list_filter = ("first_name", "full_name", "date_created")
    search_fields = ("first_name", "full_name",)


@admin.register(UExam)
class UExamAdmin(admin.ModelAdmin):
    list_display = ("book_num", "un", "fn", "sex", "date_created")
    list_filter = ("book_num", "date_created")
    search_fields = ("book_num__startswith",)


@admin.register(UExamItem)
class UExamItemAdmin(admin.ModelAdmin):
    list_display = ("id", "bn", "un", "fn", "sex", "dob", "utype", "paid", "date_created")
    list_filter = ("id", "date_created")
    search_fields = ("id",)


@admin.register(UFinding)
class UFindingAdmin(admin.ModelAdmin):
    list_display = ("id", "bn", "un", "fn", "sex", "dob", "date_created")
    list_filter = ("id", "date_created")
    search_fields = ("id",)