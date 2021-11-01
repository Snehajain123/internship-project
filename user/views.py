from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import UpdateUserForm, UpdateProfileForm
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'user/register.html',{'form':form})

def User_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_passward = form.cleaned_data['password']
            user = authenticate(username=user_name, password=user_passward)
        if user is not None:
            login(request, user)
            return redirect('users-profile')
        else:
            return render(request,'user/login.html',{'form':form})     
    else:
        form = AuthenticationForm()
        return render(request, 'user/login.html', {'form':form})

def logout_request(request):
    logout(request)
    return redirect("login")

@login_required
def profile(request):
    if request.method == "POST":
        import pdb; pdb.set_trace()
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        else:
            return redirect ("user:users-profile")
    user_form = UpdateUserForm(instance=request.user)
    profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request = request, template_name ="user/profile.html", context = {"user_form": user_form, "profile_form": profile_form })