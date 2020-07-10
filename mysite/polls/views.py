from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'  # By default the template receives the objects
                                                  # stored in a variable called 'object_list'.
                                                  # To change this name, just set this attribute

    def get_queryset(self):
        """Return the latest five published question."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):  
    model = Question                        # As this is a DetailView, variable 'question' is 
    template_name = 'polls/detail.html'     # automatically passed to the template. Where it 
                                            # refers to the model object with the specified pk

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    
class ThanksView(generic.DetailView):
    model = Question
    template_name = 'polls/thanks.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #Redisplay the question voting form.
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice.",})

    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after succesfully dealing
        # with POST data. This prevents data from being posted twice if a 
        # user hits the Back button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
