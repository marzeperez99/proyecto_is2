from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
# Create your models here.


class Usuario(User):
    class Meta:
        proxy = True

    #metodo de prueba
    def introducir(self):
        return "Hola, mi nombre es {}\n".format(self.first_name)
