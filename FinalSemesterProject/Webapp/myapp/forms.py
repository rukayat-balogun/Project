

from django import forms
from .models import Feedback

class BMIPredictionForm(forms.Form):
    height = forms.FloatField(label='Height (in feet)')
    weight = forms.FloatField(label='Weight (in Kg)')





class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'comments']
