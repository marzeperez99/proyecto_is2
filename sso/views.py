from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout

from gestion_de_proyecto.models import Proyecto
from usuario.models import Usuario


@login_required
@permission_required('pu_acceder_sistema', login_url='sin_permiso')
def index_view(request):
    """Esta función se encarga de, una vez que el usuario haya iniciado sesión, redirigirla al template que muestra el menú pricipal

    Args:
        request (HttpRequest Object): respuesta del request

    Retorna:
        El HttpResponse de la Vista a mostrarse
    """
    contexto = {'user': request.user, 'proyectos': Proyecto.objects.all()}
    return render(request, 'sso/index.html', context=contexto)


# Create your views here.

def login_view(request):
    """
    Vista que muestra la pantalla de inicio de sesión. Si el usuario ya ha iniciado sesión, este es redirigido a la pantalla principal del sistema.

    Args:
        request (HttpRequest)

    Retorna:
        HttpResponse
    """
    contexto = None
    if (request.user.is_authenticated):
        print(request.user.first_name)
        return redirect('index')
    else:

        return render(request, 'sso/login.html', context=contexto)


@login_required
def logout_view(request):
    """
    Vista que se encarga del cierre de sesion del usuario. Una vez echo esto redirige a la pantalla de inicio de sesion

    Args:
        request (HttpRequest)

    Retorna:
        HttpResponse
    """
    logout(request)
    return redirect('login')


def sin_permiso(request):
    """
    Vista que se encarga de avisarle al usuario que no posee permisos suficientes para lo que desea realizar
    """
    return render(request, 'sso/sin_acceso.html')
