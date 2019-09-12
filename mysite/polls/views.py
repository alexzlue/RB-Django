from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.db.models import Count

from .models import Choice, Question, Company
from .forms import CreateForm


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
    model = Question
    template_name = 'polls/create.html'
    fields = '__all__'
    success_url = reverse_lazy('polls:index')


# class UpdateQuestionView(generic.edit.UpdateView):
#     model = Question


# class DeleteQuestionView(generic.edit.DeleteView):
#     model = Question


def create_question(request):
    form = CreateForm()
    return render(request, 'polls/create.html', {'form': form})


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
