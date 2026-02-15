from django.urls import path
from . import views

app_name = 'boleto'

urlpatterns = [    
    path('', views.boletos_view, name='boletos'),
    #path('sorteo/', views.sorteo_view, name='sorteo'),
    path('sorteo/', views.generar_ganador, name='sorteo'),
    path('boletos/', views.boletos_view, name='boletos'),
    path('resultados/', views.dashboard, name='resultados'),
    path('boletos/download_pdf/', views.download_tickets_pdf, name='download_tickets_pdf'),
    path('<slug:slug>/', views.page_view, name='page'),
]
