from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse
from django.views import generic
from django.db.models import F
from django.utils import timezone
from django.views.generic import View
from django.db import transaction
from django.forms import ModelForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

# For requesting login: insert mixin in
# "class SomeView(LoginRequiredMixin, generic.Something...):"

from django.contrib.auth.mixins import LoginRequiredMixin #uncomment this to use it

# https://docs.djangoproject.com/en/1.9/topics/auth/default/
# There are mixins for access controls as well

from .models import Question, Choice, UserQuestion, ChoiceQuestion

# Use this ModelForm to create a form based on a model, automatically
# Might be used for teh creation of Enquetes e Opcoes
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'

"""
# Previous wy used to register, was buggy
def register(request):
    if request.method == 'POST':
        uf = UserForm(request.POST, prefix='user')
        if uf.is_valid():
            user = uf.save()
            return HttpResponseRedirect(reverse('enquetes:index'))#this is wrong, we have to pass the url differently
    else:
        uf = UserForm(prefix='user')
    return render_to_response('registration/register.html', 
                                               dict(form=uf,),
                                               context_instance=RequestContext(request))
"""

class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = 'enquetes:login'
    redirect_field_name = 'redirect_to'
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

@login_required()
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
        try:
            # Checks if user alredy answered to Question
            uq = UserQuestion.objects.get(user=request.user, question=question)
        except (KeyError, NameError, UserQuestion.DoesNotExist):
            with transaction.atomic():
                # Create object linking User to Question
                uq = UserQuestion(user=request.user, question=question)
                uq.save()
                with transaction.atomic(savepoint=False):
                    # Create object linking Choice to Question (1 answer)
                    cq = ChoiceQuestion(question=question, choice=selected_choice)
                    cq.save()
        else:
            return render(request, 'enquetes/answer.html', {
            'question': question, 
            'error_message': "You have already answered this question.", 
            })


        ## Using F to avoid race conditions:
        ## https://docs.djangoproject.com/en/1.9/ref/models/expressions/#avoiding-race-conditions-using-f
        #selected_choice.votes = F('votes') + 1
        #selected_choice.save()
        ## If the object needs to be used again, we need to:
        ## selected_choice.refresh_from_db()

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
