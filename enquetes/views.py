from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.db.models import F
from django.utils import timezone
# For requesting login: insert here
# "class SomeView(LoginRequiredMixin, generic.Something...):"
#from django.contrib.auth.mixins import LoginRequiredMixin
# https://docs.djangoproject.com/en/1.9/topics/auth/default/
# There are mixins for access controls as well

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'enquetes/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        #Return the last five published questions
        return Question.objects.order_by('-pub_date')[:5]

class AnswerView(generic.DetailView):
    model = Question
    template_name = 'enquetes/answer.html'

    def get_queryset(self):
        #Avoid answering questions in the future
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'enquetes/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, NameError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'enquetes/answer.html', {
            'question': question, 
            'error_message': "You didn't select a choice", 
            })
    else:
        # Using F to avoid race conditions:
        # https://docs.djangoproject.com/en/1.9/ref/models/expressions/#avoiding-race-conditions-using-f
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # If the object needs to be used again, we need to:
        # selected_choice.refresh_from_db()

        #After successful operation with POST, return HttpResposeRedirect
        #This will prevent double-voting
        return HttpResponseRedirect(reverse('enquetes:results', args=(question.id,)))    

"""
# OLD VIEWS
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {
		'latest_question_list' : latest_question_list,
	}
	return render(request, 'enquetes/index.html', context)

def answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'enquetes/answer.html', {'question':question})
    #	return HttpResponse("Voce esta respondendo a questao %s." % question_id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'enquetes/results.html', {'question': question})
"""
