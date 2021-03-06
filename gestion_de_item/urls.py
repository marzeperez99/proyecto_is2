from django.urls import path

from . import views

urlpatterns = [
    path('', views.listar_items, name='listar_items'),
    path('en_revision', views.listar_items_en_revision, name='listar_items_en_revision'),
    path('nuevo/', views.nuevo_item_view, name='nuevo_item'),
    path('<int:item_id>/relacionar/', views.relacionar_item_view, name='relacionar_item'),
    path('nuevo/<int:tipo_de_item_id>/', views.nuevo_item_view, name='nuevo_item_tipo'),
    path('<int:item_id>/', views.visualizar_item, name='visualizar_item'),
    path('<int:item_id>/relacion/<int:item_relacion_id>/eliminar', views.eliminar_relacion_item_view,
         name='eliminar_relacion_item'),
    path('<int:item_id>/eliminar/', views.eliminar_item_view, name='eliminar_item'),
    path('<int:item_id>/historial/', views.ver_historial_item_view, name='historial_item'),
    path('<int:item_id>/solicitar_aprobacion/', views.solicitar_aprobacion_view, name='solicitar_aprobacion_item'),
    path('<int:item_id>/aprobar/', views.aprobar_item_view, name='aprobar_item'),
    path('<int:item_id>/desaprobar/', views.desaprobar_item_view, name='desaprobar_item'),
    path('<int:item_id>/editar/', views.editar_item_view, name='editar_item'),
    path('<int:item_id>/archivo/<int:atributo'
         '_id>/eliminar', views.eliminar_archivo_view,
         name='eliminar_archivo_item'),
    path('<int:item_id>/modificar/', views.debe_modificar_view, name='debe_ser_modificado'),
    path('<int:item_id>/no_modificar/', views.no_modificar_view, name='no_modificar'),
    path('<int:item_id>/restaurar/<int:version_id>/', views.restaurar_version_item_view, name='restaurar_item'),
    path('<int:item_id>/terminar_revision', views.terminar_revision_view, name='terminar_revision'),
    path('<int:item_id>/reporte', views.reporte_de_item_view, name="reporte_de_item"),
    path('reporte/', views.reporte_de_items_view, name='reporte_de_items'),
]
