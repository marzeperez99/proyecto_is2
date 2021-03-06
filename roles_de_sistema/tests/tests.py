from http import HTTPStatus

import pytest
from django.contrib.auth.models import Permission, User, Group
from django.test import Client
from django.urls import reverse

from usuario.models import Usuario
from roles_de_sistema.models import RolDeSistema


@pytest.fixture
def rs_admin():
    rol = RolDeSistema(nombre='Admin', descripcion='descripcion de prueba')
    rol.save()
    for pp in Permission.objects.filter(content_type__app_label='roles_de_sistema', codename__startswith='p'):
        rol.permisos.add(pp)
    rol.save()
    return rol


@pytest.fixture
def usuario():
    user = User(username='user_test', email='test@admin.com')
    user.set_password('password123')
    user.save()
    return user


@pytest.fixture
def cliente_loggeado(usuario):
    client = Client()
    client.login(username='user_test', password='password123')
    return client


@pytest.fixture
def rol_de_sistema():
    rs = RolDeSistema(nombre='RSTest',
                      descripcion='Descripcion del rol')
    rs.save()
    for permiso in Permission.objects.all().filter(codename__startswith='ps_'):
        rs.permisos.add(permiso)
    return rs


@pytest.mark.django_db
class TestModeloRolDeSistema:
    """
    Pruebas unitarias que comprueban el funcionamiento de los métodos del Modelo RolDeSistema
    """

    def test_get_permisos(self, rol_de_sistema):
        """
        Prueba unitaria encargada de probar metodo get_permisos para asegurarse que al \
        tratar de obtener los permisos de un rol creado sin permisos retorne una lista \
        vacia

        Se espera:
            Que el metodo get_permisos retorne la lista de permisos del Rol de Sistema.

        Mensaje de Error:
            No se pudo traer la lsta de permisos correctamente
        """
        ps_rol = rol_de_sistema.get_permisos()
        ps_list = Permission.objects.all().filter(codename__startswith='ps_')
        assert all(p in ps_rol for p in ps_list) and all(p in ps_list for p in ps_rol), \
            'No se pudo traer la lsta de permisos correctamente'

    def test_roldesistema_lista_de_permisos_vacia(self):
        """
        Prueba unitaria encargada de probar metodo get_permisos para asegurarse que al tratar de obtener los permisos de un
        rol creado sin permisos retorne una lista vacia
        """
        rs = RolDeSistema(nombre='rol1', descripcion="descripcion")
        rs.save()

        permisos_obtenidos = rs.get_permisos()

        assert permisos_obtenidos == [], "Los permisos asignados al rol no fueron guardados correctamente,"

    def test_rol_de_sistema_es_utilzado(self, usuario, rol_de_sistema):
        """
        Prueba unitaria encargada de probar si un RS fue asignado a un usuario
        """
        usuario = Usuario.objects.get(id=usuario.id)
        usuario.asignar_rol_a_usuario(rol_de_sistema.id)
        assert rol_de_sistema.es_utilizado() == True, "La asignacion de RS al usuario no se se realizó de manera correcta"

    def test_rol_de_sistema_no_es_utilzado(self, rol_de_sistema):
        """
        Prueba unitaria encargada de probar si un RS no fue asignado a ningún usuario
        """
        assert not rol_de_sistema.es_utilizado() == True, "Ocurrió algun error al asignar este RS"

    def test_eliminar_rol_de_sistema_exito(self, usuario, rol_de_sistema):
        """
        Prueba unitaria encargada de probar la condicion de que un rol no puede ser eliminado si un usuario tiene
        asignado dicho rol
        """
        usuario = Usuario.objects.get(id=usuario.id)
        usuario.asignar_rol_a_usuario(rol_de_sistema.id)
        assert rol_de_sistema.eliminar_rs() == False, "El metodo no puede derterminar si existe una asignacion de este rol " \
                                                      "a un usuario"

    def test_eliminar_rol_de_sistema_fallido(self, rol_de_sistema):
        """
        Prueba unitaria encargada de probar la condicion de que un rol si puede ser eliminado si ningun usuario tiene
        asignado dicho rol
        """
        assert rol_de_sistema.eliminar_rs() == True, "El metodo no puede derterminar si existe una asignacion de este rol " \
                                                     "a un usuario"


@pytest.mark.django_db
class TestVistasRolDeSistema:
    """
    Pruebas unitarias que comprueban el funcionamiento de las vistas referentes a los Roles de Sistema.
    """

    def test_listar_roles_de_sistema_view(self, usuario, cliente_loggeado, rs_admin):
        """
        Prueba unitaria encargada de verificar que la vista listar_roles_de_sistema_view \
        se muestre correctamente

        Se espera:
            HttpResponse 200

        Mensaje de Error:
            Hubo un error al cargar la pagina
        """
        usuario.groups.add(Group.objects.get(name=rs_admin.nombre))
        response = cliente_loggeado.get(reverse('listar_roles_de_sistema'))

        assert response.status_code == HTTPStatus.OK, 'Hubo un error al cargar la pagina, '

    def test_editar_rol_de_sistema_view(self, usuario, cliente_loggeado, rs_admin, rol_de_sistema):
        """
        Prueba unitaria encargada de verificar que la vista editar_rol_de_sistema_view \
        se muestre correctamente

        Se espera:
            HttpResponse 200

        Mensaje de Error:
            Hubo un error al cargar la pagina
        """
        usuario.groups.add(Group.objects.get(name=rs_admin.nombre))
        usuario.save()

        response = cliente_loggeado.get(reverse('editar_rol_de_sistema', args=(rol_de_sistema.id,)))

        assert response.status_code == HTTPStatus.OK, 'Hubo un error al cargar la pagina, '

    def test_rol_de_sistema_view(self, usuario, cliente_loggeado, rs_admin, rol_de_sistema):
        """
        Prueba unitaria encargada de verificar que la vista rol_de_sistema_view \
        se muestre correctamente

        Se espera:
            HttpResponse 200

        Mensaje de Error:
            Hubo un error al cargar la pagina
        """
        usuario.groups.add(Group.objects.get(name=rs_admin.nombre))
        usuario.save()

        response = cliente_loggeado.get(reverse('rol_de_sistema', args=(rol_de_sistema.id,)))

        assert response.status_code == HTTPStatus.OK, 'Hubo un error al cargar la pagina, '

    def test_eliminar_rol_de_sistema_view(self, usuario, cliente_loggeado, rs_admin, rol_de_sistema):
        """
        Prueba unitaria encargada de verificar que la vista eliminar_rol_de_sistema_view \
        se muestre correctamente

        Se espera:
            HttpResponse 200

        Mensaje de Error:
            Hubo un error al cargar la pagina
        """
        usuario.groups.add(Group.objects.get(name=rs_admin.nombre))
        usuario.save()

        response = cliente_loggeado.get(reverse('eliminar_rol_de_sistema', args=(rol_de_sistema.id,)))

        assert response.status_code == HTTPStatus.OK, 'Hubo un error al cargar la pagina, '

    def test_nuevo_rol_de_sistema_view(self, usuario, cliente_loggeado, rs_admin):
        """
        Test encargado de comprobar que no ocurra nigun error al cargar la pagina con un usuario que ha iniciado sesion
        """
        usuario.groups.add(Group.objects.get(name=rs_admin.nombre))
        response = cliente_loggeado.get(reverse('nuevo_rol_de_sistema'))

        assert response.status_code == HTTPStatus.OK, 'Hubo un error al cargar la pagina, '
