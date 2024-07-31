

from django import forms

class BMIPredictionForm(forms.Form):
    height = forms.FloatField(label='Height (in feet)')
    weight = forms.FloatField(label='Weight (in Kg)')