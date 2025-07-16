from django import template


register = template.Library()


@register.filter(name="add_class")
def add_class(field, css_class):
    existing_classes = field.field.widget.attrs.get("class", "")
    updated_classes = f"{existing_classes} {css_class}".strip()
    field.field.widget.attrs["class"] = updated_classes
    return field


@register.filter(name="add_placeholder")
def add_placeholder(field, placeholder_text):
    field.field.widget.attrs["placeholder"] = placeholder_text
    return field


@register.inclusion_tag("core/partials/field-wrapper.html")
def field_wrapper(field):
    """
    Wraps a form field with an enclosing div and displays errors.
    """
    
    return {"field": field}