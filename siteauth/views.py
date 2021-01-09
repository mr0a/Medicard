from user_acc.models import App_User
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from .forms import SignUpForm
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import login


def signup(request):
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            mail_subject = 'User account activation'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            to_email = form.cleaned_data.get('email')
            print(urlsafe_base64_encode(force_bytes(user.pk)))
            print(account_activation_token.make_token(user))
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.add_message(request, messages.SUCCESS, "Registration Successful, please verify your mail befor login")
            return redirect(reverse_lazy('home'))
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def username_check(request):
    print(request.GET)
    username = request.GET.get('username')
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error'] = 'Username not available'
    return JsonResponse(data)

def acc_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if user.is_active:
            messages.add_message(request, messages.SUCCESS, 'Account has been verified already.')
            return redirect(reverse_lazy('home'))
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        patientuser = User.objects.filter(username=request.user)[0]
        print(patientuser)
        patient = App_User(user=patientuser)
        patient.save()
        messages.add_message(request, messages.SUCCESS, 'Account verified successfully')
        return redirect(reverse_lazy('home'))
    else:
        messages.add_message(request, messages.ERROR, 'Account doesnot exist, Signup again')
