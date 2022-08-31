from django.contrib import messages, auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, RedirectView
from accounts.forms import *
from accounts.models import User
from consultation.models import Appointment
from django.shortcuts import get_object_or_404


def patient_sign_up_view(request):
    if request.method == "POST":
        patient  = User()

        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        national_id = request.POST.get('national_id')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            patient.role = "patient"
            patient.email = email
            patient.phone_number = phone_number
            patient.first_name = first_name
            patient.last_name = last_name
            patient.national_id = national_id

            patient.set_password(password1)
            patient.save()
            return redirect('accounts:login')   

    return render(request, 'accounts/patient_signup.html')


def therapist_sign_up_view(request):
    if request.method == "POST":
        therapist  = User()

        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        speciality = request.POST.get('speciality')
        national_id = request.POST.get('national_id')
        medical_education_number = request.POST.get('medical_education_number')
        working_hours =  request.POST.get('working_hours')
        text_visit_cost_per_hour = request.POST.get('text_visit_cost_per_hour')
        video_visit_cost_per_hour = request.POST.get('video_visit_cost_per_hour')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            therapist.role = "therapist"
            therapist.email = email
            therapist.phone_number = phone_number
            therapist.first_name = first_name
            therapist.last_name = last_name
            therapist.speciality = speciality
            therapist.national_id = national_id
            therapist.medical_education_number = medical_education_number
            therapist.working_hours = working_hours
            therapist.text_visit_cost_per_hour = text_visit_cost_per_hour
            therapist.video_visit_cost_per_hour = video_visit_cost_per_hour
        
            therapist.set_password(password1)
            therapist.save()
            return redirect('accounts:login')   

    return render(request, 'accounts/therapist_signup.html')


class login_view(FormView):
    success_url = '/'
    form_class = login_form
    template_name = 'accounts/login.html'
    
    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class logout_view(RedirectView):
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'با موفقیت خارج شدید')
        return redirect('home')
       
    
def show_therapists(request):
    therapists = User.objects.filter(accepted_by_admin=True, role='therapist').order_by('-rate')

    context = {
        'therapists' : therapists
    }
    return render(request, 'accounts/show_therapists.html', context)


def therapist_profile(request, id):
    therapist = User.objects.get(id=id)

    context = {
        'therapist' : therapist
    }
    return render(request, 'accounts/therapist_profile.html', context)


def search_therapist(request):
    if request.method == "POST":
        searched = request.POST['searched']
        found1 = User.objects.filter(accepted_by_admin=True, role='therapist', first_name__contains=searched).order_by('-rate')
        found2 = User.objects.filter(accepted_by_admin=True, role='therapist', last_name__contains=searched).order_by('-rate')
        found3 = User.objects.filter(accepted_by_admin=True, role='therapist', speciality__contains=searched).order_by('-rate')
        found = found1 | found2 |found3

        return render(request, 'accounts/search-therapist.html', { 'searched':searched, 'found': found})
    return render(request, 'accounts/search-therapist.html', {})


def request(request, id):
    therapist = User.objects.get(id=id)

    context = {
        'therapist' : therapist
    }
    return render(request, 'accounts/request.html', context)


def create_appointment(request):
    if request.method == "POST":
        appointment = Appointment()

        problem = request.POST['problem']
        description = request.POST['description']
        skype_id = request.POST['skype_id']
        selected_therapist = request.POST['selected_therapist']
        patient_email = request.POST['email']
        appointment_method = request.POST['appointment_method']
        date = request.POST['date']
        start_time = request.POST['start_time']

        appointment.problem = problem
        appointment.description = description
        appointment.skype_id = skype_id
        appointment.appointment_method = appointment_method
        appointment.date = date
        appointment.start_time = start_time
        appointment.therapist_email = selected_therapist
        appointment.patient_email = patient_email
        therapist = User.objects.filter(email=appointment.therapist_email).first()
        if  appointment.appointment_method == "چت" :
            appointment.cost = therapist.text_visit_cost_per_hour
        else:
            appointment.cost = therapist.video_visit_cost_per_hour
        appointment.therapist_name = therapist.first_name + ' ' + therapist.last_name
        appointment.patient_name = User.objects.filter(email=appointment.patient_email).first().first_name + ' ' +  User.objects.filter(email=appointment.patient_email).first().last_name 
        appointment.save()
        messages.success(request, 'درخواستتان ثبت شد. منتظر تایید مشاور باشید... ')
        return redirect('home')
    else:
        messages.success(request, ' دوباره تلاش کنید ')
        return redirect('home')


def favourite_add(request, id):
  #  patient =  User.objects.select_for_update().get(id=request.user.id)
 #   patient.favourites =  patient.favourites + '$' + str(id)
  #  patient.save()
    
    messages.success(request, 'به علاقه مندی‌ها اضافه شد :)')
    return redirect('home')

"""
def show_favourites(request): 
    therapists = []
    patient =  User.objects.get(id=request.user.id)
    favourites = str(patient.favourites).split('$')
    for f in favourites[1:]:
        id = int(f)
        therapists.append(str('دکتر' + str(User.objects.get(id=id).first_name) + ' ' + str(User.objects.get(id=id).last_name)))
    return render(request, 'accounts/show_therapists.html', {'therapists' : therapists})
"""

