from django.contrib.auth.models import User
from . import models
from django.shortcuts import redirect, render
from .forms import ReportUploadForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import EmailMessage


# Create your views here.
def reportIndex(req):
    user = models.App_User.objects.get(user=req.user)
    if user.doctor:
        patient = req.GET.get('patient')
        if patient is not None:
            patient = models.App_User.objects.filter(first_name=patient)
            if len(patient):
                patient = patient[0]
                reports = models.Report.objects.filter(patient=patient)
                print(reports)
            else: reports=[]
            return render(req, 'reports/reportSearch.html', {'reports': reports})
        return render(req, 'reports/reportSearch.html')
    patient = models.App_User.objects.filter(user=req.user)[0]
    reports = models.Report.objects.filter(patient=patient)
    print(reports)
    ctx = {'reports': reports}
    return render(req, 'reports/reports.html', context=ctx)


def doctorReportList(req):
    doctor = models.App_User.objects.filter(user=req.user)[0]
    reports = models.Report.objects.filter(doctor=doctor)
    print(reports)
    ctx = {'reports': reports}
    return render(req, 'reports/reports.html', context=ctx)


class ReportCreateView(CreateView):
    template_name = 'reports/report-create.html'
    form_class = ReportUploadForm
    success_url = reverse_lazy('reports')

    def post(self, request, *args, **kwargs):
        request.POST = request.POST.copy()
        doctor = models.App_User.objects.filter(user=request.user).values()[0]
        patient = models.App_User.objects.filter(id=request.POST['patient']).values()[0]
        patient_user = User.objects.filter(id=patient['user_id']).values()[0]
        print(patient_user)
        request.POST['doctor'] = doctor['id']
        print(request.POST)
        email = EmailMessage("New Report Added", "A new report is added by Dr."+ str(doctor['first_name'])+' '+str(doctor['last_name']), to=[patient_user['email']])
        email.send()
        return super(ReportCreateView, self).post(request, **kwargs)
