from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import User

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("You are now logged in!")
        else:
            return HttpResponse("Invalid credentials.")
    return render(request, 'accounts/login.html')

def authors_and_sellers(request):
    # Filter users who have opted for public visibility
    users = User.objects.filter(public_visibility=True)
    
    return render(request, 'accounts/authors_and_sellers.html', {'users': users})