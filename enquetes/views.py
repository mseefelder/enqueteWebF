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

def answer(request, question_id):
	return HttpResponse("Voce esta respondendo a questao %s." % question_id)

# Create your views here.
