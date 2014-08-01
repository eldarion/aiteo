import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.importlib import import_module
from django.views.decorators.http import require_POST

from account.decorators import login_required
from aiteo.forms import AskQuestionForm, AddResponseForm
from aiteo.models import Question, Response


workflow = import_module(getattr(settings, "AITEO_WORKFLOW_MODULE", "aiteo.workflow"))


def question_list(request):
    questions = Question.objects.all().order_by("-score", "created", "id")
    ctx = {
        "questions": questions,
    }
    return render(request, "aiteo/question_list.html", ctx)


@login_required
def question_create(request):
    if request.method == "POST":
        form = AskQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        form = AskQuestionForm()
    ctx = {
        "form": form,
    }
    return render(request, "aiteo/question_create.html", ctx)


def question_detail(request, pk):
    questions = Question.objects.all()
    question = get_object_or_404(questions, pk=pk)
    responses = question.responses.order_by("-score", "created", "id")
    is_me = question.user == request.user
    if request.method == "POST":
        add_response_form = AddResponseForm(request.POST)
        if add_response_form.is_valid():
            response = add_response_form.save(commit=False)
            response.question = question
            response.user = request.user
            response.save()
            return HttpResponseRedirect(response.get_absolute_url())
    else:
        if not is_me or request.user.is_staff:
            add_response_form = AddResponseForm()
        else:
            add_response_form = None
    ctx = {
        "can_mark_accepted": workflow.can_mark_accepted(request.user, question),
        "question": question,
        "responses": responses,
        "add_response_form": add_response_form,
    }
    return render(request, "aiteo/question_detail.html", ctx)


@login_required
@require_POST
def mark_accepted(request, pk):
    response = get_object_or_404(Response, pk=pk)
    if not workflow.can_mark_accepted(request.user, response.question):
        return HttpResponseForbidden("You are not allowed to mark this question accepted.")

    response.accept()

    data = {"fragments": {}}
    for resp in response.question.responses.all():
        data["fragments"]["#accepted-{}".format(resp.pk)] = render_to_string(
            "aiteo/_accepted.html",
            {"response": resp},
            context_instance=RequestContext(request)
        )
    return HttpResponse(json.dumps(data), mimetype="application/json")


@login_required
@require_POST
def question_upvote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.vote(user=request.user, upvote=True)
    data = {
        "html": render_to_string("aiteo/_question_vote_badge.html", {
            "question": question
        }, context_instance=RequestContext(request))
    }
    return HttpResponse(json.dumps(data), mimetype="application/json")


@login_required
@require_POST
def question_downvote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.vote(user=request.user, upvote=False)
    data = {
        "html": render_to_string("aiteo/_question_vote_badge.html", {
            "question": question
        }, context_instance=RequestContext(request))
    }
    return HttpResponse(json.dumps(data), mimetype="application/json")


@login_required
@require_POST
def response_upvote(request, pk):
    response = get_object_or_404(Response, pk=pk)
    response.vote(user=request.user, upvote=True)
    data = {
        "html": render_to_string("aiteo/_response_vote_badge.html", {
            "response": response
        }, context_instance=RequestContext(request))
    }
    return HttpResponse(json.dumps(data), mimetype="application/json")


@login_required
@require_POST
def response_downvote(request, pk):
    response = get_object_or_404(Response, pk=pk)
    response.vote(user=request.user, upvote=False)
    data = {
        "html": render_to_string("aiteo/_response_vote_badge.html", {
            "response": response
        }, context_instance=RequestContext(request))
    }
    return HttpResponse(json.dumps(data), mimetype="application/json")
