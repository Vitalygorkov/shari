from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Category, Product


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    latest_question_list = ['1']
    template = loader.get_template('shop/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render( context, request))
