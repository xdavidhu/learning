from django.db import models
from .utils import code_generator, create_shortcode
from django.conf import settings

# Create your models here.

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)

class shortenerURLManager(models.Manager):
    def all(self, *args, **kwargs):
        qs = super(shortenerURLManager, self).all(*args, **kwargs)
        qs = qs.filter(active=True)
        return qs

    def refresh_shortcodes(self, items=None):
        qs = shortenerURL.objects.filter(id__gte=1)
        if items is not None and isinstance(items, int):
            qs = qs.order_by("-id")[:items]
        new_codes = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            print(q.url + " => " + q.shortcode)
            q.save()
            new_codes += 1
        return "New codes made: " + str(new_codes)


class shortenerURL(models.Model):
    url         = models.CharField(max_length=220)
    shortcode   = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(default=True)

    objects = shortenerURLManager()
    #some_random = shortenerURLManager()

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(self)
        super(shortenerURL, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)
