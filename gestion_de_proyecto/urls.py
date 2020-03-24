from django.urls import path
from . import views


urlpatterns = [
    path('nuevo/', views.nuevo_proyecto_view, name='nuevo'),
    # path('editar/', views.editar_proyecto_view, name='editarProyecto'),
    # path('visualizarProyecto/', views.visualizar_proyecto_view, name='visualizarProyecto'),
    # path('', views.visualizar_proyectos_view, name='visualizarProyectos'),
    # path('<int:proyecto>/fase/',)
    path('<int:proyecto_id>/participante/nuevo/', views.nuevo_participante_view, name='nuevo_participante'),
    path('<int:proyecto_id>/permisos_insuficientes', views.pp_insuficientes, name='pp_insuficientes'),

]