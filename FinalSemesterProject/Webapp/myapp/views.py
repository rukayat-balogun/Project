from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .forms import BMIForm, BMIPredictionForm
import joblib
import pandas as pd


# def home(request):
#     return render(request, 'index.html')



# Load the trained model (assume you have saved it as 'random_forest_model.pkl')
#model = joblib.load('path/to/your/random_forest_model.pkl')

def calculate_bmi(erbmi, height, weight):
    # Prepare the input data
    input_data = pd.DataFrame({'erbmi': [erbmi], 'euhgt': [height], 'euwgt': [weight]})
    
    # Predict BMI
    #predicted_bmi = model.predict(input_data[['erbmi', 'euhgt', 'euwgt']])
    
    return input_data[0]

def home(request):
    if request.method == 'POST':
        form = BMIForm(request.POST)
        if form.is_valid():
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            erbmi = weight / (height / 100) ** 2
            predicted_bmi = calculate_bmi(erbmi, height, weight)
            return render(request, 'result.html', {'predicted_bmi': predicted_bmi})
    else:
        form = BMIForm()
    return render(request, 'index.html', {'form': form})




from django.shortcuts import render
from .forms import BMIPredictionForm
import joblib
from .recommendations import recommendations

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

def predict_bmi(request):
    if request.method == 'POST':
        form = BMIPredictionForm(request.POST)
        if form.is_valid():
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            
            # Load the model
            model = joblib.load('myapp/bmi_model.pkl')
            
            # Predict BMI
            bmi = model.predict([[height, weight]])[0]
            category = categorize_bmi(bmi)
            diet_recommendations = recommendations[category]['diet']
            exercise_recommendations = recommendations[category]['exercise']
            
            return render(request, 'result.html', {
                'bmi': bmi,
                'category': category,
                'diet_recommendations': diet_recommendations,
                'exercise_recommendations': exercise_recommendations
            })
    else:
        form = BMIPredictionForm()
    
    return render(request, 'predict_bmi.html', {'form': form})
