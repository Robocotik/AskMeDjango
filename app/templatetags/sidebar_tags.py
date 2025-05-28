from django import template
from django.core.cache import cache
from app.models import Tag, User

register = template.Library()

@register.inclusion_tag('sidebar/popular_tags.html')
def popular_tags():
    cache_key = 'popular_tags'
    tags = cache.get(cache_key)
    if tags is None:
        tags = Tag.objects.popular_tags()  
    return {'tags': tags}

@register.inclusion_tag('sidebar/top_users.html')
def top_users():
    cache_key = 'top_users'
    users = cache.get(cache_key)
    if users is None:
        users = User.objects.top_users()  
    return {'users': users}