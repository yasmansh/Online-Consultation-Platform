from django.db import models
from django.utils.translation import gettext as _


class Appointment(models.Model):
    problem = models.CharField(_('مشکل'), max_length=50)
    description = models.CharField(_('توضیح'), max_length=300)
    skype_id = models.CharField(_('شناسه اسکایپ بیمار'), max_length=100)
    therapist_email  = models.EmailField(_('ایمیل مشاور'))
    patient_email = models.EmailField(_('ایمیل بیمار'))
    therapist_name  = models.CharField(_('نام مشاور'), max_length=100, null=True)
    patient_name = models.CharField(_('نام بیمار'), max_length=100, null=True)
    appointment_method = models.CharField(_('روش مشاوره'), max_length=400)
    date = models.CharField(_('تاریخ '), max_length=100)
    start_time = models.CharField(_(' زمان شروع'), max_length=100)
    accepted_by_therapist = models.BooleanField(_('تایید شده توسط مشاور'), default=False)
    canceled_by_therapist = models.BooleanField(_('لغو توسط مشاور'), default=False)
    canceled_by_patient = models.BooleanField(_('لغو توسط بیمار'), default=False)
    is_paid = models.BooleanField(_('هزینه پرداخت شده '), default=False)
    tc = models.CharField(_('کد تراکنش '), max_length=16, null=True, blank=True)
    cost = models.CharField(_('هزینه به ریال '), max_length=10, null=True)
     

    def __str__(self):
        return self.patient_email + ' ' + self.therapist_email
