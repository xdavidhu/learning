from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View

# Create your views here.

from .models import shortenerURL
def shortener_redirect_view(request, shortcode=None, *args, **kwargs):
    # try:
    #     obj = shortenerURL.objects.get(shortcode=shortcode)
    # except:
    #     obj = shortenerURL.objects.all().first()

    obj = get_object_or_404(shortenerURL, shortcode=shortcode)

    # obj_url = None
    # qs = shortenerURL.objects.filter(shortcode__iexact=shortcode.upper())
    # if qs.exists() and qs.count() == 1:
    #     obj = qs.first()
    #     obj_url = obj.url

    return HttpResponse("hello " + str(obj.url))

class shortenerCBView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        obj = get_object_or_404(shortenerURL, shortcode=shortcode)
        return HttpResponse("hello again " + str(obj.url))
