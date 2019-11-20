from django import template
from outstation.apps.core.models import LocationTag, TripType
import json
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()

@register.filter()
def parseInt(value):
    return int(value)

@register.filter(name="item")
def item(l, i):
    i = int('0' + i)
    try:
        return l[i]
    except:
        return None

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def mod(number, modBy):
    return number % modBy

@register.filter
def formattime(duration):
    seconds = duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    formatedDuration =''
    if minutes == 0:
        formatedDuration = str(hours) + " hr"
    elif hours == 0:
        formatedDuration = str(minutes) + " minutes"
    else :
        formatedDuration = str(hours) + " hr " + str(minutes) + " minutes"

    return formatedDuration

@register.filter
def static_url(file):
    url = static(file)
    return url

@register.filter
def dicValue(dic, key):
    value=""
    k = str(key)
    if k in dic:
        value = dic[k]
        print(value)
    return value

@register.filter
def dic(value, key):
    dict={}
    dict[str(key)] = value
    return dict

@register.filter
def JSON(list):
    items = {}
    json_script_escapes = {
    ord('>'): '\\u003E',
    ord('<'): '\\u003C',
    ord('&'): '\\u0026',
}
    for item in list:
        if isinstance(item, LocationTag):
            items[str(item.id)] = item.tag
        if isinstance(item, TripType):
            items[str(item.id)] = item.trip_type
    from django.core.serializers.json import DjangoJSONEncoder
    json_str = json.dumps(items, cls=DjangoJSONEncoder).translate(json_script_escapes)
    return json_str

@register.filter
def classname(obj):
    return obj.__class__.__name__
