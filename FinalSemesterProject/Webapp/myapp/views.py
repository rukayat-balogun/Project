import os
import random
import pickle
import numpy as np
from django.conf import settings
from django.shortcuts import render
from .forms import BMIPredictionForm

# Load the model

def home(request):

    return render(request, 'index.html')



with open('myapp/bmi_model.pkl', 'rb') as file:
    model = pickle.load(file)

def categorize_bmi(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 25:
        return 'Normal_weight'
    elif 25 <= bmi < 30:
        return 'Overweight'
    elif 30 <= bmi < 40:
        return 'Obese'
    else:
        return 'Morbid_Obesity'

def get_random_images(category, num_images=5):
    """Get random images from the specified category folder."""
    image_folder = os.path.join(settings.STATIC_ROOT, 'recommendations', category)
    images = os.listdir(image_folder)
    selected_images = random.sample(images, min(num_images, len(images)))
    # Construct URLs for static files
    return [os.path.join('recommendations', category, image) for image in selected_images]

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
            bmi = model.predict(X)[0]
            
            # Determine category based on BMI
            category = categorize_bmi(bmi)
            
            # Get random image recommendations
            diet_images = get_random_images(category, num_images=5)
            
            return render(request, 'bmi_result.html', {
                'bmi': bmi,
                'category': category,
                'diet_images': diet_images,
            })
    else:
        form = BMIPredictionForm()
    return render(request, 'calculate_bmi.html', {'form': form})
