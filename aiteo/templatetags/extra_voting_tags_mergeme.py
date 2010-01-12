from django import template

register = template.Library()


@register.filter
def get_state(original_type, vote_obj):
    # FIXME: there is a better name for it
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