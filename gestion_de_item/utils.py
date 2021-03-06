import json

from django import db
from gdstorage.storage import GoogleDriveStorage

import gestion_de_tipo_de_item.models as modelos
from gestion_de_item.forms import AtributoItemNumericoForm, AtributoItemBooleanoForm, AtributoItemFechaForm, \
    AtributoItemCadenaForm, AtributoItemArchivoForm
from gestion_de_item.models import AtributoItemArchivo, Item
from gestion_de_proyecto.models import Proyecto


def get_atributos_forms(tipo_de_item, request, instance=None):
    """
    Función utilitaria que construye una lista de forms para cada atributo del item asociado a su tipo de item.

    Argumentos:
        - tipo_de_item: TipoDeItem
        - request: HttpRequest

    Retorna
        atributo_forms: lista de forms adecuados para cada atributo.
   """

    atributo_forms = []
    counter = 0
    for atributo in tipo_de_item.get_atributos():
        counter = counter + 1
        if type(atributo) == modelos.AtributoCadena:
            atributo_forms.append(
                AtributoItemCadenaForm(request.POST or None, plantilla=atributo, counter=counter))
        elif type(atributo) == modelos.AtributoNumerico:
            atributo_forms.append(
                AtributoItemNumericoForm(request.POST or None, plantilla=atributo, counter=counter))
        elif type(atributo) == modelos.AtributoBinario:
            atributo_forms.append(
                AtributoItemArchivoForm(request.POST or None, request.FILES, plantilla=atributo, counter=counter))
        elif type(atributo) == modelos.AtributoFecha:
            atributo_forms.append(
                AtributoItemFechaForm(request.POST or None, plantilla=atributo, counter=counter))
        elif type(atributo) == modelos.AtributoBooleano:
            atributo_forms.append(
                AtributoItemBooleanoForm(request.POST or None, plantilla=atributo, counter=counter))
    return atributo_forms


def hay_ciclo(padre, hijo):
    """
    Funcion auxiliar del metodo "clean_padre", para determinar si al formar una relacion entre padre e hijo
    esta no va a formar un ciclo. El algoritmo utilizado es DFS iterativo.\n
    Argumentos: \n
        - padre: item de una fase\n
        - hijo: item de la misma fase\n
    Retorna: \n
        - True: si ya hay un camino directo o indirecto que conecta padre con hijo\n
        - False: si no hay un camnino que concecte padre con hijo\n
    """
    stack = []
    visitado = set()
    stack.append(padre)
    visitado.add(padre)
    while len(stack) != 0:
        item = stack.pop()
        for padre in item.get_padres():
            if padre not in visitado:
                stack.append(padre)
                visitado.add(padre)
    return hijo in visitado


def upload_and_save_file_item(gd_storage, atributo_id, file, proyecto, fase, item):
    """
    Funcion utilitaria que se encarga de subir al repositorio de GoogleDrive la lista de archivos de los atributos
    dinamicos de un item, una vez subido cada arcivo se guardará el enlace de descarga en cada atributo.

    Argumentos:
        - gd_storage: Objeto que se comunuca con GDrive\n
        - atributo_id: Lista de ids de atributos e tipo aarchivo\n
        - file: Lista de archivos asociados a cada atributo\n
        - proyecto: Proyecto en el que se ecuentra el item\n
        - fase: Fase del Proyecto en el que se encuentra el item\n
        - item: Item que posee los atributos\n

    Retorna:
        - Void
    """
    db.close_old_connections()

    for i in range(0, len(atributo_id)):
        atributo = AtributoItemArchivo.objects.get(id=atributo_id[i])
        path = f'/PROY-{proyecto.nombre}-ID{proyecto.id}_/' \
               f'FASE-{fase.nombre}-ID{fase.id}_/ITEM-{item}_/ATRIB-{atributo.plantilla.nombre}_/' \
               f'VERS{atributo.version.version}_/FILENAME-{file[i].name}'

        gd_storage.save(path, file[i])
        atributo.valor = gd_storage.url(path)

        atributo.save()


def upload_and_save_file_item_2(atributo, file, proyecto, fase, item):
    gd_storage = GoogleDriveStorage()
    path = f'/PROY-{proyecto.nombre}-ID{proyecto.id}_/FASE-{fase.nombre}-ID{fase.id}_/ITEM-{item}_/ATRIB-{atributo.plantilla.nombre}_/VERS{atributo.version.version}_/FILENAME-{file.name}'
    print(path)
    gd_storage.save(path, file)
    return gd_storage.url(path)


def trazar_item(proyecto: Proyecto, item: Item):
    """
    | Funcion utilitaria que toma un item de un proyecto y construye una representación
    | del grafo conformado por el item, sus antecesores y padres, directos e indirectos.
    | Este grafo es presentado en un formato JSON.

    Argumentos:
        - proyecto: Proyecto
        - item: Item

    Retorna:
        - JSON
    """
    items = [item]
    items_visitados = set()
    queue = []
    for padre in item.get_padres():
        queue.append([padre, {'sucesores': False, 'antecesores': True, 'hijos': False, 'padres': True}])

    for antecesor in item.get_antecesores():
        queue.append([antecesor, {'sucesores': False, 'antecesores': True, 'hijos': False, 'padres': True}])

    for hijo in item.get_hijos():
        queue.append([hijo, {'sucesores': True, 'antecesores': False, 'hijos': True, 'padres': False}])

    for sucesor in item.get_sucesores():
        queue.append([sucesor, {'sucesores': True, 'antecesores': False, 'hijos': True, 'padres': False}])

    items_visitados.add(item.id)
    while len(queue) > 0:
        [item, dependencias] = queue.pop()
        if item.id in items_visitados:
            continue
        items_visitados.add(item.id)
        items.append(item)
        if dependencias['padres']:
            for padre in item.get_padres():
                if padre.id not in items_visitados:
                    queue.append([padre, dependencias])

        if dependencias['antecesores']:
            for antecesor in item.get_antecesores():
                if antecesor.id not in items_visitados:
                    queue.append([antecesor, dependencias])

        if dependencias['hijos']:
            for hijo in item.get_hijos():
                if hijo.id not in items_visitados:
                    queue.append([hijo, dependencias])

        if dependencias['sucesores']:
            for sucesor in item.get_sucesores():
                if sucesor.id not in items_visitados:
                    queue.append([sucesor, dependencias])

    return json.dumps([
        {
            "fase": fase.nombre,
            "items": [
                {
                    "codigo": item.codigo,
                    "data": {
                        "nombre": str(item),
                        "tipoDeItem": item.tipo_de_item.nombre,
                        "peso": item.get_peso(),
                        "estado": item.estado
                    },
                    "hijos": [hijo.codigo for hijo in item.get_hijos() if hijo.id in items_visitados],
                    "sucesores": [sucesor.codigo for sucesor in item.get_sucesores() if sucesor.id in items_visitados]
                }
                for item in items if item.get_fase().id == fase.id
            ]
        }
        for fase in proyecto.get_fases()
    ],sort_keys=True)
