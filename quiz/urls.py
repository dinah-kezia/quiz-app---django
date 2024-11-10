from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('subjects/', views.subjects, name='subjects'),
    path('quiz/<int:subject_id>/', views.quiz, name='quiz'),
    path('score/', views.score, name='score'),
]
