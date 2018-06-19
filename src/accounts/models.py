from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

class UserManager(BaseUserManager):
    def create_user(self, email,name, password=None, is_staff=False, is_admin=False, is_active=True):
        if not email:
            raise ValueError("User must have a email address")
        if not password:
            raise ValueError("Password required")
        if not name:
            raise ValueError("Username required")
        user = self.model(
            email=self.normalize_email(email),
            name=name

        )
        user.staff = is_staff
        user.admin = is_admin
        user.staff = is_staff
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, name, password=None):
        user = self.create_user(email,name,password=password,is_staff=True)
        return user


    def create_superuser(self, email, name, password=None):
        user = self.create_user(email,name,password=password,is_staff=True,is_admin=True)
        return user









class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=255,blank=True,null=True,default="user")
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True





class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



