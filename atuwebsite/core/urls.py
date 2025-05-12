from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('services/<slug:service_slug>/', views.service_detail, name='service_detail'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('search/', views.search_courses, name='search'),
    path('pay/<int:course_id>/', views.initiate_payment, name='initiate_payment'),
   path('payment-success/<int:course_id>/', views.payment_success, name='payment_success'),
    path('paystack-webhook/', views.paystack_webhook, name='paystack_webhook'),  # 👈 Add this
]
