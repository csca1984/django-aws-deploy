from .models import MenuItem
from django.utils import timezone


def menu_items(request):
    """Provide visible menu items and current time to all templates.

    Returns:
        dict: { 'menu_items': QuerySet(MenuItem), 'now': datetime }
    """
    items = MenuItem.objects.filter(visible=True).order_by('order')
    return {
        'menu_items': items,
        'now': timezone.now(),
    }
