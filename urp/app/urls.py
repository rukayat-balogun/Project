from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('who-we-are/', views.who_we_are, name='who_we_are'),
    path('what-we-do/', views.what_we_do, name='what_we_do'),
    path('gallery/', views.gallery, name='gallery'),
     path('gallery/upload/', views.upload_image, name='upload_image'),
    path('events/', views.events, name='events'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('partnership/', views.partnership, name='partnership'),
]
