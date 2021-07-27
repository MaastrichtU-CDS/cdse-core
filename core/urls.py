"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import os

import mozilla_django_oidc
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from authprovider import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index_view"),
    path("api/", include("predictionmodel.urls")),
]


if os.environ.get("DJANGO_SETTINGS_MODULE", "") != "core.settings":
    urlpatterns = urlpatterns + [
        path("oidc/", include("mozilla_django_oidc.urls")),
        path("admin/login/", mozilla_django_oidc.urls.OIDCAuthenticateClass.as_view()),
        path("admin/", admin.site.urls),
    ]
else:
    urlpatterns = urlpatterns + [
        path("admin/", admin.site.urls),
        path("logout", views.LogoutView.as_view(), name="oidc_logout"),
    ]
