from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from account.decorators import ad_required
from account.forms import LoginForm
from .forms import CreateUserForm, ChangePwForm


def errorView(request):
    raise Http404


@ad_required
def CreateUser(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/listdevices/')
    return render(request, 'account/createuser.html', {'form': form})


@login_required
def ChangePassword(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        currentpw = request.POST['current_password']
        newpw = request.POST['new_password']
        newpwcf = request.POST['new_password_confirmation']
        user = User.objects.get(username=uname)
        if user.password == currentpw and newpw == newpwcf:
            User.objects.get(username=uname).set_password(newpw)
        return HttpResponseRedirect('/accounts/logout/')
    return render(request, 'account/ChangePassword.html')
