from django.urls import path

# My app imports
from SIMS_Authentication.views import (
    LoginView,
    RegisterView,
    LogoutView,
    ChangePassword,
)

app_name = 'auth'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('register', RegisterView.as_view(), name='register'),
    path('cpass/<int:user_id>/', ChangePassword.as_view(), name='cpass'),
]