from django.conf import settings
from django.db import models
from .utils import code_generator, create_shortcode
from .validators import validate_url, validate_dot_com
# from django.core.urlresolvers import reverse
from django_hosts.resolvers import reverse

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)


class KirrURLManager(models.Manager):
    """Django data model NAME"""
    def all(self, *args, **kwargs):
        qs_main = super(KirrURLManager, self).all(*args, **kwargs)
        qs = qs_main.filter(active=True)
        return qs

    def refresh_shortcodes(self, items=None):
        print(items)
        qs = KirrURL.objects.filter(id__gte = 1)
        if items is not None and isinstance(items, int):
            qs = qs.order_by('-id')[:items]

        new_codes = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            print(q.shortcode)
            q.save()
            new_codes += 1
        return "New codes made: {i}".format(i=new_codes)

    class Meta:
        verbose_name = 'NAME'
        verbose_name_plural = 'NAMEs'

    def __str__(self):
        return str(self.id)

# Create your models here.
class KirrURL(models.Model):
    """Django data model KirrURL"""
    url = models.CharField(max_length=250, validators = [validate_url, validate_dot_com])
    shortcode = models.CharField(max_length = SHORTCODE_MAX, unique = True, blank=True)
    updated = models.DateTimeField(auto_now = True) #everyTime the model is saved
    timestamp = models.DateTimeField(auto_now_add = True) # when model was created
    active = models.BooleanField(default=True)

    objects = models.Manager();
    custom_manager = KirrURLManager();

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(self)
        if not "http" in self.url:
            self.url = "http://" + self.url
        super(KirrURL, self).save(*args, **kwargs)

    def get_short_url(self):
        url_path = reverse("scode", kwargs = {"shortcode" : self.shortcode}, host= "www", scheme = 'http', port = "8000")
        return url_path

    class Meta:
        verbose_name = 'KirrURL'
        verbose_name_plural = 'KirrURLs'

    def __str__(self):
        return str(self.url)
