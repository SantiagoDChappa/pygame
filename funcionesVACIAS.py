from operator import truediv
from principal import *
from configuracion import *
import random
import math

def nuevaPalabra(lista):
    cont = len(lista)
    nuevaPalabra = lista[random.randrange(cont)]
    return nuevaPalabra

def lectura(archivo, salida, largo):
    archivoPalabras = archivo.readlines()
    for palabra in archivoPalabras:
        if len(palabra) == largo:
            salida.append(palabra)
    return salida

def lecturaSinLargo(archivo, salida):
    archivoPalabras = archivo.readlines()
    for palabra in archivoPalabras:
        salida.append(palabra)
    return salida

def buscarPalabra(lista, palabraUsuario):
    if "\n" in palabraUsuario:
        palabraUsuario = palabraUsuario.replace("\n","")
    for palabra in lista:
        palabraNew = palabra.replace("\n","")
        if palabraNew == palabraUsuario:
            return True
    return False

def contarPalabras():
    records = open("records.txt","r")
    contador = 0
    for linea in records.readlines():
        if "Player" in linea:
            contador += 1
    records.close()
    return contador
    

def revision(palabraCorrecta, palabraUsuario, correctas, incorrectas, casi):
    palabraCorrecta = palabraCorrecta.replace('\n',"").lower()
    palabraUsuario = palabraUsuario.replace('\n',"").lower()
    for i,letra in enumerate(palabraUsuario):
        if palabraCorrecta[i] == palabraUsuario[i]:
            if letra in casi:
                casi.pop(casi.index(letra))
                correctas.append(letra)
            else:
                correctas.append(letra)
        elif letra in palabraCorrecta:
            casi.append(letra) 
        else:
            incorrectas.append(letra)
    return correctas,casi,incorrectas