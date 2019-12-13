"""projects_man URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.views.decorators.csrf import csrf_exempt
from projects import views

urlpatterns = [
    path('api/createClasses', csrf_exempt(views.create_classes), name='create_classes'),
    path('api/classes', csrf_exempt(views.get_classes), name='classes'),
    path('api/register', csrf_exempt(views.register), name='register'),
    path('api/login', csrf_exempt(views.login), name='login'),
    path('admin/', admin.site.urls),
]
