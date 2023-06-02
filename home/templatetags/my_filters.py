from django import template
register = template.Library()


def currency(dollars):
    # dollars = round(float(dollars), 2)
    return f"{dollars:,} تومان"


register.filter('currency', currency)
