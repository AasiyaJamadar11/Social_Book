from django.urls import path,include
from accounts import views
from .views import my_books, upload_books
from .views import send_email_view


urlpatterns = [

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', views.user_login, name='user_login'),
    path('register', views.register, name='register'),
    path('authors-and-sellers', views.authors_and_sellers, name='authors_and_sellers'),
    # urls.py
    path('dashboard', views.dashboard, name='dashboard'),
    path('my-books/', my_books, name='my_books'),
    path('upload-books/', upload_books, name='upload_books'),
    path('uploaded-files/', views.uploaded_files, name='uploaded_files'),
    path('send-email/', send_email_view, name='send_email'),
    

]






