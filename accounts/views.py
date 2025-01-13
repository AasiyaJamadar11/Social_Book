from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import CustomUser
from django.views.decorators.csrf import csrf_protect 
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from accounts.models import UploadedFile
from .forms import FileUploadForm
from django.contrib.auth import get_user_model
from django.contrib import messages
import logging

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
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('user_login')
    return render(request, 'login.html')

def authors_and_sellers(request):
    # Filter users who have opted for public visibility
    users = CustomUser.objects.filter(public_visibility=True)
    
    return render(request, 'authors_and_sellers.html', {'users': users})

# views.py


@login_required
def dashboard(request):
    user = request.user  # This is the logged-in user
    
    if request.method == "POST":
        # Retrieve form data
        book_title = request.POST.get('book_title')
        book_description = request.POST.get('book_description')
        book_visibility = request.POST.get('book_visibility')
        book_file = request.FILES.get('book_file')  # Retrieve the uploaded file
        
        # Correctly pass the user instance to the UploadedFile object
        uploaded_file = UploadedFile.objects.create(
            title=book_title,
            file=book_file,
            user=user,  # Pass the user instance here
            description=book_description,
            visibility=True if book_visibility == "public" else False,
            cost=0.00,  # Example cost
            year_published=2025  # You can dynamically set this if needed
        )
        
        return redirect('dashboard')  # Redirect back to dashboard after upload

    return render(request, 'dashboard.html', {'user': user})


@login_required
def uploaded_files(request):
    files = UploadedFile.objects.filter(
    user=request.user, visibility='private'
) | UploadedFile.objects.filter(visibility='public')
    return render(request, 'uploaded_files.html', {'files': files})
    