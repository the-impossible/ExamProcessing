from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from random import choice, shuffle
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

from django.contrib.auth import login, logout
from SIMS_Admin.decorator import is_admin, is_staff

# My app imports
from SIMS_Authentication.models import Accounts
from SIMS_Admin.models import StudentGrades
from SIMS_Authentication.forms import AccountRegistrationForm

# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request,'auth/login.html')

    def post(self, request):
        password = request.POST['password']
        email = request.POST['email']

        if email and password:
            # Authenticate user
            user = authenticate(request, email=email.lower(), password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'You are now signed in {user.schNo}')
                    return redirect('sims_admin:dashboard')
                else:
                    messages.warning(request, 'Account not active contact the administrator')
                    return redirect('auth:login')
            else:
                messages.warning(request, 'Invalid login credentials')
                return redirect('auth:login')
        else:
            messages.error(request, 'All fields are required!!')
            return redirect('auth:login')

class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'You are now signed out!')
        return redirect('sims:home')

class ChangePassword(LoginRequiredMixin, View):
    def post(self, request, user_id):
        try:
            user = Accounts.objects.get(pk=user_id)
            print(user)
        except Accounts.DoesNotExist:
            messages.error(request, 'Oops user does not exist!')
            return redirect('sims_admin:profile', user_id)
        else:
            password = request.POST['password']
            password1 = request.POST['password1']

            if(password1 != password):
                messages.error(request, 'Password don\'t match!')
                return redirect('sims_admin:profile', user_id)

            if(len(password1) < 6):
                messages.error(request, 'Password too short!')
                return redirect('sims_admin:profile', user_id)

            user.set_password(password)
            messages.success(request, 'Password has been changed you can now login with new password below')
            user.save()
        if request.user.is_superuser:
            return redirect('sims_admin:profile', user_id)
        return redirect('sims_auth:login')


def generate_schno(type=None):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    while True:
        schNo_list = [choice(numbers) for _ in range(4)]
        shuffle(list(schNo_list))
        if type == None:
            schNo = 'TSSI'+''.join(schNo_list)
        else:
            schNo = 'TSSA'+''.join(schNo_list)

        if not Accounts.objects.filter(schNo=schNo).exists():
            break
    return schNo

class RegisterView(View):
    def get(self, request):
        context = {
            'form':AccountRegistrationForm()
        }
        return render(request,'auth/register.html', context)

    def post(self, request):
        form = AccountRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if 'student' in request.POST:
                user.schNo = str(generate_schno())
            else:
                user.schNo = str(generate_schno('staff'))
                user.is_staff = True
            user.set_password(user.password)
            user.save()
            if 'student' in request.POST:
                messages.success(request, ('Account creation successful'))
                return redirect('sims_admin:add_student')
            elif 'staff' in request.POST:
                messages.success(request, ('Staff Account creation successful'))
                return redirect('sims_admin:add_staff')
            else:
                messages.success(request, ('Registration Successful you can now login in'))
                return redirect('auth:login')
        else:
            if 'student' in request.POST:
                return render(request, 'admin/add_student.html', {'form':form})
            elif 'staff' in request.POST:
                return render(request, 'admin/add_staff.html', {'form':form})
            else:
                return render(request, 'auth/register.html', {'form':form})