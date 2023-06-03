from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def rplc(text, wth="/"):
    text = str(text)
    return text.replace("-", wth)


@mark_safe
def currency(dollars):
    # dollars = round(float(dollars), 2)
    print("dollars>", dollars)

    try:
        dollars = int(dollars)
        return f"<b>{dollars:,}</b> تومان"
    except ValueError:
        return f"<b>{dollars}</b> تومان"


register.filter('currency', currency)
