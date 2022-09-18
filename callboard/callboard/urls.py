"""callboard URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from app.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),

    path("register/", register_request, name="register"),
    path("register/email/<int:user_id>", register_email_request, name="register_check_email"),
    path("register/email/<int:user_id>/resend", register_email_request_resend, name="register_check_email_resend"),
]


# Добавляем summernote
urlpatterns += [ path('summernote/', include('django_summernote.urls')) ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('', AnnouncementList.as_view(), name='main_page'),
    path('post/<int:pk>', AnnouncementDetail.as_view(), name='view_post'),
    path('post/<int:pk>/edit', AnnouncementUpdate.as_view(), name='edit_post'),
    path('post/<int:pk>/del', AnnouncementDelete.as_view(), name='del_post'),
    path('post/<int:pk>/add', AnnouncementCreate.as_view(), name='add_post'),

    path('recall/<int:post>', RecallList.as_view(), name='list_recall'),
    path('recall/<int:pk>/edit', RecallUpdate.as_view(), name='edit_recall'),
    path('recall/<int:pk>/del', RecallDelete.as_view(), name='del_recall'),
    path('recall/<int:pk>/add', RecallCreate.as_view(), name='add_post'),
]
