from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.views import View

from .forms import SubmitUrlForm
from .models import shortenerURL

# def shortener_redirect_view(request, shortcode=None, *args, **kwargs):
#     # try:
#     #     obj = shortenerURL.objects.get(shortcode=shortcode)
#     # except:
#     #     obj = shortenerURL.objects.all().first()
#
#     obj = get_object_or_404(shortenerURL, shortcode=shortcode)
#
#     # obj_url = None
#     # qs = shortenerURL.objects.filter(shortcode__iexact=shortcode.upper())
#     # if qs.exists() and qs.count() == 1:
#     #     obj = qs.first()
#     #     obj_url = obj.url
#
#     return HttpResponseRedirect(obj.url)
#
# def home_view_fbv(self, request, *args, **kwargs):
#     if request.method == "POST":
#         pass
#     return render(request, "shortener/home.html")

class homeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForm()
        context = {
            "title": "Kirr.com",
            "form": the_form,
        }
        return render(request, "shortener/home.html", context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        print(request.POST.get("url")) # Returns None by default
        form = SubmitUrlForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

        context = {
            "title": "Kirr.com",
            "form": form,
        }
        return render(request, "shortener/home.html", context)


class shortenerCBView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        obj = get_object_or_404(shortenerURL, shortcode=shortcode)
        return HttpResponseRedirect(obj.url)
