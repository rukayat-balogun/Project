from django import template
from core.models import Purchase

register = template.Library()

@register.filter
def has_bought(user, course):
    return Purchase.objects.filter(user=user, course=course).exists()
