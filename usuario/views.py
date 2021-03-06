from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.models import Permission

from gestion_de_proyecto.models import Proyecto
from roles_de_proyecto.models import RolDeProyecto
from roles_de_sistema.models import RolDeSistema
from .forms import AsignarRolDeSistemaForm, ConfigCloudForm
from .models import Usuario
from .tasks import mail_for_new_rol
from gestion_de_reportes.utils import make_report


# Create your views here.
@login_required
@permission_required('roles_de_sistema.pu_acceder_sistema', login_url='sin_permiso')
def usuarios_view(request):
    """
    Vista que muestra la lista de usuarios del sistema.

    Require los siguientes permisos de sistema:
        Visualizar usuarios del sistema.
    """
    lista_usuario = list(User.objects.all())
    contexto = {'lista_usuario': lista_usuario, 'user': request.user,
                'breadcrumb': {'pagina_actual': 'Usuarios',
                               'links': [{'nombre': 'Panel de Administracion', 'url': reverse('panel_de_control')}]},
                }
    return render(request, 'usuario/usuarios.html', context=contexto)

@login_required
@permission_required('roles_de_sistema.pu_acceder_sistema', login_url='sin_permiso')
@permission_required('roles_de_sistema.ps_ver_usuarios', login_url='sin_permiso')
def usuario_view(request, usuario_id):
    """
    Vista que permite ver la información publica de un usuario. \n
    En caso de intentar acceder a un usuario no existente se muestra una pantalla de error

    Requiere los siguientes permisos del sistema:
        Visualizar usuarios del sistema
    """
    user = Usuario.objects.get(id=request.user.id)
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    grupo = None
    if request.method == 'POST':
        usuario.desasignar_rol_a_usuario()
    else:
        for g in usuario.groups.all():
            grupo = g.name
    contexto = {'usuario': usuario, 'user': user, 'rs_asignado': usuario.tiene_rs(), 'nombre_rs': grupo,
                'breadcrumb': {'pagina_actual': usuario.get_full_name(),
                               'links': [{'nombre': 'Usuarios', 'url': reverse('usuarios')}]}}
    return render(request, 'usuario/usuario.html', context=contexto)


@login_required
@permission_required('roles_de_sistema.pu_acceder_sistema', login_url='sin_permiso')
@permission_required('roles_de_sistema.pa_asignar_rs', login_url='sin_permiso')
def usuario_asignar_rol_view(request, usuario_id):
    """
    Vista que permite asignar un rol a un usuario y enviar un mensaje al usuario en caso exitoso\n
    En caso de intentar acceder a un usuario no existente se muestra una pantalla de error

    Requiere los siguientes permisos del sistema:
        Asignar Roles de Sistema
    """
    usuario = get_object_or_404(Usuario, pk=usuario_id)

    if request.method == 'POST':
        form = AsignarRolDeSistemaForm(request.POST, usuario=usuario)
        if form.is_valid():
            usuario.asignar_rol_a_usuario(form.cleaned_data.get('Rol'))
            mail_for_new_rol.delay(usuario.id)
            return redirect('perfil_de_usuario', usuario_id=usuario.id)
        else:
            messages.error(request, "No se pudo asignar Rol de Sistema")
    else:
        form = AsignarRolDeSistemaForm(usuario=usuario)

    contexto = {'usuario': usuario, 'user': request.user, 'form': form}
    return render(request, 'usuario/asignar_rs.html', contexto)


@login_required
@permission_required('roles_de_sistema.pu_acceder_sistema', login_url='sin_permiso')
def panel_de_administracion_view(request):
    """
    Vista que muestra el Panel de Administración del Sistema desde el cual el Administrador puede
    realizar operaciones como Crear Nuevos Proyectos, Visualizar los Usuarios del Sistema,etc.

    Así también, aquellos usuarios con un Rol de Sistema que cuente con algún permiso especial de visualización
    podrá visualizar los usuarios del Sistema o los Usuarios del Sistema.

    Argumentos:
        - request: HttpRequest, petición recibida por el servidor.

    Retorna:
        - HttpResponse.
    """
    user = Usuario.objects.get(id=request.user.id)
    contexto = {'user': user,
                'permisos': user.get_permisos_list(),
                'usuarios': Usuario.objects.all().filter(is_superuser=False),
                'proyectos': Proyecto.objects.all(),
                'roles_de_proyecto': RolDeProyecto.objects.all(),
                'roles_de_sistema': RolDeSistema.objects.all(),
                'breadcrumb': {'links': [],
                               'pagina_actual': 'Panel de Administracion'}
                }
    return render(request, 'usuario/panel_de_administracion.html', contexto)


@login_required
@permission_required('roles_de_sistema.pu_acceder_sistema', login_url='sin_permiso')
@permission_required('roles_de_sistema.pa_desasignar_rs', login_url='sin_permiso')
def desasignar_rol_de_sistema_view(request, usuario_id):
    """
    Vista que que se encarga de Desasignar un Rol de Sistema a un Usuario si este no se encuantra en ningun proyecto

    Argumentos:
        request: HttpRequest \n
        usuario_id: int, identificador unico del Usuario

    Retorna:
        HttpResponse
    """
    usuario = get_object_or_404(Usuario, pk=usuario_id)

    contexto = {'user': request.user, 'usuario': usuario, 'en_proyecto': usuario.get_proyectos() != [],
                'rol': usuario.get_rol_de_sistema(),
                'breadcrumb': {'pagina_actual': 'Desasignar RS',
                               'links': [{'nombre': 'Usuarios', 'url': reverse('usuarios')},
                                         {'nombre': usuario.get_full_name(), 'url': reverse('perfil_de_usuario',
                                                                                            args=(usuario_id,))}]}}

    grupo = None
    if request.method == 'POST':
        usuario.desasignar_rol_a_usuario()
        return redirect('perfil_de_usuario', usuario_id=usuario_id)

    return render(request, 'usuario/desasignar_rs.html', contexto)


@login_required
@permission_required('roles_de_sistema.pu_acceder_sistema', login_url='sin_permiso')
@permission_required('roles_de_sistema.pa_config_cloud', login_url='sin_permiso')
def configurar_cloud_view(request):
    if request.method == 'POST':
        form = ConfigCloudForm(request.POST)
        if form.is_valid() and len(form.cleaned_data.get('credenciales')) > 0:
            json = open(settings.GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE, 'w')

            json.write(form.cleaned_data.get('Json de Configuración del Cloud').replace('\n', '\\n'))
            json.close()
            print(form.cleaned_data.get('Json de Configuración del Cloud'))
        return redirect('panel_de_control')
    json = open(settings.GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE, 'r').read().replace('\n', '\\n')
    form = ConfigCloudForm()
    contexto = {'form': form, 'jsontext': json, 'breadcrumb': {'pagina_actual': 'Configuracion Cloud',
                                                               'links': [{'nombre': 'Panel de Administracion',
                                                                          'url': reverse('panel_de_control')}]}}

    return render(request, 'usuario/configuracion_cloud.html', contexto)


@login_required()
@permission_required('roles_de_sistema.pu_acceder_sistema', login_url='sin_permiso')
def mi_perfil_view(request):
    """
    Vista que muestra a un usuario sus datos dentro del ststema: nombre completo, correo, rol de sistema, permisos de sistema y proyectos en los que participa.

    Argumentos:
        - request: HttpRequest

    Retorna:
        - HttpResponse
    """
    user = request.user
    user = get_object_or_404(Usuario, id=user.id)

    permisos = [Permission.objects.get(codename=x) for x in user.get_permisos_list()]
    proyectos_activos = user.get_proyectos_activos()
    proyectos_no_activos = []
    proyectos_no_activos = proyectos_no_activos + user.get_proyectos(estado='Finalizado')
    proyectos_no_activos = proyectos_no_activos + user.get_proyectos(estado='Cancelado')
    roles_activos = []
    roles_no_activos = []
    for proyecto in proyectos_activos:
        if proyecto.gerente != user:
            roles_activos.append(proyecto.get_participante(user).rol.nombre)
        else:
            roles_activos.append('Gerente')
    proyectos_activos = zip(proyectos_activos, roles_activos)
    for proyecto in proyectos_no_activos:
        if proyecto.gerente != user:
            roles_no_activos.append(proyecto.get_participante(user).rol.nombre)
        else:
            roles_no_activos.append('Gerente')
    proyectos_no_activos = zip(proyectos_no_activos, roles_no_activos)

    contexto = {'user': user, 'permisos': permisos, 'proyectos_activos': proyectos_activos,
                'proyectos_no_activos': proyectos_no_activos}
    return render(request, 'usuario/mi_perfil.html', context=contexto)


@login_required
@permission_required('roles_de_sistema.pu_acceder_sistema', login_url='sin_permiso')
@permission_required('roles_de_sistema.ps_ver_usuarios', login_url='sin_permiso')
def usuarios_reporte_view(request):
    """
    Vista que muestra el reporte de la lista de usuarios del sistema.

    Require los siguientes permisos de sistema:
        Visualizar usuarios del sistema.
    """
    lista_usuarios = list(Usuario.objects.all())
    contexto = {'lista_usuarios': lista_usuarios}
    return make_report('reportes/usuarios_reporte.html', context=contexto)
