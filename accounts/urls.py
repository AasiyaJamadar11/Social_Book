from django.urls import path,include

from .views import register
from .views import user_login
from . import views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('authors-and-sellers/', views.authors_and_sellers, name='authors_and_sellers'),
   
]



