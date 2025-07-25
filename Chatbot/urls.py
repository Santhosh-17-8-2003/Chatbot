
from django.urls import path
from AIchat import views

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path('index/', views.chat_view, name="index"),
    path('get_bot_response_ajax/', views.get_bot_response_ajax, name='get_bot_response_ajax')
]

