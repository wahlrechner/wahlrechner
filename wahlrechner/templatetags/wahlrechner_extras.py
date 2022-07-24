from django.template.defaulttags import register


@register.filter(name="get_param_value")
def get_param_value(dictionary, key):
    return dictionary.get(str(key))


@register.filter(name="addstr")
def addstr(arg1, arg2):
    return str(arg1) + str(arg2)


@register.filter(name="times")
def times(number):
    return range(number)


@register.simple_tag(name="alias")
def alias(obj):
    return obj
