
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),

    # path('', include('User.api.urls')),
    path('specializations', include('Specialization.api.urls')),
    path('account/doctor/', include('Doctor.api.urls')),
    path('account/patient/', include('Patient.api.urls')),
    path('specialization/', include('Specialization.api.urls')),
    path('city/', include('City.api.urls')),
    path('district/', include('District.api.urls')),
    path('appointment/', include('Appointment.api.urls')),
    path('reservation/', include('Reservation.api.urls')),
    path('medical-entry/', include('MedicalEntry.api.urls')),

    path('review/', include('Review.api.urls')),
    path('code/', include('MedicalCode.api.urls')),
    path('payment/', include('Payment.api.urls')),




]
urlpatterns += staticfiles_urlpatterns()
