from django.urls import path
from . import views

urlpatterns = [
  path('calculate_bmi/', views.calculate_bmi, name='calculate_bmi'),
]
