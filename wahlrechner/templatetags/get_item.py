from django.template.defaulttags import register


@register.filter(name="get_item")
def get_item(dictionary, key):
    return dictionary.get(str(key))


@register.filter(name="get_item_p")
def get_item(dictionary, key):
    return dictionary.get(f"p{str(key)}")
