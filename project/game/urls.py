from django.urls import path
from . import views

urlpatterns = [
    path('', views.train, name='train'),
    path('result-game/', views.win_lose, name='result-game'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('clarify-question/', views.clarify_question, name='clarify-question'),
    path('api-game/', views.apiGame, name='apiGame'),
]
