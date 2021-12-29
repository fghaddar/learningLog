from django.shortcuts import render
from . models import Entry, Topic                                                              # Import topics, which is a model that we need
from . forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect
from django.urls import reverse

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

def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':                                                        # No data is submitted, so create a blank form
        form = TopicForm()                                                              
    else:                                                                               # Post data submitted; process data
        form = TopicForm(request.post)                                                  # Make an instance of TopicForm and pass it the data entered by the user stored in request.POST: returns a form object that contain's information submitted by the user                                             
        if form.is_valid():                                                             # Check if form is valid: all filled in, with valid data entered?
            form.save()                                                                 # Write the form to the database
            return HttpResponseRedirect(reverse('learning_logs:topics'))                # We have a page named topics. Reverse finds the URL path for that page. We are then redirected to that URL
    
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)                                         # Create a new entry object, load it into new_entry, but don't commit to the database yet
            new_entry.topic = topic                                                     # Add the topic about the entry
            new_entry.save()                                                            # Now we save
            return HttpResponseRedirect(                                                # Redirect to the topic page the entry was made for                                         
                reverse('learning_logs:topic', args=[topic_id]))

    context = {'topic':topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    """Edit an exisiting entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)