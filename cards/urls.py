from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('', views.request_card_view, name='request_card'),
]