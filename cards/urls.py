from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    # หน้า form
    path('', views.request_card_view, name='request_card'),

    # 🔥 หน้า preview / print
    path('print/<int:pk>/', views.print_card_view, name='print_card'),

    # 🔥 export PDF
    path('export-pdf/<int:pk>/', views.export_pdf_view, name='export_pdf'),
]