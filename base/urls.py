from django.urls import path
from base import views 

urlpatterns =[
    path('',views.chatbot,name='chatbot'),
    path('login', views.login, name = 'login'),
    path('signup', views.signup, name = 'signup'),
]