

from django import forms

class BMIPredictionForm(forms.Form):
    height = forms.FloatField(label='Height (in feet)')
    weight = forms.FloatField(label='Weight (in Kg)')




class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, label="Your Name")
    email = forms.EmailField(required=False, label="Your Email")
    comments = forms.CharField(widget=forms.Textarea, label="Your Feedback")
