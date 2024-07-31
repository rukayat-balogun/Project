# views.py

import pickle
import numpy as np
from django.shortcuts import render
from .forms import BMIPredictionForm
from .recommendations import recommendations

# Load the model
with open('myapp/bmi_model.pkl', 'rb') as file:
    model = pickle.load(file)

def categorize_bmi(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 25:
        return 'Normal weight'
    elif 25 <= bmi < 30:
        return 'Overweight'
    elif 30 <= bmi < 40:
        return 'Obese'
    else:
        return 'Morbid Obesity'
    
def calculate_bmi(request):
    if request.method == 'POST':
        form = BMIPredictionForm(request.POST)
        if form.is_valid():
            height_feet = form.cleaned_data['height']
            weight_kg = form.cleaned_data['weight']
            
            # Convert height to inches and weight to pounds
            height_inches = height_feet * 12
            weight_pounds = weight_kg * 2.20462
            
            # Prepare the input for prediction
            X = np.array([[height_inches, weight_pounds]])
            
            # Predict BMI
            bmi = model.predict(X)
            
            # Determine category based on BMI
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 25:
                category = "Normal weight"
            elif 25 <= bmi < 30:
                category = "Overweight"
            elif 30 <= bmi < 40:
                category = "Obese"
            else:
                category = "Morbid Obesity"
            
            diet_recommendations = recommendations[category]['diet']
            fitness_recommendations = recommendations[category]['exercise']
            
            return render(request, 'bmi_result.html', {
                'bmi': bmi[0], 
                'category': category,
                'diet_recommendations': diet_recommendations,
                'fitness_recommendations': fitness_recommendations
            })
           
    else:
        form = BMIPredictionForm()
    return render(request, 'calculate_bmi.html', {'form': form})




