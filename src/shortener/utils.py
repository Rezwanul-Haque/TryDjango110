import random
import string
from django.conf import settings
# from .models import KirrURL


SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 6)

def code_generator(size = SHORTCODE_MIN, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_shortcode(instance, size = SHORTCODE_MIN):
    new_code = code_generator(size = size)
    Klass = instance.__class__
    queryset_exists = Klass.objects.filter(shortcode = new_code).exists()
    if queryset_exists:
        return create_shortcode(size=size)
    return new_code
