from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from voting.models import Vote



class Question(models.Model):
    
    object_id = models.IntegerField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    group = generic.GenericForeignKey()
    
    question = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(User, related_name="questions")
    created = models.DateTimeField(default=datetime.now)
    
    score = models.IntegerField(editable=False, default=0)
    vote_count = models.IntegerField(editable=False, default=0)
    
    def update_score(self):
        result = Vote.objects.get_score(self)
        self.score = result["score"]
        self.vote_count = result["num_votes"]
        self.save()
    
    def get_absolute_url(self, group=None):
        kwargs = {
            "question_id": self.pk,
        }
        if group:
            return group.content_bridge.reverse("questions_question_detail", kwargs=kwargs)
        return reverse("questions_question_detail", kwargs=kwargs)


class Response(models.Model):
    
    question = models.ForeignKey(Question, related_name="responses")
    content = models.TextField()
    accepted = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name="responses")
    created = models.DateTimeField(default=datetime.now)
    
    score = models.IntegerField(editable=False, default=0)
    vote_count = models.IntegerField(editable=False, default=0)
    
    def update_score(self):
        result = Vote.objects.get_score(self)
        self.score = result["score"]
        self.vote_count = result["num_votes"]
        self.save()
    
    def accept(self):
        # check for another active one and mark it inactive
        try:
            response = Response.objects.get(question=self.question, accepted=True)
        except Response.DoesNotExist:
            pass
        else:
            if self != response:
                response.accepted = False
                response.save()
        self.accepted = True
        self.save()
    
    def get_absolute_url(self, group=None):
        return "%s#response-%d" % (self.question.get_absolute_url(group), self.pk)


def vote_save(sender, instance=None, **kwargs):
    if instance:
        # GFK "join" -- issues a query
        obj = instance.object
        if isinstance(obj, (Question, Response)):
            obj.update_score()

post_save.connect(vote_save, sender=Vote)
