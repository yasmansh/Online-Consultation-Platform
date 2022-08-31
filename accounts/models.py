from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


class user_manager(BaseUserManager): 
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields): 

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    role = models.CharField(max_length=15, error_messages={
        'required': "نقش الزامی است"
    })
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "این ایمیل قبلا استفاده شده است",
                              })
    phone_number = models.CharField(unique=True, blank=True, null=True, max_length=20,
                                    error_messages={
                                        'unique': "این شماره قبلا ثبت شده است"
                                    })

    accepted_by_admin  = models.BooleanField(verbose_name=('تایید شده توسط مدیر'), default=False)
    first_name = models.CharField(verbose_name=('نام'), max_length=50, blank=True, null=True)
    last_name = models.CharField(verbose_name=('نام خانوادگی'), max_length=50, blank=True, null=True)
    national_id =  models.CharField(verbose_name=('کد ملی'), max_length=10, blank=True, null=True)
    speciality = models.CharField(verbose_name=('تخصص'), max_length=100, blank=True, null=True)
    medical_education_number = models.CharField(verbose_name=('شماره نظام پزشکی'), max_length=50, blank=True, null=True)
    working_hours = models.CharField(verbose_name=('ساعات کاری'), max_length=50, blank=True, null=True)
    text_visit_cost_per_hour = models.CharField(verbose_name=('بهای ویزیت متنی در ساعت'), max_length=15, blank=True, null=True, default="")
    video_visit_cost_per_hour = models.CharField(verbose_name=('بهای ویزیت ویدیویی در ساعت'), max_length=15, blank=True, null=True, default="")
    rate = models.IntegerField(verbose_name=('امتیاز'), default=0, blank=True, null=True)
    favourites = models.CharField(verbose_name=('آیدی علاقه‌مندی‌ها'), max_length=150, default='')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.email

    objects = user_manager()


class appointment_manager(BaseUserManager): 
    use_in_migrations = True

    def _create_user(self, problem, password, **extra_fields):
        if not problem:
            raise ValueError('The given problem must be set')
        user = self.model(problem=problem, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields): 

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

