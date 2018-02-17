from django.shortcuts import render, get_object_or_404, Http404
from django.http import HttpResponse, HttpResponseRedirect

from django.views import View

from .models import KirrURL
from analytics.models import ClickEvent
from .forms import SubmitUrlForm


# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForm()
        bg_image = 'https://i0.wp.com/www.joemartinfitness.com/wp-content/uploads/2014/10/beach-beautiful-starfish-on-the-beach_1600x1200_93284.jpg'
        context = {
            "title": "Shortify",
            "form": the_form,
            "bg_image": bg_image
        }
        return render(request, "shortener/home.html", context)

    def post(self, request, *args, **kwargs):
        form = SubmitUrlForm(request.POST)
        context = {
            "title": "Shortify",
            "form": form,
        }

        template = "shortener/home.html"

        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            obj, created = KirrURL.objects.get_or_create(url= new_url)
            bg_image = 'https://i0.wp.com/www.joemartinfitness.com/wp-content/uploads/2014/10/beach-beautiful-starfish-on-the-beach_1600x1200_93284.jpg'
            context = {
                "object": obj,
                "created": created,
                "bg_image": bg_image
            }
            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/already-exists.html"


        return render(request, template, context)

class URLRedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        # obj = get_object_or_404(KirrURL, shortcode = shortcode)
        # return HttpResponse("Class Based Hello {sc}".format(sc=shortcode))
        qs = KirrURL.objects.filter(shortcode__iexact = shortcode)
        if qs.count != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        # save item
        ClickEvent.objects.create_event(obj)
        return HttpResponseRedirect(obj.url)




# def kirr_redirect_view(request, shortcode=None, *args, **kwargs):
#     obj = get_object_or_404(KirrURL, shortcode = shortcode)
#     obj_url = obj.url


    # try:
    #     obj = KirrURL.custom_manager.get(shortcode = shortcode)
    # except Exception as e:
    #     obj = KirrURL.custom_manager.all().first()


    # obj_url = None
    # qs = KirrURL.custom_manager.filter(shortcode__iexact = shortcode)
    # if qs.exists() and qs.count() == 1:
    #     obj = qs.first()
    #     obj_url = obj.url
    #
    # return HttpResponseRedirect(obj.url)
