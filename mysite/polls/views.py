from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.db.models import Count
from django.db import transaction

from .models import Choice, Question, Company
from .forms import CreateForm, CHOICE_FORM_SET
import json


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        '''
        Return the last five published questions.
        (not including future questions)
        '''
        return Question.objects.annotate(
            choice_count=Count('choice')).filter(
                choice_count__gt=0,
                pub_date__lte=timezone.now()
                ).order_by('-pub_date')[:5]


class CreateQuestionView(generic.edit.CreateView):
    '''
    Some code from this tutorial to aid in adding choices to question view
    https://dev.to/zxenia/django-inline-formsets-with-class-based-views-and-crispy-forms-14o6
    Additional elements adapted in:
        - forms.py
        - create.html
        - custom_layout.py
        - formset.html
    as well as imported jquery.formset.js for dynamic choice additions
    '''
    model = Question
    template_name = 'polls/create.html'
    # fields = '__all__'
    form_class = CreateForm
    success_url = reverse_lazy('polls:index')

    def get_context_data(self, **kwargs):
        data = super(CreateQuestionView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['choices'] = CHOICE_FORM_SET(self.request.POST)
        else:
            data['choices'] = CHOICE_FORM_SET()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        choices = context['choices']
        if choices.is_valid():
            with transaction.atomic():
                self.object = form.save()
                choices.instance = self.object
                choices.save()
        else:
            return super(CreateQuestionView, self).form_invalid(form)
        return super(CreateQuestionView, self).form_valid(form)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        '''
        Excludes any questions not published
        '''
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def graph_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choice = []
    for ch in question.choice_set.all():
        choice.append(ch)
    return render(request, 'polls/graph.html', {'question': question,
                                                'choices': choice})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse(
            'polls:results', args=(question.id,)))


def autocomplete_model(request):
    if request.is_ajax():
        co = request.GET.get('query', '')
        search_cos = Company.objects.filter(name__istartswith=co)
        results = []
        for company in search_cos:
            inp = {}
            inp['value'] = company.name
            inp['data'] = company.id
            results.append(inp)
        resp = {"suggestions": results}
        data = json.dumps(resp)
    else:
        data = 'fail'
    mimetype = 'json'
    return HttpResponse(data, mimetype)
