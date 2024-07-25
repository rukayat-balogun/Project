from django import forms

class BMIForm(forms.Form):
    height = forms.FloatField(label='Height (cm)', min_value=0)
    weight = forms.FloatField(label='Weight (kg)', min_value=0)



class BMIPredictionForm(forms.Form):
    height = forms.FloatField(label='Height (meters)')
    weight = forms.FloatField(label='Weight (kg)')
