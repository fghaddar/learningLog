from django.db import models

# Create your models here.

class Topic(models.Model):                                                              # This class (Topic) inherits from Model. Model defines the basic functionality of a model, which is what we want this class to be
    """A topic the user is learning about."""
    text = models.CharField(max_length=200)                                             # Char field is similar to char in MySQL
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text

class Entry(models.Model):                                                              # Creating a model, so needs to inherit from Model
    """Something specific learned about a topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)                          # Foreign Key references Topic, which is another record in the database
    text = models.TextField()                                                           # Text about the entry
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:                                                                         # Nested class Meta holds extra information for managing a model
        verbose_name_plural = 'entries'                                                 # When referring to moer than one entry, use 'entries'

    def __str__(self):                                                                  # Which information to show when referring to an individual entry
        """Return a string representation of the model."""                              # In this case, just show the first 50 characters with a '....'
        return self.text[:50] + "..."