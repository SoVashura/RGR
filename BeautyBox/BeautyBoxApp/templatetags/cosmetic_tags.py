from django import template
from BeautyBoxApp.models import Category, Tag
from django.db.models import Count

register = template.Library()

@register.simple_tag
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('cosmetics/list_tags.html')
def show_tags():
    tags = Tag.objects.annotate(total=Count('products')).filter(total__gt=0)
    return {'tags': tags}