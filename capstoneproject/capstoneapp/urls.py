from django.urls import path
from . import views
from .views import askQuestion

urlpatterns = [
    path('', views.index, name='index'),
    path('askQuestion/', views.askQuestion, name='askQuestion')
]