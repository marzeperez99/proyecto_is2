"""

proyecto_is2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
from django.contrib import admin
from django.urls import path, include  # <--

urlpatterns = [
    path('', include('sso.urls')),
    path('accounts/', include('allauth.urls')),  # <--
    path('roles_de_proyecto/', include('roles_de_proyecto.urls')),
    path('roles_de_sistema/', include('roles_de_sistema.urls')),
    path('', include('usuario.urls')),
    path('proyecto/<int:proyecto_id>/fase/<int:fase_id>/', include('gestion_de_tipo_de_item.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('proyecto/', include('gestion_de_proyecto.urls')),
    path('proyecto/<int:proyecto_id>/fase/', include('gestion_de_fase.urls')),
    path('proyecto/<int:proyecto_id>/solicitudes/', include('gestion_de_solicitud.urls')),
    path('proyecto/<int:proyecto_id>/fase/<int:fase_id>/item/', include('gestion_de_item.urls')),
    path('proyecto/<int:proyecto_id>/fase/<int:fase_id>/linea_base/', include('gestion_linea_base.urls')),
    path('notificaciones/',include('gestion_de_notificaciones.urls'))
]
