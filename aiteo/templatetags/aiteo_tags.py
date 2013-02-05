from django import template
from django.conf import settings
from django.utils.importlib import import_module


workflow = import_module(getattr(settings, "AITEO_WORKFLOW_MODULE", "aiteo.workflow"))
register = template.Library()


@register.filter
def can_accept(user, response):
    return workflow.can_mark_accepted(user, response.question)


@register.filter
def voted_up(user, obj):
    return obj.votes.filter(user=user, upvote=True).exists()


@register.filter
def voted_down(user, obj):
    return obj.votes.filter(user=user, upvote=False).exists()
