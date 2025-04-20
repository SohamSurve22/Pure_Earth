from django import template
import json

register = template.Library()

@register.filter
def subtract(value, arg):
    """Subtract the arg from the value."""
    return value - arg

@register.filter
def divide(value, arg):
    """Divide the value by the arg."""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0
        
@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='multiply')
def multiply(value, arg):
    return float(value) * float(arg)

@register.filter
def split(value, arg):
    """Split the value by the arg."""
    return value.split(arg)


@register.filter
def parse_json(value):
    """Parse a JSON string into a Python object."""
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return None

@register.filter
def jsonify(value):
    """Convert a Python object to a JSON string."""
    try:
        return json.dumps(value)
    except (ValueError, TypeError):
        return '""'