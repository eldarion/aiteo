from django import template
from django.conf import settings
from django.utils.importlib import import_module


workflow = import_module(getattr(settings, "AITEO_WORKFLOW_MODULE", "aiteo.workflow"))
register = template.Library()


@register.filter
def get_state(original_type, vote_obj):
    """
    Wraps the vote state in a template filter that we can use it within
    the url tag.
    
    for up: {% if vote and vote.is_downvote %}clear{% else %}up{% endif %}
    for down: {% if vote and vote.is_upvote %}clear{% else %}down{% endif %}
    """
    if original_type == "up" and vote_obj and vote_obj.is_downvote():
        return "clear"
    if original_type == "down" and vote_obj and vote_obj.is_upvote():
        return "clear"
    return original_type


@register.filter
def can_accept(user, response):
    return workflow.can_mark_accepted(user, response.question)
