from django.template.defaulttags import register


@register.filter(name="get_param_value")
def get_param_value(dictionary, key):
    return dictionary.get(str(key))


@register.filter(name="addstr")
def addstr(arg1, arg2):
    """Kombiniert zwei Strings zu einem."""
    return str(arg1) + str(arg2)


@register.filter(name="times")
def times(n):
    """Gibt eine Liste mit n Einträgen zurück."""
    return range(n)


@register.simple_tag(name="alias")
def alias(obj):
    return obj


@register.filter(name="get_opinion")
def get_opinion(opinions, these):
    """Gibt die Position des Nutzers zu einer These zurück."""
    return opinions[these][0]


@register.filter(name="is_prio")
def is_prio(opinions, these):
    """Gibt zurück, ob der Nutzer eine These priorisiert hat."""
    return opinions[these][1]
