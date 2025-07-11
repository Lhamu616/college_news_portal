from django.shortcuts import render

def home(request):
    return render(request,'home.html')

def dashboard(request):
    return render(request,'dashboard.html')



# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):  # ✅ renamed from 'login' to 'login_view'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')
