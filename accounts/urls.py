from django.urls import path,include
from accounts import views


urlpatterns = [

    path('', views.user_login, name='user_login'),
    path('register', views.register, name='register'),
    path('authors-and-sellers', views.authors_and_sellers, name='authors_and_sellers'),
]



