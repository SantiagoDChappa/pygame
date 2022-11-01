from operator import truediv
from principal import *
from configuracion import *
import random
import math



def nuevaPalabra(lista):
    nuevaPalabra = lista[random.randint(0,len(lista))]
    return nuevaPalabra

def lectura(archivo, salida, largo):
    archivoPalabras = archivo.readlines()
    for palabra in archivoPalabras:
        if len(palabra) == largo:
            salida.append(palabra)
    return salida

def buscarPalabra(lista, palabraUsuario):
    for palabra in lista:
        if palabra == palabraUsuario:
            return True
    return False

def buscarLetra(palabra, elemento):
    for letra in palabra:
        if letra == elemento:
            return letra

def desestructurarPalabra(palabra):
    palabraDesarmada = []
    for letra in palabra:
        palabraDesarmada += letra
    return palabraDesarmada

def revision(palabraCorrecta, palabraUsuario, correctas, incorrectas, casi):
    palabraCorrecta = palabraCorrecta.replace('\n',"").lower()
    palabraUsuario = palabraUsuario.replace('\n',"").lower()
    for letra in palabraCorrecta:
        letraVerificar = buscarLetra(palabraUsuario, letra)
        if letraVerificar != "" and palabraCorrecta.index(letra) == palabraUsuario.index(letra) and palabraUsuario.index(letra) != -1:
            correctas.append(letra)
            palabraCorrecta = palabraCorrecta.replace(letra, " ",1)


#def revisionLetras(palabraCorrecta, palabraUser, correctas, incorrectas, casi):
    #for caracteres in palabraCorrecta:
     #   for caracteresUser in palabraUser:
      #      if caracteres == caracteresUser and palabraCorrecta.index(caracteres) == palabraUser.index(caracteresUser):
       #         correctas += caracteresUser
        #    elif caracteres == caracteresUser and palabraCorrecta.index(caracteres) != palabraUser.index(caracteresUser):
         #       casi += caracteresUser
          #  else:
           #     incorrectas += caracteresUser
    #return (correctas,casi,incorrectas)