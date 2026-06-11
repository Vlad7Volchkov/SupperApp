from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignupForm, RegisterForm
from django.contrib.auth import authenticate, login, logout

def logoutView(request):
    logout(request)
    return redirect('homepage:homepage')

def registerView(request):
    if request.method == 'POST':
        form = RegisterForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage:homepage')
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def signupView(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage:homepage')
    else:
        form = SignupForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)
