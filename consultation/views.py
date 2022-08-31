from accounts.forms import *
from accounts.models import User
from .models import Appointment
from django.shortcuts import render, redirect
import logging
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
from django.contrib import messages

current_appointment = None

def ShowAppointments(request, id):
    user = User.objects.get(id=id)

    if user.role == 'therapist':
        appointments = Appointment.objects.filter(therapist_email=user.email)
      
        return render(request, 'appointments/show_for_therapist.html', {'appointments' : appointments})
    else:
        appointments = Appointment.objects.filter(patient_email=user.email)
            
        return render(request, 'appointments/show_for_patient.html', {'appointments' : appointments})

def UpdateAppointment(request):

    if request.method == "POST":
        state = request.POST.get('state')
        id = int(str(state).split('$')[-1])
        appointment = Appointment.objects.select_for_update().get(id=id)
        if str(state).__contains__("t-accept"):
            messages.success(request,"با موفقیت تایید شد.")
            appointment.accepted_by_therapist = True
            appointment.save()
        elif str(state).__contains__("t-cancel"):  
            messages.success(request,"قرار ملاقات لغو شد.")
            appointment.canceled_by_therapist = True
            appointment.save()               
        elif  str(state).__contains__("p-cancel"):
            messages.success(request,"با موفقیت لغو شد و درصورت پرداخت هزینه، تا 24 ساعت قبل نصف مبلغ به شما بازخواهد گشت..")
            appointment.canceled_by_patient = True
            appointment.save()   
            
   
    return redirect('home')

def Transactions(request, id):
    user = User.objects.get(id=id)

    if user.role == 'therapist':
        appointments = Appointment.objects.filter(therapist_email=user.email, is_paid=True)
      
        return render(request, 'appointments/transactions.html', {'appointments' : appointments})
    else:
        appointments = Appointment.objects.filter(patient_email=user.email, is_paid=True)
              
        return render(request, 'appointments/transactions.html', {'appointments' : appointments})



def Pay(request, id):
    global current_appointment

    current_appointment = Appointment.objects.filter(id=id).first()
    return render(request, 'appointments/pay.html', {'appointment' : current_appointment})


def go_to_gateway_view(request):
    global current_appointment
   
    amount = int(current_appointment.cost) #10 IRR = 1 Toman
  
    user_mobile_number = '+989112221234'  #Optional

    factory = bankfactories.BankFactory()
    try:
        bank = factory.create()
        bank.set_request(request)
        bank.set_amount(amount)

        bank.set_client_callback_url(('/callback-gateway/'))
        bank.set_mobile_number(user_mobile_number) 
    
        bank_record = bank.ready()
        
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e





def callback_gateway_view(request):
    global current_appointment
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    if bank_record.is_success:
        messages.success(request,"پرداخت با موفقیت انجام شد.")
        current_appointment.is_paid = True
        current_appointment.save()
        return redirect('home')

    messages.success(request, "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")
    return redirect('home')
   