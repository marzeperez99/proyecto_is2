from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Usuario


# Create your views here.
@login_required
def usuarios_view(request):
    lista_usuario = list(Usuario.objects.all())
    contexto = {'lista_usuario': lista_usuario, 'user': request.user}
    return render(request, 'usuario/usuarios.html', context=contexto)


@login_required
def usuario_view(request, id_usuario):
    usuario = get_object_or_404(Usuario, pk=id_usuario)
    contexto = {'usuario': usuario, 'user': request.user}
    return render(request, 'usuario/usuario.html', context=contexto)
