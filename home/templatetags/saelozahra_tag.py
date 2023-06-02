from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@mark_safe
def currency(dollars):
    # dollars = round(float(dollars), 2)
    print("dollars>", dollars)

    try:
        dollars = float(dollars)
        return f"<b>{dollars:,}</b> تومان"
    except ValueError:
        return f"<b>{dollars}</b> تومان"


register.filter('currency', currency)
