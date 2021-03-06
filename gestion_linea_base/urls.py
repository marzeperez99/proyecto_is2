from django.urls import path

from . import views

urlpatterns = [
    path('nuevo/', views.nueva_linea_base_view, name='nuevo_linea_base'),
    path('<int:linea_base_id>/', views.visualizar_linea_base_view, name='visualizar_linea_base'),
    path('', views.listar_linea_base_view, name='listar_linea_base'),
    path('<int:linea_base_id>/solicitar_rompimiento/', views.solicitar_rompimiento_view, name='solicitar_rompimiento'),
    path('<int:linea_base_id>/reporte/', views.reporte_linea_base_view, name='reporte_linea_base'),
]
