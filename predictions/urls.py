from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('predictor/', views.predictor, name='predictor'),  # Predictor page
    path('visualizer/', views.visualizer, name='visualizer'),
    path('predict/', views.predict, name='predict'),  # Visualizer page
]





