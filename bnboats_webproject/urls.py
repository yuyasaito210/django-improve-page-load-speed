"""bnboats_webproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from bnboats_app import urls as app_urls
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(app_urls)),
    path('blog/', include('blog.urls', namespace = 'blog')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('favicon.ico', lambda request: redirect(settings.STATIC_URL + 'media/admin/favicon.png', permanent=False)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'bnboats_app.views.handler404'
handler500 = 'bnboats_app.views.handler500'