from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet

from .forms import CustomSearch
from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(question.get_absolute_url())


def custom_search(request):
    form = CustomSearch(request.GET)

    context = {}
    if form.is_valid():
        page_number = request.GET.get('page')
        results = SearchQuerySet().filter(content=AutoQuery(form.cleaned_data['q']))
        context['page'] = Paginator(results, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE).get_page(page_number)

    context['form'] = form

    return render(request, 'polls/custom_search.html', context)
