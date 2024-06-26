from django.urls import path
from . import views
from .views import askQuestion
from .views import apiAskQuestion, apiSendData

urlpatterns = [
    path('', views.index, name='index'),
    path('askQuestion/', views.askQuestion, name='askQuestion'),
    path('apiAskQuestion/', apiAskQuestion, name='apiAskQuestion'),
    path('apiSendData/', apiSendData, name='apiSendData')
]