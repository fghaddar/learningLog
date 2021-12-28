from django.shortcuts import render
from . models import Topic                                                              # Import topics, which is a model that we need

# Create your views here.

def index(request):                                                                     # The request object is sent along when we call this function. We can use it to process data
    """The home page for Learning Log"""
    return render(request, 'learning_logs/index.html')                                  # Two arguments: rwquest object, and an html template page

def topics(request):
    """Show all topics."""
    topics = Topic.objects.order_by('date_added')                                       
    context = {'topics': topics}                                                        # context is a dictionary we send the template so that it can use the information within it
    return render(request, 'learning_logs/topics.html', context)                        # On top of the request object and the html page to render, we send the context

def topic(request, topic_id):
    """Show a single topic and all of its entries"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)