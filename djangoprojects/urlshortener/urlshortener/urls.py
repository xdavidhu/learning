"""urlshortener URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from shortener.views import shortener_redirect_view, shortenerCBView

urlpatterns = [
    url(r'^new-admin/', admin.site.urls),
    url(r'^(?P<shortcode>[\w-]{6,15})/$', shortener_redirect_view),
    url(r'^b/(?P<shortcode>[\w-]{6,15})/$', shortenerCBView.as_view()),
]

SHORTCODE_MAX = 15
SHORTCODE_MIN = 6
