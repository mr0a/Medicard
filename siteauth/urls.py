from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

app_name = 'auth'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('usernamecheck/', views.username_check, name='username_validate'),
    path('activate/<slug:uidb64>/<slug:token>', views.acc_activate, name='activate'),
]