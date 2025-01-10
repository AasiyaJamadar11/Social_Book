from django.urls import path,include

from .views import register
from .views import user_login

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
   
]



