"""
URL configuration for workIndia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from railways.views.users import Register, Login, Bookings, Seats
from railways.views.admin import Admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register", csrf_exempt(Register.as_view()), name="register_user"),
    path("login", csrf_exempt(Login.as_view()), name="login_user"),
    path("booking", csrf_exempt(Bookings.as_view()), name="bookings"),
    path("administartion", csrf_exempt(Admin.as_view()), name="admins_panel"),
    path("seats", csrf_exempt(Seats.as_view()), name="seats_available"),
]
