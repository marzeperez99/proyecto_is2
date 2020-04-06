from django.db import models

# Create your models here.
from gestion_de_tipo_de_item.models import *


class EstadoDeItem:
    """
    Clase que especifica todos los estados en los que se puede encontrar un tipo de item

    Estados de un item:
        CREADO = "Creado"
        APROBADO = "Aprobado"
        EN_LINEA_BASE = "En Linea Base"
        ELIMINADO = "Eliminado"
        A_APROBAR = "Listo para su aprobación"
        EN_REVISION = "En Revisión"
        A_MODIFICAR = "A modificar"
    """
    CREADO = "Creado"
    APROBADO = "Aprobado"
    EN_LINEA_BASE = "En Linea Base"
    ELIMINADO = "Eliminado"
    A_APROBAR = "Listo para su aprobación"
    EN_REVISION = "En Revisión"
    A_MODIFICAR = "A modificar"


class Item(models.Model):
    """
    Modelo que representa a un item de una fase.
    TODO: COMENTAR!!!
    """
    tipo_de_item = models.ForeignKey(TipoDeItem,on_delete=models.CASCADE)
    estado = models.CharField(max_length=40)
    codigo = models.CharField(max_length=40)  # TODO: construir en el field: tipo_de_item.prefijo + #order
    version = models.ForeignKey('gestion_de_item.VersionItem', null=True,related_name= 'item_version',on_delete=models.CASCADE)

    def __str__(self):
        return self.version.nombre

    def get_fase(self):
        return self.tipo_de_item.fase

    def get_peso(self):
        return self.version.peso

    def get_antecesores(self):
        return self.version.antecesores

    def get_padres(self):
        return self.version.padres

    def get_numero_version(self):
        return self.version.version


class VersionItem(models.Model):
    """
    Modelo que representa la versión actual de un item y sus atributos versionables.
    """

    item = models.ForeignKey(Item, on_delete=models.CASCADE,related_name='version_item')
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=400)
    version = models.IntegerField()  # TODO: construir en el field: item.version_item_set.all.count() + 1
    peso = models.IntegerField()
    antecesores = models.ManyToManyField(Item,related_name='antecesores')
    padres = models.ManyToManyField(Item,related_name='padres')


class AtributoItemArchivo(models.Model):
    version = models.ForeignKey(VersionItem,on_delete=models.CASCADE)
    plantilla = models.ForeignKey(AtributoBinario,on_delete=models.CASCADE)
    url = models.CharField(
        max_length=500)  # TODO: Marcos, podes cambiar esto si ves necesario. Puede llamarse valor tambien para ser estandar.


class AtributoItemBooleano(models.Model):
    version = models.ForeignKey(VersionItem,on_delete=models.CASCADE)
    plantilla = models.ForeignKey(AtributoBooleano,on_delete=models.CASCADE)
    valor = models.BooleanField()


class AtributoItemFecha(models.Model):
    version = models.ForeignKey(VersionItem,on_delete=models.CASCADE)
    plantilla = models.ForeignKey(AtributoFecha,on_delete=models.CASCADE)
    valor = models.DateTimeField()


class AtributoItemNumerico(models.Model):
    version = models.ForeignKey(VersionItem,on_delete=models.CASCADE)
    plantilla = models.ForeignKey(AtributoNumerico,on_delete=models.CASCADE)
    valor = models.DecimalField(decimal_places=20,max_digits=20)


class AtributoItemCadena(models.Model):
    version = models.ForeignKey(VersionItem,on_delete=models.CASCADE)
    plantilla = models.ForeignKey(AtributoCadena,on_delete=models.CASCADE)
    valor = models.CharField(max_length=500)

