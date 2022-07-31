import os

from django.template.defaulttags import register


@register.simple_tag(name="wahlrechner_name")
def wahlrechner_name():
    return os.getenv("WAHLRECHNER_NAME", default="Wahlrechner")


@register.simple_tag(name="wahlrechner_title")
def wahlrechner_title():
    return os.getenv("WAHLRECHNER_TITLE", default="Startseite")
