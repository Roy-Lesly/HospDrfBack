from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

user = None


def current_user(request):
    global user
    user = get_user_model()


class MyAccountManager(BaseUserManager):
    def create_user(self, username, password, role, account_name_id):
        if not username:
            raise ValueError("Must Enter Username")

        user = self.model(username=username, role=role, account_name_id=account_name_id,)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, username, password, role, account_name_id):
        acc_name_id = AccountName.objects.filter(id=account_name_id).first()
        user = self.create_user(
            account_name_id=acc_name_id,
            username=username,
            password=password,
            role=role)

        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        if user.is_staff is not True:
            raise ValueError("SuperUser has to have is_staff to true")
        if user.is_superuser is not True:
            raise ValueError("SuperUser has to have is_superuser to true")
            
        user.save(using=self._db)
        return user


DEPT_CHOICES = (('Registration', 'Registration'),
                ('Radiology', 'Radiology'),
                ('Pharmacy', 'Pharmacy'),
                ('Laboratory', 'Laboratory'),
                ('Ophthalmology', 'Ophthalmology'),
                ('Maternity', 'Maternity'),
                ('Ward', 'Ward'),
                ('Orthopedic', 'Orthopedic'),
                ('admin', "Admin"),
                ('zane', "Zane"),
                ('Technical', "Technical"),
                ('Finance', "Finance"),
                ('Other', 'Other'))

ROLE_CHOICES = (('admin', 'admin'),
                ('hod', "hod"),
                ('dept', "dept"),
                ('staff', "staff"),
                ('visitor', "visitor"),
                ('other', 'other'))

class AccountName(models.Model):
    name = models.CharField(max_length=20, unique=True, blank=False, null=False)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Account(AbstractBaseUser, PermissionsMixin):
    # username = models.CharField(verbose_name='username', choices=DEPT_CHOICES, max_length=15, unique=True, blank=False,null=False)
    username = models.CharField(verbose_name='username', max_length=15, unique=True, blank=False,null=False)
    account_name_id = models.ForeignKey(AccountName, unique=False, on_delete=models.CASCADE)
    role= models.CharField(verbose_name='role', choices=ROLE_CHOICES, max_length=15, unique=False)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    # photo = models.ImageField(upload_to='profiles')
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, editable=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role', 'account_name_id']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perms(self, perm_list, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
