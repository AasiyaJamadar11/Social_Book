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
from djoser.views import UserViewSet
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import certifi

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
        title = request.POST.get('title')
        description = request.POST.get('description')
        visibility = request.POST.get('visibility')
        file = request.FILES.get('file')  # Retrieve the uploaded file
        
        # Correctly pass the user instance to the UploadedFile object
        uploaded_file = UploadedFile.objects.create(
            title=title,
            file=file,
            user=user,  # Pass the user instance here
            description= description,
            visibility=True if visibility == "public" else False,
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
    

# accounts/views.py

class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Create a response
            response = JsonResponse({"message": "Login successful!"})

            # Set cookies
            response.set_cookie(
                "access_token",
                access_token,
                httponly=True,
                secure=True,
                samesite="Strict",  # Adjust to your frontend setup
            )
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                secure=True,
                samesite="Strict",
            )
            return response

        return JsonResponse({"error": "Invalid credentials"}, status=400)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthenticationFromCookie(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get("access_token")
        if not access_token:
            return None

        try:
            token = AccessToken(access_token)
            user_id = token["user_id"]
            user = User.objects.get(id=user_id)
            return (user, None)
        except Exception:
            return None


# accounts/views.py

class ProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # You can access the authenticated user via request.user
        return Response({"message": "This is a protected view!", "user": str(request.user)})
    

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims here
        token['username'] = user.username
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

# You can create a custom view for refreshing the token if needed, or use the default provided by simplejwt
class TokenRefreshViewCustom(TokenRefreshView):
    pass


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UploadedFile
from accounts.serializers import UploadedFileSerializer

class UserFilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Fetch files uploaded by the authenticated user
        user_files = UploadedFile.objects.filter(user=user)
        serializer = UploadedFileSerializer(user_files, many=True)
        return Response(serializer.data)

from django.shortcuts import redirect
from functools import wraps
from .models import UploadedFile

def check_user_uploads(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:  # Ensure the user is logged in
            return redirect('user_login')

        # Check if the user has uploaded any files
        if not UploadedFile.objects.filter(user=user).exists():
            return redirect('upload_books')  # Redirect if no files uploaded

        return view_func(request, *args, **kwargs)

    return wrapper

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
@check_user_uploads
def my_books(request):
    user = request.user
    # Fetch user-uploaded files
    user_files = UploadedFile.objects.filter(user=user)
    return render(request, 'my_books.html', {'files': user_files})

@login_required
def upload_books(request):
    if request.method == 'POST':
        book_title = request.POST.get('book_title')
        book_description = request.POST.get('book_description')
        book_file = request.FILES.get('book_file')

        # Save the uploaded file
        UploadedFile.objects.create(
            title=book_title,
            description=book_description,
            file=book_file,
            user=request.user,
            visibility=True,  # Or implement your visibility logic
        )

        return redirect('my_books')  # Redirect to "My Books" after upload

    return render(request, 'upload_books.html')

from django.core.mail import send_mail
from django.http import HttpResponse

def send_email_view(request):
    subject = "Welcome to Django Email System"
    message = "This is a test email sent from Django."
    from_email = 'aasiyajamadar2@gmail.com'  # Replace with your email
    recipient_list = ['aasiyajamadar5@gmail.com']  # Replace with the recipient's email

    try:
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse("Email sent successfully!")
    except Exception as e:
        return HttpResponse(f"Failed to send email: {e}")

