from django.db import models
from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()


# Create your models here.


class EstadoDeItem:
    """
    Clase que especifica todos los estados en los que se puede encontrar un tipo de item

    Estados de un item:
        - NO_APROBADO = "No Aprobado"
        - APROBADO = "Aprobado"
        - EN_LINEA_BASE = "En Linea Base"
        - ELIMINADO = "Eliminado"
        - A_APROBAR = "Listo para su aprobación"
        - EN_REVISION = "En Revisión"
        - A_MODIFICAR = "A modificar"
    """
    NO_APROBADO = "No Aprobado"
    APROBADO = "Aprobado"
    EN_LINEA_BASE = "En Linea Base"
    ELIMINADO = "Eliminado"
    A_APROBAR = "Listo para su aprobación"
    EN_REVISION = "En Revisión"
    A_MODIFICAR = "A modificar"


class Item(models.Model):
    """
    Modelo que representa a un item de una fase.

    - tipo_de_item: TipoDeItem, el tipo de este ite,
    - estado: EstadoItem, estado en que se encuentra el item
    - version: VersionItem, versión actual de este item.

    """
    tipo_de_item = models.ForeignKey('gestion_de_tipo_de_item.TipoDeItem', on_delete=models.CASCADE)
    estado = models.CharField(max_length=40)
    codigo = models.CharField(max_length=40)
    version = models.ForeignKey('gestion_de_item.VersionItem', null=True, related_name='item_version',
                                on_delete=models.CASCADE)
    encargado_de_modificar = models.ForeignKey('gestion_de_proyecto.Participante', null=True, default=None,
                                               on_delete=models.CASCADE)
    estado_anterior = models.CharField(max_length=40, default="")

    # No cambiar save() o se rompe
    def nueva_version(self):
        """
        Método que crea una nueva version para el item. Debe ser invocado antes de modificar un item y solo si se desea modificar.

        Ej:

            >>> item = Item.objects.first()
            >>> item.nueva_version()
            >>> item.agregar_padre(padre)
        """

        version = VersionItem(nombre=self.version.nombre, descripcion=self.version.descripcion, peso=self.version.peso,
                              item=self, version=self.version.version + 1)
        version.save()

        # version.save(versionar=True)
        assert version != self.version
        # Agrega los atributos dinamicos del item
        for atributo in self.get_atributos_dinamicos():
            atributo.pk = None
            atributo.version = version
            atributo.save()
        # Agrega los padres del item
        for item in self.get_padres():
            print('Un padre de este item es:' + str(item))
            version.padres.add(item)
        # Agrega los antecesores del item
        for item in self.get_antecesores():
            version.antecesores.add(item)

        self.version = version
        self.save()

    def __str__(self):
        return self.version.nombre

    def get_fase(self):
        return self.tipo_de_item.fase

    def get_peso(self):
        return self.version.peso

    def get_antecesores(self):
        return self.version.antecesores.all()

    def get_padres(self):
        return self.version.padres.all()

    def get_hijos(self):
        """
        Metodo del model item, filtra y retorna los items cuya version mas actual tenga como
        padre el item en cuestion.\n
        Retorna:
            -Item que cumplan las condiciones especificadas.
        """
        hijos = self.hijos.all()
        lista_hijos = []
        for hijo in hijos:
            if hijo == hijo.item.version and hijo.item.estado != EstadoDeItem.ELIMINADO:
                lista_hijos.append(hijo.item.id)
        return Item.objects.filter(id__in=lista_hijos)

    def get_sucesores(self):
        """
        Metodo del model item, filtra y retorna los items cuya version mas actual tenga como
        antecesor el item en cuestion.\n
        Retorna:
            -Item que cumplan las condiciones especificadas.
        """
        sucesores = self.sucesores.all()
        lista_sucesores = []
        for sucesor in sucesores:
            if sucesor == sucesor.item.version and sucesor.item.estado != EstadoDeItem.ELIMINADO:
                lista_sucesores.append(sucesor.item.id)
        return Item.objects.filter(id__in=lista_sucesores)

    def get_numero_version(self):
        return self.version.version

    def get_atributos_dinamicos(self):
        """
        Metodo que retorna la lista de atributos dinamicos del Item.

        Retorna:
            list(): lista de objetos AtributoItemNumerico, AtributoItemFecha,
        """
        return self.version.get_atributos_dinamicos()

    def get_versiones(self):
        """
        Metodo que retorna la lista de versiones de un determinado Item.

        Retorna:
            list(): lista de objetos Version, con los datos de la version del item
        """
        return self.version_item.all().order_by('-version')

    def eliminar(self):
        """
        Meétodo del model Item que permite cambiar el estado de un item a ELIMINADO.\n
        Lanza:
            -Exception: si el item tiene un estado diferente a No Aprobado, o el item tiene una relacion (padre-hijo) o
            (antececesor-sucesor) con otro item
        """
        mensaje_error = []
        # mensaje_error.append('El ítem no puede ser eliminado debido a las siguientes razones:')
        if self.estado != EstadoDeItem.NO_APROBADO:
            mensaje_error.append('El item se encuentra en el estado ' + self.estado)
            raise Exception(mensaje_error)
        hijos = self.get_hijos()
        sucesores = self.get_sucesores()
        if hijos.count() != 0 or sucesores.count() != 0:
            for hijo in hijos:
                mensaje_error.append(
                    'El item es el padre del item ' + hijo.version.nombre + ' con código ' + hijo.codigo)
            for sucesor in sucesores:
                mensaje_error.append(
                    f'El item es el antecesor del item {sucesor.version.nombre} con codigo  {sucesor.codigo}')
            raise Exception(mensaje_error)

        self.estado = EstadoDeItem.ELIMINADO
        self.save()

    def add_padre(self, item, versionar=True):
        """
        Metodo del model Item que anhade a un item pasado como parametro a la
        lista que representa los padres del item, creando tambien una nueva version del item con esta nueva relacion.\n
        Parametros:\n
            -item: int, identificador unico del item a la cual se anhade a la liste de padres
        """
        if versionar:
            self.nueva_version()
        self.version.padres.add(item)

    def add_antecesor(self, item, versionar=True):
        """
        Metodo del model Item que anhade a un item pasado como parametro a la lista que representa los
        antecesores del item, creando tambien una nueva version del item con esta nueva relacion.\n
        Parametros:\n
            -item: int, identificador unico del item a la cual se anhade a la liste de antecesores
        """
        if versionar:
            self.nueva_version()
        self.version.antecesores.add(item)

    def solicitar_aprobacion(self):
        """
        Metodo que cambia el estado del Item de No Aprobado a A Aprobar.

        Requiere:
            Item debe estar en el estado NO_APROBADO
        Lanza:
            Exception: si el item no esta en el estado NO_APROBADO
        """
        if self.estado == EstadoDeItem.NO_APROBADO:
            self.estado = EstadoDeItem.A_APROBAR
            self.save()
        else:
            raise Exception(f"El item debe esta en el estado {EstadoDeItem.NO_APROBADO} para solicitar su Aprobacion")

    def aprobar(self):
        """
        Metodo que cambia el estado del Item de A Aprobar A Aprobado.
        El estado del item tiene que estar en A Aprobar.\n
        Requiere:
            Item debe estar en el estado A_APROBAR
        Lanza:
            Exception: si el item no esta en el estado A_APROBAR
        """
        if self.estado == EstadoDeItem.A_APROBAR:
            self.estado = EstadoDeItem.APROBADO
            self.save()
        else:
            raise Exception(f"El item debe esta en el estado {EstadoDeItem.A_APROBAR} para solicitar su Aprobacion")

    def desaprobar(self):
        """
        Metodo que cambia el estado de un item de 'Aprobado' a 'No Aprobado'.
        El metodo verifica primero el estado del item sea el adecuado y que este no tenga ninguna relacion
        (padre-hijo) para que se pueda desaprobar.\n
        Lanza:
            Exception: si el item esta relacionado con otro item o no esta con los estdos Aprobado o A Aprobar.
        """

        if self.estado == EstadoDeItem.APROBADO or self.estado == EstadoDeItem.A_APROBAR:
            hijos = self.get_hijos()
            if len(hijos) == 0:
                self.estado = EstadoDeItem.NO_APROBADO
                self.save()
            else:
                mensaje_error = []
                for hijo in hijos:
                    mensaje_error.append(
                        'El item es el padre del item ' + hijo.version.nombre + ' con código ' + hijo.codigo)

                raise Exception(mensaje_error)
        else:
            raise Exception("El item tiene que estar con estado Aprobado o A Aprobar para desaprobarlo")

    def eliminar_relacion(self, item):
        """
        Metodo de model Item que elimina la relacion entre dos item relacionados en la misma fase o fases adyacentes.
        Una relacion va a poder eliminarse siempre y cuando esta no cree ninguna inconsistencia. La eliminacion de una
        relacion implica una nueva version del item

        Parametros:
            - item: int, identificador unico del item, el cual se desea eliminar su relacion, es decir, de la lista de padres.

        Lanza:
            -Exception: si el los item no estan relacionados entre si, y si uno o ambos estan en una linea base

        """

        mensaje_error = []

        if self.estado != EstadoDeItem.EN_LINEA_BASE and item.estado != EstadoDeItem.EN_LINEA_BASE:
            if self.padres.filter(id=item.id).exists():
                if self.get_fase().fase_anterior is None or self.get_padres() > 1 or (
                        self.get_padres() == 1 and self.get_antecesores() >= 1):
                    self.nueva_version()
                    self.padres.remove(item)
                    return
                else:
                    mensaje_error.append(
                        'No se puede eliminar la relacion, pues el item dejara de ser trazable a la primera fase')
            elif self.antecesores.filter(id=item.id).exists():
                if self.get_fase().fase_anterior is None or self.get_antecesores() > 1 or (
                        self.get_antecesores() == 1 and self.get_padres() >= 1):
                    self.nueva_version()
                    self.antecesores.remove(item)
                    return
                else:
                    mensaje_error.append(
                        'No se puede eliminar la relacion, pues el item dejara de ser trazable a la primera fase')

            else:
                mensaje_error.append(
                    'Los item ' + self.version.nombre + ' y ' + item.version.nombre + ' no estan relacionados')
        else:
            if self.estado == EstadoDeItem.EN_LINEA_BASE:
                mensaje_error.append('El item ' + self.version.nombre + ' esta en una linea base')
            if item.estado == EstadoDeItem.EN_LINEA_BASE:
                mensaje_error.append('El item ' + item.version.nombre + ' esta en una linea base')

        raise Exception(mensaje_error)

    def puede_restaurarse(self, version):
        """
        Metodo de model Item que verifica si un item puede o no volver a una version pasada.
        Una version va a poder restaurarse si, el item esta en la primera fase, o si esta en una fase siguiente
        al menos tiene que tener un padre aprobado, o al menos un antecesor en linea base.\n
        Parametros:
            - version: int, identificador unico de la version a la cual se desea regresar

        Retorna:
            -True: Si el item puede restaurarse a una version anterior
            -False: Si el item no puede restaurarse a una version anterior
        """
        if self.get_fase().es_primera():
            return True
        else:
            return version.padres.filter(estado=EstadoDeItem.APROBADO).count() > 0 or \
                   version.antecesores.filter(estado=EstadoDeItem.EN_LINEA_BASE).count() > 0

    def restaurar(self, version):
        """
        Metodo de model Item que restaura la version de un item a una anterior, esta es espesificada como parametro.\n
        Parametros:
            - version: int, identificador unico de la version a la cual se desea regresar
        """
        nueva_version = VersionItem(nombre=version.nombre, descripcion=version.descripcion, peso=version.peso,
                                    item=version.item)
        nueva_version.version = self.get_numero_version() + 1
        nueva_version.save()
        for atributo in version.get_atributos_dinamicos():
            atributo.pk = None
            atributo.version = nueva_version
            atributo.save()

        for padre in version.padres.all():
            if padre.estado == EstadoDeItem.APROBADO:
                nueva_version.padres.add(padre)

        for antecesor in version.antecesores.all():
            if antecesor.estado == EstadoDeItem.EN_LINEA_BASE:
                nueva_version.antecesores.add(antecesor)

        self.version = nueva_version
        self.save()

    def solicitar_revision(self):
        # TODO: comentar y probar
        assert self.estado in [EstadoDeItem.APROBADO, EstadoDeItem.EN_LINEA_BASE]
        self.estado_anterior = self.estado
        self.estado = EstadoDeItem.EN_REVISION
        self.save()

    def solicitar_modificacion(self, usuario_encargado=None):
        # TODO: comentar y probar

        self.encargado_de_modificar = usuario_encargado
        self.estado = EstadoDeItem.A_MODIFICAR
        self.save()


class VersionItem(models.Model):
    """
    Modelo que representa una versión de un ítem junto a sus atributos versionables.

    - nombre: string
    - descripcion: string
    - peso: int
    - antecesores: lista[] items
    - padres: lista[] items
    - version: int

    """

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='version_item')
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=400)
    version = models.IntegerField()
    peso = models.IntegerField()
    # Relaciones
    antecesores = models.ManyToManyField('gestion_de_item.Item', related_name='sucesores')
    padres = models.ManyToManyField('gestion_de_item.Item', related_name='hijos')

    def get_atributos_dinamicos(self):
        atributos = list(self.atributoitemnumerico_set.all())
        atributos += list(self.atributoitemfecha_set.all())
        atributos += list(self.atributoitemcadena_set.all())
        atributos += list(self.atributoitembooleano_set.all())
        atributos += list(self.atributoitemarchivo_set.all())
        return atributos


class AtributoItemArchivo(models.Model):
    """
    Modelo que representa un atributo dinámico de tipo archivo de un item. Sus especificaciones estan dadas por la plantilla del attributo de tipo archivo del tipo de item correspondiente.

    """
    version = models.ForeignKey(VersionItem, on_delete=models.CASCADE)
    plantilla = models.ForeignKey('gestion_de_tipo_de_item.AtributoBinario', on_delete=models.CASCADE)
    valor = models.FileField(upload_to='items/', storage=gd_storage, null=True)
    archivo_temporal = models.FileField(upload_to='items/', null=True)

    def getTipoAtributo(self):
        return "Archivo"

    def archivo_pendiente(self):
        """
        Metodo que se encarga de determinar si el atributo tiene una subida de archivo a la nube pendiente o en proceso.
        Retorna "True" si el atributo "valor" esta vacío pero no el atributo "archivo_temporal", y "False" en caso
        contrario; esto se debe a que inicialmete el archivo es guardado en el atributo "archivo_temporal" y cuando
        el archivo esta completamente subido, pasa al atributo "valor"

        Retorna:
            Booleano
        """
        return self.archivo_temporal.name != ''

    def archivo_subido(self):
        # TODO: marcos, comentar
        return self.valor.name != ''


class AtributoItemBooleano(models.Model):
    """
        Modelo que representa un atributo dinámico de tipo booleano de un item. Sus especificaciones estan dadas por la plantilla del attributo de tipo booleano del tipo de item correspondiente.

    """

    version = models.ForeignKey(VersionItem, on_delete=models.CASCADE)
    plantilla = models.ForeignKey('gestion_de_tipo_de_item.AtributoBooleano', on_delete=models.CASCADE)
    valor = models.BooleanField(null=True)

    def getTipoAtributo(self):
        return "Booleano"


class AtributoItemFecha(models.Model):
    """
    Modelo que representa un atributo dinámico de tipo fecha de un item. Sus especificaciones estan dadas por la plantilla del attributo de tipo fecha del tipo de item correspondiente.

    """
    version = models.ForeignKey(VersionItem, on_delete=models.CASCADE)
    plantilla = models.ForeignKey('gestion_de_tipo_de_item.AtributoFecha', on_delete=models.CASCADE)
    valor = models.DateField(null=True)

    def getTipoAtributo(self):
        return "Fecha"


class AtributoItemNumerico(models.Model):
    """
        Modelo que representa un atributo dinámico de tipo númerico de un item. Sus especificaciones estan dadas por la plantilla del attributo de tipo númerico del tipo de item correspondiente.

    """
    version = models.ForeignKey(VersionItem, on_delete=models.CASCADE)
    plantilla = models.ForeignKey('gestion_de_tipo_de_item.AtributoNumerico', on_delete=models.CASCADE)
    valor = models.DecimalField(decimal_places=20, max_digits=40, null=True)

    def getTipoAtributo(self):
        return "Numerico"


class AtributoItemCadena(models.Model):
    """
        Modelo que representa un atributo dinámico de tipo cadena de un item. Sus especificaciones estan dadas por la plantilla del attributo de tipo cadena del tipo de item correspondiente.

    """
    version = models.ForeignKey(VersionItem, on_delete=models.CASCADE)
    plantilla = models.ForeignKey('gestion_de_tipo_de_item.AtributoCadena', on_delete=models.CASCADE)
    valor = models.CharField(max_length=500, null=True)

    def getTipoAtributo(self):
        return "Cadena"
