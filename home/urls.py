from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import ProfileView, LoginView, SignUpView, index

urlpatterns = [
    #Profile
    path('profile', ProfileView.as_view(), name='profile'),

    #Signup and Login
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignUpView.as_view(), name='signup'),

    #Forgot Password
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    #OAuth
    path('accounts/', include('allauth.urls')),

    #Login Required Index
    path('', index, name='index'),
]
