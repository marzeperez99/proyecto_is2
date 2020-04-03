from http import HTTPStatus

import pytest
from django.contrib.auth.models import User, Permission, Group
from django.test import Client
from django.urls import reverse

from roles_de_sistema.models import RolDeSistema


@pytest.fixture
def rs_admin():
    rol = RolDeSistema(nombre='Admin', descripcion='descripcion de prueba')
    rol.save()
    for pp in Permission.objects.filter(content_type__app_label='roles_de_sistema', codename__startswith='p'):
        rol.permisos.add(pp)
    rol.save()
    return rol

# Create your tests here.
@pytest.mark.django_db
def test_ver_usuario_existente(rs_admin):
    """
    Prueba el acceso a la información de un usuario existente dentro del sistema. \n
    Crea un usuario en la base de datos. \n
    Inicia sesión con este nuevo usuario. \n
    Accede a /usuarios/id con id igual a la clave primaria del usuario creado.

    Resultado esperado:
        Una respuesta HTTP con código 200

    Mensaje Error:
        No se puede acceder a '/usuarios/id' para un usuario existente.
    """
    user = User.objects.create(username='testing')
    user.set_password('12345')
    user.save()
    user.groups.add(Group.objects.get(name=rs_admin.nombre))
    client = Client()
    client.login(username='testing', password='12345')

    response = client.get(reverse('perfil_de_usuario', args=(user.id,)))
    assert response.status_code == HTTPStatus.OK, 'No se puede acceder a \'/usuarios/id\' para un usuario existente.'


@pytest.mark.django_db
def test_ver_usuario_no_existente(rs_admin):
    """
        Prueba el acceso a la información de un usuario no existente dentro del sistema. \n
        Crea un usuario en la base de datos. \n
        Inicia sesión con este nuevo usuario. \n
        Accede a /usuarios/id con id distinto al de la clave primaria del usuario creado.

        Resultado esperado:
            Una respuesta HTTP con código 404

        Mensaje Error:
            El sistema muestra información de un usuario no existente.
        """
    user = User.objects.create(username='testing')
    user.set_password('12345')
    user.save()
    user.groups.add(Group.objects.get(name=rs_admin.nombre))
    client = Client()
    client.login(username='testing', password='12345')

    response = client.get(reverse('perfil_de_usuario', args=(user.id + 1,)))
    assert response.status_code == HTTPStatus.NOT_FOUND, 'El sistema muestra información de un usuario no existente.'


@pytest.mark.django_db
def test_ver_usuarios(rs_admin):
    """
        Prueba el acceso a la lista de usuarios existentes dentro del sistema. \n
        Crea un usuario en la base de datos. \n
        Inicia sesión con este nuevo usuario. \n
        Accede a /usuarios/ .

        Resultado esperado:
            Una respuesta HTTP con código 200

        Mensaje Error:
            No es posible visualizar la lista de usuarios
        """
    user = User.objects.create(username='testing')
    user.set_password('12345')
    user.save()
    user.groups.add(Group.objects.get(name=rs_admin.nombre))
    client = Client()
    client.login(username='testing', password='12345')

    response = client.get(reverse('usuarios'))
    assert response.status_code == HTTPStatus.OK, 'No es posible visualizar la lista de usuarios'
