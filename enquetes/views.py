from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from .models import Question

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {
		'latest_question_list' : latest_question_list,
	}
	return render(request, 'enquetes/index.html', context)

# Create your views here.

def answer(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'enquetes/answer.html', {'question':question})
    #	return HttpResponse("Voce esta respondendo a questao %s." % question_id)

def results(request, question_id):
        response = "Voce esta vendo os resultados da questao %s."
        return HttpResponse(response % question_id)

def vote(request, question_id):
        return HttpResponse("Voce esta votando na questao %s." % question_id)
