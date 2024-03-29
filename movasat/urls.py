"""movasat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from movasat import settings
urlpatterns = [
    path('madmin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('account.urls')),
    path('course/', include('lms.urls')),
    path('', include('job.urls')),
    path('', include('madadyar.urls')),
    path('', include('challenge.urls')),
    path('', include('harkat.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

admin.site.site_header = ' پنل مدیریت '
admin.site.site_title = ' پنل مدیریت '
admin.site.index_title = 'پنل مدیریت'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
