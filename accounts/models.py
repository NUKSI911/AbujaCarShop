# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db import models


# Create your models here.
class  UserManager(BaseUserManager):
    def create_user(self,fullname,email,password=None,is_active=False,is_staff=False,is_admin=False):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not fullname:
            raise ValueError("User must have a Full name")
        
        user_obj=self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.staff=is_staff
        user_obj.admin=is_admin
        user_obj.active=is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, fullname,password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            fullname,
            password=password,
            
        )
        user.staff = True,
        user.save(using=self._db)
        return user

    def create_superuser(self, email,fullname, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            fullname,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email=models.EmailField(max_length=254,unique=True)
    fullname=models.CharField(max_length=50 ,default=True,null=True)
    active=models.BooleanField(default=True)
    staff=models.BooleanField(default=False)
    admin=models.BooleanField(default=False)
    timestamp=models.DateTimeField( auto_now_add=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['fullname']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.fullname
    def get_short_name(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True


    def has_module_perms(self,app_label):
        return True


    objects=UserManager()
    @property
    def is_staff(self):
        return self.staff


    @property
    def is_staff(self):
        return self.active
    
    @property
    def is_staff(self):
        return self.admin


    



class GuestEmail(models.Model):
    email=models.EmailField()
    active=models.BooleanField(default=True)
    update=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.email