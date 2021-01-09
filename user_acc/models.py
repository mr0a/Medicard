from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class App_User(models.Model):
    first_name = models.CharField(max_length=30, null=True, default='')
    last_name = models.CharField(max_length=30, null=True, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, default='')
    pincode = models.CharField(max_length=10, default='', blank=True)
    country = models.CharField(max_length=30, default='', blank=True)
    aboutme = models.TextField(blank=True, null=True)
    doctor = models.BooleanField(default=False)

    def __str__(self) -> str:
        if self.doctor:
            return str(self.first_name + ' ' + self.last_name)
        return str(self.first_name + ' ' + self.last_name)


class Report(models.Model):
    doctor = models.ForeignKey(App_User, on_delete=models.CASCADE)
    patient = models.ForeignKey(App_User, on_delete=models.CASCADE, related_name='patient')
    report = models.FileField(upload_to='documents/')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)