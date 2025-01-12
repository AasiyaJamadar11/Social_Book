from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import CustomUser
from django.views.decorators.csrf import csrf_protect 
from .forms import CreateUserForm

from django.contrib.auth import get_user_model

User = get_user_model()


@csrf_protect
def register(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
    
    context = { 'form':form}
    return render(request,'register.html',context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # return HttpResponse("You are now logged in!")
            return redirect('authors_and_sellers')
        else:
            return HttpResponse("Invalid credentials.")
    return render(request, 'login.html')

def authors_and_sellers(request):
    # Filter users who have opted for public visibility
    users = CustomUser.objects.filter(public_visibility=True)
    
    return render(request, 'authors_and_sellers.html', {'users': users})

