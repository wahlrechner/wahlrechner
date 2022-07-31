from django.template.defaulttags import register


# noinspection PyGlobalUndefined,PyUnboundLocalVariable
@register.simple_tag(name="wahlrechner_version")
def wahlrechner_version():
    if "w_version" not in globals():
        global w_version
        try:
            file = open("version.txt", "r")
            version = file.read()
            file.close()
        except FileNotFoundError:
            version = "DEV"

        if version == "":
            w_version = "DEV"
        else:
            w_version = version

    return w_version
