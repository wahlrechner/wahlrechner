import os

from django.template.defaulttags import register


# noinspection PyGlobalUndefined,PyUnboundLocalVariable
@register.simple_tag(name="wahlrechner_name")
def wahlrechner_name():
    if "w_name" not in globals():
        global w_name
        w_name = os.getenv("WAHLRECHNER_NAME")

    return w_name


# noinspection PyGlobalUndefined,PyUnboundLocalVariable
@register.simple_tag(name="wahlrechner_title")
def wahlrechner_title():
    if "w_title" not in globals():
        global w_title
        w_title = os.getenv("WAHLRECHNER_TITLE", default="Startseite")

    return w_title
