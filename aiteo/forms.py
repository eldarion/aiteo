from django import forms

from aiteo.models import Question, Response


class AskQuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ["question", "content"]


class AddResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = ["content"]
