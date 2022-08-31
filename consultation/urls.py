"""consultation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .views import ShowAppointments, UpdateAppointment, go_to_gateway_view, callback_gateway_view, Pay, Transactions
from azbankgateways.urls import az_bank_gateways_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts', include('django.contrib.auth.urls')),
    path('show-appointments/<int:id>/', ShowAppointments, name='show-appointments'),
    path('update-appointment', UpdateAppointment, name='update-appointment'),
    path('transactions/<int:id>/', Transactions, name='transactions'),
    path('bankgateways/', az_bank_gateways_urls()),
    path('pay/<int:id>/', Pay, name='pay'),
    path('go_to_gateway/', go_to_gateway_view, name='go_to_gateway'),
    path('callback-gateway/', callback_gateway_view),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
