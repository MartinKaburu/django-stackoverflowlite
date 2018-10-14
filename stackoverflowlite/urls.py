from django.urls import path

from . import views

urlpatterns = [
    path('questions', views.getPostQue, name='getQuestions'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('questions/<int:queId>/answers', views.ansQue, name='answerQuestion'),
    path('questions/<int:queId>', views.getDelEditQue, name='getDelEditQue'),
    path('questions/<int:queId>/answers/<int:ansId>', views.editDelAns, name='answerQuestion')
]
