from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('calculate_bmi/', views.calculate_bmi, name='calculate_bmi'),
]
