from django.urls import path
from .views import *
from . import views

app_name = "accounts"

urlpatterns = [
    path('patient/signup', patient_sign_up_view, name='patient-signup'),
    path('therapist/signup', therapist_sign_up_view, name='therapist-signup'),
    path('login', login_view.as_view(), name='login'),
    path('logout', logout_view.as_view(), name='logout'),
    path('show_therapists', views.show_therapists, name='show-therapists'),
    path('show_therapists/<int:id>/', views.therapist_profile, name='therapist-profile'),
    path('search_therapist', views.search_therapist, name='search-therapist'),
 #   path('favourites', views.show_favourites, name='show-favourites'),
    path('request/<int:id>/', views.request, name='request'),
    path('appointment', views.create_appointment, name='appointment'),
    path('fav/<int:id>/', views.favourite_add, name='favourite'),
]