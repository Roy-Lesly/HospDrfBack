from django.db import models

from apps.root.models import CommonStaff, Exam
from apps.regi.models import Patient, RegiStaff
import datetime
from apps.account.models import Account

from django.db.models.signals import post_save, pre_save


# ==================== USER FOR RADIO ========================================================
class RadiUser(models.Model):
    username = models.OneToOneField(Account, unique=True, on_delete=models.CASCADE)

    class Meta:
        pass

    def __str__(self):
        return str(self.username)


def create_radiUser(sender, **kwargs):
    if kwargs['created']:
        created_obj = Account.objects.all().order_by('date_joined').last()
        name = created_obj.username
        print("radi: " + name)
        if name == 'Radiology' or name == 'zane' or name == 'admin':
            radUser = RadiUser.objects.create(username=created_obj)


post_save.connect(create_radiUser, sender=Account)


# =============  Increment US number, US ms, US ds  =======================
def auto_increment_un():
    now = datetime.date.today()
    all_patients = UPatient.objects.all().filter(date_created__year=now.year).order_by('un')
    print(all_patients)
    if all_patients.exists():
        up = all_patients.last()
        if up.date_created.year == now.year:
            pat_int = int(up.un[:5])
            new_pat_int = int(pat_int) + 1
            un = str(new_pat_int).zfill(5) + "-" + str(now.year)[2:4]
            return un
    else:
        un = '00001' + "-" + str(now.year)[2:4]
        return un


def auto_increment_ums():
    now = datetime.date.today()
    all_month = UExam.objects.all().filter(date_created__year=now.year,
                                           date_created__month=now.month, ).order_by("date_created")
    if all_month.exists():
        count = all_month.count()
        new = count + 1
        ms = str(new).zfill(4)
        return ms
    else:
        ms = '0001'
        return ms


def auto_increment_uds():
    now = datetime.date.today()
    all_day = UExam.objects.all().filter(date_created__year=now.year,
                                         date_created__month=now.month,
                                         date_created__day=now.day).order_by("date_created")
    if all_day.exists():
        count = all_day.count()
        new = count + 1
        ds = str(new).zfill(3)
        return ds
    else:
        ds = '001'
        return ds


# -------------------------------------------------------------------------


# ==============  Increment XR number, XR ms, XR ds   =====================

def auto_increment_xn():
    now = datetime.date.today()
    all_patients = XPatient.objects.all().filter(date_created__year=now.year,
                                                 date_created__month=now.month, ).order_by('xn')
    if all_patients.exists():
        xp = all_patients.last()
        if xp.date_created.year == now.year:
            pat_int = int(xp.xn[:5])
            new_pat_int = int(pat_int) + 1
            xn = str(new_pat_int).zfill(5) + "-" + str(now.year)[2:4]
            return xn
    else:
        xn = '00001' + "-" + str(now.year)[2:4]
        return xn


def auto_increment_xms():
    now = datetime.date.today()
    all_month = XExam.objects.all().filter(date_created__year=now.year,
                                           date_created__month=now.month, ).order_by("date_created")
    if all_month.exists():
        count = all_month.count()
        new = count + 1
        ms = str(new).zfill(4)
        return ms
    else:
        ms = '0001'
        return ms


def auto_increment_xds():
    now = datetime.date.today()
    all_day = XExam.objects.all().filter(date_created__year=now.year,
                                         date_created__month=now.month,
                                         date_created__day=now.day).order_by("date_created")
    if all_day.exists():
        count = all_day.count()
        new = count + 1
        ds = str(new).zfill(3)
        return ds
    else:
        ds = '001'
        return ds


# -------------------------------------------------------------------------------------

# ==============  Increment Year number for Ultrasound Exams =====================================

def auto_increment_uys():
    now = datetime.date.today()
    u_exams = UExam.objects.all().filter(date_created__year=now.year, ).order_by('ys')
    if u_exams.exists():
        count = u_exams.count()
        new = count + 1
        uys = str(new).zfill(5) + "-" + str(now.year)[2:4]
        return uys
    else:
        uys = '00001' + "-" + str(now.year)[2:4]
        return uys


# _____________________________________________________________________________________

# ==============  Increment Year number for X-ray Exams ==========================================

def auto_increment_xys():
    now = datetime.date.today()
    x_exams = XExam.objects.all().filter(date_created__year=now.year).order_by('ys')
    if x_exams.exists():
        count = x_exams.count()
        new = count + 1
        xys = str(new).zfill(5) + "-" + str(now.year)[2:4]
        return xys
    else:
        xys = '00001' + "-" + str(now.year)[2:4]
        return xys


# _____________________________________________________________________________________

# PURPOSES = (('CONST', 'consultation'), ('RDV', 'rendez-vous'), ('VISIT', 'visit'), ('OTHER', 'other'))
WARD_CHOICES = (
    ('OPD', 'OPD'),
    ('MAT', 'Maternity'),
    ('LW', 'Labour / Delivery'),
    ('MW', 'Medical Ward'),
    ('SW', 'Surgical Ward'),
    ('CW', "Childrens' Ward"),
    ('OTHER', 'Other')
)
DEPTS = (('Echo', 'Echo'), ('Xray', 'Xray'))
TITLE_CHOICES = (
    ('RAD', 'Radiologist'),
    ('RAD TECHNO', 'Rad. Technologist'),
    ('RAD TECH', 'Rad. Technician'),
    ('As.Tech', 'Assistant Technician'),
    ('ASS', 'Assistant'),
    ('OTHER', "Other")
)
CATEGORY_CHOICES = (
    ('Echo-General', 'Echo-General'),
    ('Echo Special', 'Echo-Special'),
    ('Xray-General', 'Xray-General'),
    ('Xray-Special', 'Xray-Special')
)
SHIFT_CHOICES = (
    ('Morning', 'Morning'),
    ('Afternoon', 'Afternoon'),
    ('Night', 'Night'),
    ('Straight', 'Straight'),
    ('10 to', '10 to'),
    ('Other', 'Other')
)


class RadiDept(models.Model):
    name = models.CharField(max_length=15, unique=True,
                            default='', choices=DEPTS)

    def __str__(self):
        return str(self.name.upper())


class RadiStaff(CommonStaff):
    title = models.CharField(max_length=15, unique=False, default='',
                             choices=TITLE_CHOICES)

    def __str__(self):
        return str(self.first_name.upper()) + " " + str(self.last_name.upper()[0])


def create_radiStaff(sender, **kwargs):
    if kwargs['created']:
        obj = RadiStaff.objects.all().order_by('date_created').last()
        RegiStaff.objects.create(first_name=obj.first_name, last_name=obj.last_name,
                                #  full_name=obj.full_name, 
                                 address=obj.address, age=obj.age,dob=obj.dob,
                                 sex=obj.sex, phone=obj.phone, title=obj.title, code=obj.code)


post_save.connect(create_radiStaff, sender=RadiStaff)


class RadiTestCategory(models.Model):
    category_name = models.CharField(max_length=50, unique=True, choices=CATEGORY_CHOICES)
    department = models.ForeignKey(RadiDept, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.category_name.upper())

    def save(self, *args, **kwargs):
        self.category_name = (str(self.category_name)).upper()
        super(RadiTestCategory, self).save(*args, **kwargs)


class RadiTestType(models.Model):
    type_name = models.CharField(max_length=15, unique=True, default='')
    cost = models.IntegerField(default='')
    category = models.ForeignKey(RadiTestCategory, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.type_name)

    def save(self, *args, **kwargs):
        self.type_name = (str(self.type_name)).upper()
        super(RadiTestType, self).save(*args, **kwargs)


class RadiHanding(models.Model):
    shift = models.CharField(max_length=20, unique=False, choices=SHIFT_CHOICES)
    equipment1 = models.CharField(max_length=20)
    equipment2 = models.CharField(max_length=20)
    equipment3 = models.CharField(max_length=20)
    department = models.ForeignKey(RadiDept, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=100)
    staff = models.ForeignKey(RadiStaff, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.category_name.upper())

    def save(self, *args, **kwargs):
        self.category_name = (str(self.category_name)).upper()
        super(RadiTestCategory, self).save(*args, **kwargs)


# =================== ECHO MODELS =====================

class UPatient(models.Model):
    patient = models.OneToOneField(Patient, default='none', on_delete=models.CASCADE)
    un = models.CharField(max_length=20, verbose_name='US-Number', primary_key=True,
                          default=auto_increment_un, editable=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.patient.first_name.upper())

    def sn(self):
        return self.patient.sn
    sn.short_description = "Serial Number"

    def fn(self):
        return self.patient.full_name
    fn.short_description = "Full Name"

    def sex(self):
        return self.patient.sex
    sex.short_description = "Sex"

    def dob(self):
        self.age = datetime.datetime.today().date() - self.patient.dob
        return round((self.age.days)/365.25)
    dob.short_description = "Age"


class UExam(Exam):
    u_exam = models.ManyToManyField(RadiTestType, through='UExamItem')
    ys = models.CharField(max_length=20, verbose_name='Y-Serial',
                          default=auto_increment_uys, editable=False)
    patient = models.ForeignKey(UPatient, on_delete=models.CASCADE)
    dept = models.ForeignKey(RadiDept, default=1, on_delete=models.CASCADE, editable=False)
    ms = models.CharField(max_length=20, verbose_name='M-Serial',
                          default=auto_increment_ums, editable=False)
    ds = models.CharField(max_length=20, verbose_name='D-Serial',
                          default=auto_increment_uds, editable=False)
    cost = models.IntegerField(default=0, editable=False)
    paid = models.IntegerField(default=0, editable=False)
    # paid = models.IntegerField(default='')
    count = models.CharField(max_length=7, editable=False)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.book_num) + " " + str(self.patient.patient.first_name)

    def un(self):
        return self.patient.un
    un.short_description = "Ultrasound Number"

    def fn(self):
        return self.patient.patient.full_name
    fn.short_description = "Full Name"

    def sex(self):
        return self.patient.patient.sex
    sex.short_description = "Sex"

    def auto_increment_ex_count(self, *args, **kwargs):
        this = UExam.objects.all().filter(patient=self.patient)  # query this patient
        if this.exists():
            count = this.order_by('count').count()
            new = count + 1
            self.count = new
        else:
            self.count = 1

    def save(self, *args, **kwargs):
        now = datetime.date.today()
        if len(self.book_num) < 5:
            book_num = "U" + str(self.book_num).zfill(5) + "_" + str(now.year)[2:4]
            self.book_num = book_num
            self.auto_increment_ex_count()
            super(UExam, self).save(*args, self, **kwargs)
        elif len(self.book_num) == 5:
            self.book_num = "U" + self.book_num + "_" + str(now.year)[2:4]
            super(UExam, self).save(*args, self, **kwargs)
        super(UExam, self).save()    


class UExamItem(models.Model):
    uexam = models.ForeignKey(UExam, related_name="uexams", on_delete=models.CASCADE)
    utype = models.ForeignKey(RadiTestType, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    cost = models.CharField(max_length=6, editable=False, null=False)
    paid = models.CharField(max_length=6, default=0, null=False, blank=False)

    def __str__(self):
        return str(self.uexam) + " " + str(self.utype)

    def un(self):
        return self.uexam.patient.un
    un.short_description = "Ultrasound Number"

    def bn(self):
        return self.uexam.book_num
    bn.short_description = "Book Number"

    def fn(self):
        return self.uexam.patient.patient.full_name
    fn.short_description = "Full Name"

    def sex(self):
        return self.uexam.patient.patient.sex
    sex.short_description = "Sex"

    def dob(self):
        self.age = datetime.datetime.today().date() - self.uexam.patient.patient.dob
        return round((self.age.days)/365.25)
    dob.short_description = "Age"

    def auto_cost(self, *args, **kwargs):
        this = RadiTestType.objects.all().filter(type_name=self.utype)  # query this patient
        if this.exists():
            cost = this[0].cost
            self.cost = cost
        else:
            self.cost = 0

    def save(self, *args, **kwargs):
        self.auto_cost()
        super(UExamItem, self).save(*args, **kwargs)

    class Meta:
        unique_together = [['utype', 'uexam']]


def uexam_update_cost(sender, instance, *args, **kwargs):
    if kwargs['created']:
        this = UExam.objects.get(book_num=instance.uexam.book_num)  # query this Exam
        print(this)
        print(this.cost)
        if this:
            print("exist here 1")
            sum_cost = this.cost + int(instance.cost)
            print("sum_cost: " + str(sum_cost))
            sum_paid = this.paid + int(instance.paid)
            print("sum_paid: " + str(sum_paid))
            try:
                this.cost = sum_cost
                this.save(update_fields=['cost'])
            except:
                print("cannot cost")
            try:
                this.paid = sum_paid
                this.save(update_fields=['paid'])
            except:
                print("cannot paid")

            # this.save()
            print("Exam cost Updated")
        else:
            print("instance not exist")


post_save.connect(uexam_update_cost, sender=UExamItem)


class UFinding(models.Model):
    staff = models.ForeignKey(RadiStaff, on_delete=models.CASCADE)
    u_test = models.ForeignKey(UExamItem, on_delete=models.CASCADE)
    uexam = models.ForeignKey(UExam, on_delete=models.CASCADE)
    findings = models.TextField(max_length=150, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        unique_together = ['u_test', 'uexam']

    def __str__(self):
        return str(self.u_test) + " " + str(self.uexam)

    def un(self):
        return self.uexam.patient.un
    un.short_description = "Ultrasound Number"

    def bn(self):
        return self.uexam.book_num
    bn.short_description = "Book Number"

    def fn(self):
        return self.uexam.patient.patient.full_name
    fn.short_description = "Full Name"

    def sex(self):
        return self.uexam.patient.patient.sex
    sex.short_description = "Sex"

    def dob(self):
        self.age = datetime.datetime.today().date() - self.uexam.patient.patient.dob
        return round((self.age.days)/365.25)
    dob.short_description = "Age"

    def save(self, *args, **kwargs):
        super(UFinding, self).save(*args, **kwargs)


# =================== XRAY MODELS =====================

class XPatient(models.Model):
    patient = models.OneToOneField(Patient, default='none', on_delete=models.CASCADE)
    xn = models.CharField(max_length=20, verbose_name='XR-Number', primary_key=True,
                          default=auto_increment_un, editable=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.patient.first_name.upper())


class XExam(Exam):
    x_exam = models.ManyToManyField(RadiTestType, through='XExamItem')
    ys = models.CharField(max_length=20, verbose_name='Y-Serial',
                          default=auto_increment_xys, editable=False)
    patient = models.ForeignKey(XPatient, on_delete=models.CASCADE)
    dept = models.ForeignKey(RadiDept, default=1, on_delete=models.CASCADE, editable=False)
    ms = models.CharField(max_length=20, verbose_name='M-Serial',
                          default=auto_increment_xms, editable=False)
    ds = models.CharField(max_length=20, verbose_name='D-Serial',
                          default=auto_increment_xds, editable=False)
    cost = models.IntegerField(default=0, editable=False)
    paid = models.IntegerField(default='')
    count = models.CharField(max_length=7, editable=False)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.book_num) + " " + str(self.patient.patient.first_name)

    def auto_increment_ex_count(self, *args, **kwargs):
        this = XExam.objects.all().filter(patient=self.patient)  # query this patient
        if this.exists():
            count = this.order_by('count').count()
            new = count + 1
            self.count = new
        else:
            self.count = 1

    def save(self, *args, **kwargs):
        now = datetime.date.today()
        if len(self.book_num) != 8:
            book_num = str(self.book_num).zfill(5) + "-" + str(now.year)[2:4]
            self.book_num = book_num
            self.auto_increment_ex_count()
            super(XExam, self).save(*args, self, **kwargs)
        super(XExam, self).save(update_fields=['cost'])


class XExamItem(models.Model):
    xexam = models.ForeignKey(XExam, on_delete=models.CASCADE)  # related_name="xexams"
    xtype = models.ForeignKey(RadiTestType, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    cost = models.CharField(max_length=6, editable=False, null=False)
    paid = models.CharField(max_length=6, default=0, null=False, blank=False)

    def __str__(self):
        return str(self.xexam) + " " + str(self.xtype)

    def auto_cost(self, *args, **kwargs):
        this = RadiTestType.objects.all().filter(type_name=self.xtype)  # query this patient
        if this.exists():
            cost = this[0].cost
            self.cost = cost
        else:
            self.cost = 0

    def save(self, *args, **kwargs):
        self.auto_cost()
        super(XExamItem, self).save(*args, **kwargs)

    class Meta:
        unique_together = [['xtype', 'xexam']]


def xexam_update_cost(sender, instance, *args, **kwargs):
    if kwargs['created']:
        this = XExam.objects.get(book_num=instance.uexam.book_num)  # query this Exam
        if this:
            new = this.cost + int(instance.cost)
            this.cost = new
            this.save(update_fields=['cost'])
            print("Exam Updated")
        else:
            print("instance not exist")


post_save.connect(uexam_update_cost, sender=UExamItem)


class XFinding(models.Model):
    staff = models.ForeignKey(RadiStaff, on_delete=models.CASCADE)
    x_test = models.ForeignKey(XExamItem, on_delete=models.CASCADE)
    x_exam = models.ForeignKey(XExam, on_delete=models.CASCADE)
    findings = models.TextField(max_length=150, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        unique_together = ['x_test', 'x_exam']

    def __str__(self):
        return str(self.x_test) + " " + str(self.x_exam)

    def save(self, *args, **kwargs):
        super(XFinding, self).save(*args, **kwargs)