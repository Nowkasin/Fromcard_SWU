from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import set_language
from cards import views as cards_views
from cards.views import generate_pdf

urlpatterns = [
    path('admin/', admin.site.urls),

    path('i18n/setlang/', set_language, name='set_language'),

    path('cards/', include('cards.urls')),

    path('GOVCard/', cards_views.gov_card_view, name='gov_card'),

    path('api/address/', cards_views.address_api, name='address_api'),

    path('pdf/', generate_pdf, name='generate_pdf'),
]