import django.dispatch


voted = django.dispatch.Signal(providing_args=["vote_obj", "upvote"])
vote_cleared = django.dispatch.Signal(providing_args=["vote_obj", "was_upvote"])
