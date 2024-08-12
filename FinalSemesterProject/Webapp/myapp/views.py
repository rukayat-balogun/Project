import os
import random
import pickle
import numpy as np
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import BMIPredictionForm, FeedbackForm
from .models import Feedback

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

def get_random_images(category, subcategory, num_images=5):
    """Get random images from the specified category and subcategory folder."""
    image_folder = os.path.join(settings.STATICFILES_DIRS[0], 'recommendations', category, subcategory)
    
    if not os.path.exists(image_folder):
        print(f"Directory not found: {image_folder}")
        return []

    images = os.listdir(image_folder)
    
    if not images:
        return []

    selected_images = random.sample(images, min(num_images, len(images)))
    
    return [os.path.join(settings.STATIC_URL, 'recommendations', category, subcategory, image) for image in selected_images]

def calculate_bmi(request):
    if request.method == 'POST':
        form = BMIPredictionForm(request.POST)
        feedback_form = FeedbackForm(request.POST)
        
        if form.is_valid():
            height_feet = form.cleaned_data['height']
            weight_kg = form.cleaned_data['weight']
            
            height_inches = round((height_feet * 12),2)
            weight_pounds = round((weight_kg * 2.20462),2)
            
            X = np.array([[height_inches, weight_pounds]])
            
            bmi = round(model.predict(X)[0],2)
            
            category = categorize_bmi(bmi)
            
            diet_images = get_random_images(category, 'diet', num_images=5)
            fitness_images = get_random_images(category, 'fitness', num_images=5)
            
            if feedback_form.is_valid():
                feedback_form.save()
                return redirect('thank_you')
            
            return render(request, 'bmi_result.html', {
                'bmi': bmi,
                'category': category,
                'diet_images': diet_images,
                'fitness_images': fitness_images,
                'feedback_form': feedback_form
            })
    else:
        form = BMIPredictionForm()
        feedback_form = FeedbackForm()

    return render(request, 'calculate_bmi.html', {'form': form, 'feedback_form': feedback_form})

def thank_you(request):
    return render(request, 'thank_you.html')

def feedback_view(request):
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback_form.save()
            return redirect('thank_you')  # Redirect to thank you page after submitting feedback
    else:
        feedback_form = FeedbackForm()

    return render(request, 'feedback.html', {'feedback_form': feedback_form})