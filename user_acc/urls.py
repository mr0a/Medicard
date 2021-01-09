from django.urls import path
from . import views


urlpatterns = [
    path('', views.reportIndex, name='reports'),
    path('doctor/', views.doctorReportList, name='doctor_reports'),
    path('doctor/create/', views.ReportCreateView.as_view()),
]