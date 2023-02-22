from django.urls import path
from .views import TelegramBotView,HomeView

app_name = 'fun_bot'

urlpatterns = [
    
    path('c817304a3d163ebd58b44dd446eba29572300724098cdbca1a/', TelegramBotView.as_view(), name="telegram_bot_view"),
    path('home/', HomeView.as_view(), name="home_view"),
    
    # path('', views.TelegramBotView.as_view()),
]


