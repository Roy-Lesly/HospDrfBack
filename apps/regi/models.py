from django.db import models
from django.utils.text import slugify

from apps.root.models import CommonPatient, CommonStaff
from datetime import timedelta
import datetime
from apps.account.models import Account

from django.db.models.signals import post_save


# ==================== USER FOR REGIS ========================================================


class RegiUser(models.Model):
    username = models.OneToOneField(Account, unique=True, on_delete=models.CASCADE)

    class Meta:
        pass

    def __str__(self):
        return str(self.username)


def create_regUser(sender, **kwargs):
    if kwargs['created']:
        created_obj = Account.objects.all().order_by('date_joined').last()
        name = created_obj.username
        print("regi: " + name)
        if name == 'Registration' or name == 'zane' or name == 'admin': #or name == 'Laboratory'\
                #or name == 'Consultation' or name == 'Pharmacy' or name == 'Radiology':
            regUser = RegiUser.objects.create(username=created_obj)


post_save.connect(create_regUser, sender=Account)


# =========================================================================
def auto_increment_sn():
    now = datetime.date.today()
    all_patients = Patient.objects.all().filter(date_created__year=now.year,
                                                date_created__month=now.month,).order_by('sn')
    if all_patients.exists():
        lp = all_patients.last()
        if lp.date_created.year == now.year:
            pat_int = int(lp.sn[4:8])
            new_pat_int = int(pat_int) + 1
            new_pat_sn = str(now.year)[2:4] + str(now.month).zfill(2) + str(new_pat_int).zfill(4)
            return new_pat_sn
    else:
        sn = str(now.year)[2:4] + str(now.month).zfill(2) + '0001'
        print("first_num: " + sn)
        return sn
# =========================================================================

def auto_increment_ms():
    now = datetime.date.today()
    # now.month, now.year
    all_purpose = Purpose.objects.all().filter(date_created__year=now.year,
                                               date_created__month=now.month,).order_by("date_created")
    if all_purpose.exists():
        lp = all_purpose.last()
        lp_ms = lp.ms
        lp_date = lp.date_created
        lp_year = lp_date.year
        lp_month = lp_date.month

        if lp_year == now.year:
            if lp_month == now.month:
                new = int(lp_ms) + 1
                ms = str(new).zfill(4)
                return ms
            else:
                ms = '0001'
                return ms
        else:
            ms = '0001'
            return ms
    else:
        ms = '0001'
        return ms


def auto_increment_ds():
    now = datetime.date.today()
    all_purpose = Purpose.objects.all().filter(date_created__year=now.year,
                                               date_created__month=now.month,
                                               date_created__day=now.day).order_by("date_created")
    if all_purpose.exists():
        lp = all_purpose.last()
        if lp.date_created.year == now.year:
            if lp.date_created.month == now.month:
                if lp.date_created.day == now.day:
                    new = int(lp.ds) + 1
                    ds = str(new).zfill(2)
                    return ds
                else:
                    ds = '01'
                    return ds
            else:
                ds = '01'
                return ds
        else:
            ds = '01'
            return ds
    else:
        ds = '01'
        return ds


PURPOSES = (('CONST', 'consultation'), ('RDV', 'rendez-vous'), ('VISIT', 'visit'), ('OTHER', 'other'))


class RegiStaff(CommonStaff):
    title = models.CharField(max_length=15)

    def __str__(self):
        return str(self.first_name.upper()) + " " + str(self.last_name.upper()[0])


class Patient(CommonPatient):
    reg_num = models.CharField(max_length=10, verbose_name='Register No', unique=True)
    sn = models.CharField(primary_key=True, max_length=20, verbose_name='Serial No',
                          default=auto_increment_sn, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.reg_num) + "-" + str(self.first_name)

    def save(self, *args, **kwargs):
        this = datetime.date.today()
        self.first_name = (str(self.first_name)).upper()
        self.last_name = (str(self.last_name)).upper()
        self.full_name = (str(self.first_name) + " " + str(self.last_name)).upper()
        self.address = (str(self.address)).upper()
        
        if not self.slug:
            self.slug = slugify(self.sn + "-" + self.first_name[0:3])
        super(Patient, self).save(*args, **kwargs)


class Purpose(models.Model):
    CONS_FEES_CHOICES = (('0', 'N/C'),
    ('1000', '1000'), ('2000', '2000'), ('3000', '3000'),
    ('5000', '5000'), ('10000', '10000'), ('5500', '5500'),
    ('12000', '12000'), ('15000', '15000'))
    BOOK_FEES_CHOICES = (('0', 'N/C'), ('500', '500'), ('1000', '1000'), ('1500', '1500'))

    purpose = purpose = models.CharField(max_length=30, choices=PURPOSES)
    ds = models.CharField(max_length=20, verbose_name='D-Serial',
                          default=auto_increment_ds, editable=False)
    ms = models.CharField(max_length=20, verbose_name='M-Serial',
                          default=auto_increment_ms, editable=False)
    cons_book = models.CharField(max_length=8, choices=BOOK_FEES_CHOICES)
    fees = models.CharField(max_length=8, choices=CONS_FEES_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    class Meta:
        pass

    def __str__(self):
        return str(self.purpose.upper())

    def save(self, *args, **kwargs):
        self.address = (str(self.purpose)).upper()
        super(Test, self).save(*args, **kwargs)


class Test(models.Model):
    purpose = models.CharField(max_length=30)
    ds = models.CharField(max_length=20, verbose_name='D-Serial',
                          default="auto_increment_ds")
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def __str__(self):
        return self.purpose

