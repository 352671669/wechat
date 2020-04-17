"""wechat URL Configuration

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
from django.contrib.auth.views import LoginView, LogoutView
from .views import excute, get_business, get_hosts, excute_script, get_scripts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('excute/', excute),
    path('excute/get_business', get_business),
    path('excute/get_hosts', get_hosts),
    path('excute/excute_script', excute_script),
    path('excute/get_scripts', get_scripts),
]
