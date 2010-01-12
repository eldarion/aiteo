from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response

from django.contrib.auth.decorators import login_required

from aiteo.forms import AskQuestionForm, AddResponseForm
from aiteo.models import Question



@login_required # @@@
def question_list(request, group_slug=None, bridge=None):
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404()
    else:
        group = None
    
    questions = Question.objects.all().order_by("-score", "created", "id")
    
    if group:
        questions = group.content_objects(questions)
    
    ctx = {
        "group": group,
        "questions": questions,
    }
    
    return render_to_response("aiteo/question_list.html",
        context_instance = RequestContext(request, ctx)
    )


@login_required
def question_create(request, group_slug=None, bridge=None):
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404()
    else:
        group = None
    
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
        "group": group,
        "form": form,
    }
    
    return render_to_response("aiteo/question_create.html",
        context_instance = RequestContext(request)
    )


@login_required # @@@
def question_detail(request, question_id, group_slug=None, bridge=None):
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404()
    else:
        group = None
    
    questions = Question.objects.all()
    
    if group:
        questions = group.content_objects(questions)
    
    question = get_object_or_404(questions, pk=question_id)
    responses = question.responses.order_by("-score", "created", "id")
    
    if question.user == request.user:
        is_me = True
    else:
        is_me = False
    
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
        "group": group,
        "is_me": is_me,
        "question": question,
        "responses": responses,
        "add_response_form": add_response_form,
    }
    
    return render_to_response("aiteo/question_detail.html",
        context_instance = RequestContext(request)
    )


@login_required
def mark_accepted(request, question_id, response_id, group_slug=None, bridge=None):
    
    if request.method != "POST":
        return HttpResponse("bad")
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404()
    else:
        group = None
    
    questions = Question.objects.all()
    
    if group:
        questions = group.content_objects(questions)
    
    question = get_object_or_404(questions, pk=question_id)
    
    if question.user == request.user:
        is_me = True
    else:
        is_me = False
    
    if is_me:
        response = question.responses.get(pk=response_id)
        response.accept()
    else:
        return HttpResponse("cannot perform action")
    
    return HttpResponse("good")
