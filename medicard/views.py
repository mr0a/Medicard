from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.forms import Form
from django.shortcuts import redirect, render
from user_acc import models
from django.views import View
from django.utils.decorators import method_decorator
from user_acc.forms import PatientProfile
from django.views.generic import UpdateView


def indexView(request):
    return render(request, 'index/index.html')


@method_decorator(login_required, name='dispatch')
class ProfileView(UpdateView):
    def get(self, request):
        form = PatientProfile()
        user = models.App_User.objects.filter(user=request.user).values()[0]
        if len(user):
            ctx = {'user_data': user, 'form': form}
            return render(request, 'index/profile.html', context=ctx)
        ctx = {'form': form}
        return render(request, 'index/profile.html', context=ctx)

    def post(self, request):
        user = User.objects.filter(id=request.user.id)[0]
        data = dict(request.POST)
        for k,v in data.items():
            data[k] = v[0]
        # user.delete()
        # form = PatientProfile(request.POST)
        # if form.is_valid():
        #     form.save()
        data['user'] = user
        models.App_User.objects.update_or_create(user=user, defaults=data)
        return redirect('/profile/')

