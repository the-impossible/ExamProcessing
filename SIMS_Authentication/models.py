from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, password=None):
        # creates a student with the parameters
        if not email:
            raise ValueError('Email Address required!')
        if password is None:
            raise ValueError('Password is required!')

        user = self.model(email=self.normalize_email(email), firstname=firstname, lastname=lastname, password=password)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, firstname, lastname, password):
        # create a superuser with the above parameters
        if password is None:
            raise ValueError('Password should not be empty')
        if not email:
            raise ValueError('Email Address required!')

        user = self.create_user(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user

class Accounts(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(max_length=30, db_index=True)
    lastname = models.CharField(max_length=30, db_index=True)
    othername = models.CharField(max_length=30, db_index=True, blank=True)
    email = models.EmailField(max_length=50, unique=True, verbose_name='email address', db_index=True,blank=True)
    schNo = models.CharField(max_length=30, unique=True, db_index=True, blank=True)
    picture = models.ImageField(default='user.png', null=True)

    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['firstname', 'lastname']

    objects = AccountManager()

    def get_firstname(self):
        return self.firstname

    def get_lastname(self):
        return self.lastname

    def __str__(self):
        return f'{self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def imageURL(self):
        try:
            url = self.picture.url
        except:
            url = ''
        return url
    class Meta:
        db_table = 'Accounts'
        verbose_name_plural = 'Accounts'