from django.conf.urls import url
from django.contrib import admin

from shortener.views import homeView, shortenerCBView

urlpatterns = [
    url(r'^new-admin/', admin.site.urls),
    url(r'^$', homeView.as_view()),
    url(r'^(?P<shortcode>[\w-]{6,15})/$', shortenerCBView.as_view()),
]
