from django import template

register = template.Library()

@register.filter(name='human_price')
def human_price(price):
    try:
        price = float(price)/100
        return price
    except:
        return None