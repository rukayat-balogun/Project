from django import forms
from .models import Gallery, Event, NewsEvent

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title', 'description', 'image']




class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'image', 'date', 'description']

class NewsEventForm(forms.ModelForm):
    class Meta:
        model = NewsEvent
        fields = ['title', 'image', 'date', 'description']