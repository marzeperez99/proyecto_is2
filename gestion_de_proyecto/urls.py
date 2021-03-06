from django.urls import path
from . import views


urlpatterns = [
    path('nuevo/', views.nuevo_proyecto_view, name='nuevo_proyecto'),
    path('<int:proyecto_id>/', views.visualizar_proyecto_view, name='visualizar_proyecto'),
    path('<int:proyecto_id>/info/', views.info_proyecto_view, name='info_proyecto'),
    path('<int:proyecto_id>/editar/', views.editar_proyecto_view, name='editar_proyecto'),
    path('<int:proyecto_id>/cancelar/', views.cancelar_proyecto_view, name='cancelar_proyecto'),
    path('<int:proyecto_id>/finalizar/', views.finalizar_proyecto_view, name='finalizar_proyecto'),
    path('<int:proyecto_id>/iniciar/', views.iniciar_proyecto_view, name='iniciar_proyecto'),
    path('<int:proyecto_id>/participante/nuevo/', views.nuevo_participante_view, name='nuevo_participante'),
    path('<int:proyecto_id>/permisos_insuficientes/', views.pp_insuficientes, name='pp_insuficientes'),
    path('<int:proyecto_id>/participante/<int:participante_id>/', views.participante_view,
         name='participante'),
    path('<int:proyecto_id>/participante/<int:participante_id>/asignar_rol_de_proyecto/',
         views.asignar_rol_de_proyecto_view, name='asignar_rol_de_proyecto'),
    path('<int:proyecto_id>/participante/', views.participantes_view, name='participantes'),
    path('<int:proyecto_id>/participante/<int:participante_id>/eliminar/', views.eliminar_participante_view,
         name='eliminar_participante'),
    path('<int:proyecto_id>/comite/asignar',views.seleccionar_miembros_del_comite_view, name='asignar_miembros_comite'),
    path('<int:proyecto_id>/reporte/', views.reporte_de_proyecto_view, name='reporte_de_proyecto'),
]
