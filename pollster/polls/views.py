from django.shortcuts import render

from .models import Question, Choice
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse


# Get questions and display them
def index(req):
    latest_questions_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_questions_list}
    return render(req, "polls/index.html", context)


# show specific question and choices
def detail(req, q_id):
    try:
        q = Question.objects.get(pk=q_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(req, "polls/detail.html", {"question": q})


# get question and display results
def results(req, q_id):
    q = get_object_or_404(Question, pk=q_id)
    return render(req, "polls/results.html", {"question": q})


# Vote for a question choice
def vote(req, q_id):
    # print(request.POST['choice'])
    question = get_object_or_404(Question, pk=q_id)
    try:
        selected_choice = question.choice_set.get(pk=req.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            req,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(q_id,)))
