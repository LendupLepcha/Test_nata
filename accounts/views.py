from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 


@login_required(login_url="/accounts/login/")
def view_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            messages.warning(request, 'Account created')
            return redirect('accounts:dash')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html' , {'form' : form})

def view_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            #login
            user = form.get_user()
            login(request, user)
            return redirect('accounts:dash')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form' : form})

@login_required(login_url="/accounts/login/")
def view_dash(request):
    return render(request, 'accounts/dash.html')

def view_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')

