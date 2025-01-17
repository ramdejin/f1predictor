from django.urls import path
from . import views

urlpatterns = [
    path('', views.predictor_view, name='home'),  # Root URL mapped to the predictor form
    path('predict/', views.predict, name='predict'),  # Predict endpoint
]




