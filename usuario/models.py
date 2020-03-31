from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
from roles_de_sistema.models import RolDeSistema


class Usuario(User):
    """
    Modelo proxy que extiende el modelo User de Django.

    """
    class Meta:
        proxy = True

    def asignar_rol_a_usuario(self, rs_id):
        self.groups.clear()
        rs = RolDeSistema.objects.get(id=rs_id)
        print(rs.nombre)
        group = Group.objects.get(name=rs.nombre)
        self.groups.add(group)

    def desasignar_rol_a_usuario(self):
        self.groups.clear()

    def tiene_rs(self):
        return self.groups.all().exists()

    def get_rol_de_sistema(self):
        """
        Metodo que retorna el rol de Sistema que tiene asignado el usuairo.

        Retorna:
            RolDeSistema: objeto con los datos del rol de sistema asignado al usuario.
        """
        assert self.groups.all().count() in [0, 1], 'El usuario tiene mas de un rol de sistema asignado'
        if self.groups.all().count() == 1:
            rol = self.groups.all()[0]
            return RolDeSistema.objects.get(nombre=rol.name)
        return None

