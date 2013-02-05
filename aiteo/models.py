from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from aiteo.signals import voted, vote_cleared


class TimestampModel(models.Model):
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        return super(TimestampModel, self).save(*args, **kwargs)


class ScoringModel(TimestampModel):
    score = models.IntegerField(editable=False, default=0)
    vote_count = models.IntegerField(editable=False, default=0)
    
    class Meta:
        abstract = True
    
    def vote(self, user, upvote):
        vote, created = self.votes.get_or_create(user=user, defaults={"upvote": upvote})
        if hasattr(vote, "response"):
            vote_obj = vote.response
        else:
            vote_obj = vote.question
        changed = not created and (vote.upvote != upvote)
        if changed:
            vote.delete()
        if changed or created:
            self.update_score()
        if changed:
            vote_cleared.send(sender=vote.__class__, vote_obj=vote_obj, was_upvote=upvote)
        if created:
            voted.send(sender=vote.__class__, vote_obj=vote_obj, upvote=upvote)
    
    def update_score(self):
        votes = self.votes.count()
        upvotes = self.votes.filter(upvote=True).count()
        downvotes = votes - upvotes
        self.score = upvotes - downvotes
        self.vote_count = votes
        self.save()


class Question(ScoringModel):
    
    question = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(User, related_name="questions")
    
    @property
    def accepted_response(self):
        try:
            response = self.responses.get(accepted=True)
        except Response.DoesNotExist:
            response = None
        return response
    
    def get_absolute_url(self):
        return reverse("aiteo_question_detail", args=[self.pk])


class Response(ScoringModel):
    
    question = models.ForeignKey(Question, related_name="responses")
    content = models.TextField()
    accepted = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name="responses")
    
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
    
    def get_absolute_url(self):
        return "%s#response-%d" % (self.question.get_absolute_url(), self.pk)


class QuestionVote(TimestampModel):
    question = models.ForeignKey(Question, related_name="votes")
    upvote = models.BooleanField(default=True)
    user = models.ForeignKey(User, related_name="question_votes")
    
    class Meta:
        unique_together = [("question", "user")]


class ResponseVote(TimestampModel):
    response = models.ForeignKey(Response, related_name="votes")
    upvote = models.BooleanField(default=True)
    user = models.ForeignKey(User, related_name="response_votes")
    
    class Meta:
        unique_together = [("response", "user")]
