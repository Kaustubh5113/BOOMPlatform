"""
URL configuration for boom_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from videos.views import home 

urlpatterns = [
    path('admin/', admin.site.urls),

    # Include user and video API routes
    path('api/users/', include('users.urls')),
    path('api/videos/', include('videos.urls')),
     path('', home, name='home'),
    
    
    

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
