from django.template.defaulttags import register


@register.simple_tag(name='wahlrechner_version')
def wahlrechner_version():
    if not 'w_version' in globals():
        global w_version
        try:
            file = open('version.txt', 'r')
            version = file.read()
            file.close()
        except FileNotFoundError:
            version = 'DEV'

        if version == '':
            w_version = 'DEV'
        else:
            w_version = version

    return w_version
