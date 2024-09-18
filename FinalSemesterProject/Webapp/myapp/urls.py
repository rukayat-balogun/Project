from django.urls import path
from . import views

urlpatterns = [
  path('fitness', views.home, name='home'),
  path('calculate_bmi/', views.calculate_bmi, name='calculate_bmi'),
  path('thank-you/', views.thank_you, name='thank_you'),
  path('feedback/', views.feedback_view, name='feedback'),
]
