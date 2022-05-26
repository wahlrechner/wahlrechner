import os

from django.template.defaulttags import register


@register.simple_tag(name="wahlrechner_name")
def wahlrechner_name():
    if not "w_name" in globals():
        global w_name
        w_name = os.environ["WAHLRECHNER_NAME"]

    return w_name
