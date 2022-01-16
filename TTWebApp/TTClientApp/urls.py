from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('statistics/', views.statistics_view, name='statistics'),
    #For Password Reset
    path('accounts/password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/passReset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="auth/passReset/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/passReset/password_reset_complete.html'), name='password_reset_complete'),
]