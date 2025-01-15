"""
URL configuration for social_book project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from djoser import views as djoser_views
from accounts.views import CustomUserViewSet 
from accounts.views import CustomUserViewSet, login_view, ProtectedView
from rest_framework_simplejwt.views import TokenRefreshView 
from accounts.views import CustomTokenObtainPairView
from accounts.views import UserFilesView



router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
   
    
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
     path('auth/', include(router.urls)),  # Djoser endpoints
     path('protected/', ProtectedView.as_view(), name='protected'),  # Protected API view
     path('api/login/', login_view, name='login'),
     path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh
     path('api/user-files/', UserFilesView.as_view(), name='user_files'),
    
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





