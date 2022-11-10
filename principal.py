#! /usr/bin/env python
import os, random, sys, math, pygame_menu

import pygame
from pygame.locals import *
from configuracion import *
from extras import *

from funcionesVACIAS import *


pygame.init()
surface = pygame.display.set_mode((800, 600))

DIFICULTAD = [1]
NOMBRE = ["Fulanito"]
LARGO = [5]

def seleccionarDificultad(sinUso ,valor):
    DIFICULTAD[0] = valor

def longitud(valor):
    if valor != '':
        int(valor) + 1
    LARGO[0] = valor

def cambiarNombre(nombre):
    NOMBRE[0] = nombre

def empezarJuego():
    main()

def recordsHistoricos():
    pygame.init()

    backgroundImage = pygame.image.load("imagenes/fondo.jpg").convert_alpha()
    screen = pygame.display.set_mode((ANCHO , ALTO))
    salir = False

    while salir != True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir = True

        defaultFont= pygame.font.Font(pygame_menu.font.FONT_NEVIS, TAMANNO_LETRA)
        screen.blit(backgroundImage,(0,0))

        record=[]
        records = open("records.txt","r")
        for linea in records.readlines():
            if "\n" in linea:
                record.append(linea[0:-1])
            else:
                record.append(linea)
        records.close()

        y=150
        ren1 = defaultFont.render("Puntajes Históricos", 1, COLOR_INCORRECTAS)
        screen.blit(ren1, (ANCHO//2-100, 100))

        k=0
        for i in range(len(record)-1,0,-1):
            k=k+1
            if k<=10:
                ren2 = defaultFont.render(record[i], 1, COLOR_CORRECTAS)
                screen.blit(ren2, (ANCHO//2-100, y))
                y=y+35

        pygame.display.update()


def mostrarPuntajes():
    recordsHistoricos()


menu = pygame_menu.Menu('La palabra escondida...', 800, 600, theme = pygame_menu.themes.THEME_DARK)
menu.add.text_input('Nombre: ', default='Fulanito', onchange=cambiarNombre)
menu.add.text_input('Longitud: ', default="4", onchange=longitud)
menu.add.selector('Modo: ', [('Colores', 1), ('Paises', 2), ('Avanzado', 3)], onchange=seleccionarDificultad)
menu.add.button('Jugar', empezarJuego)
menu.add.button('Puntajes Historicos', mostrarPuntajes)
menu.add.button('Salir', pygame_menu.events.EXIT)

#Funcion principal
def main():
    #Centrar la ventana y despues inicializar pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("sonidos/music.wav")
    #pygame.mixer.music.play(3)
    pygame.mixer.music.set_volume(NIVEL_VOLUMEN)

    #Preparar la ventana
    pygame.display.set_caption("La palabra escondida...")
    screen = pygame.display.set_mode((ANCHO, ALTO))

    #tiempo total del juego
    gameClock = pygame.time.Clock()
    totaltime = 0
    segundos = TIEMPO_MAX
    fps = FPS_inicial

    lemario = ""
    puntos = 0
    palabraUsuario = ""
    listaPalabrasDiccionario=[]
    ListaDePalabrasUsuario = []
    listaPuntos = []
    correctas = []
    incorrectas = []
    casi = []
    gano = False

    if DIFICULTAD[0] == 1:
        lemario = "lemarioColores.txt"
    elif DIFICULTAD[0] == 2:
        lemario = "lemarioPaises.txt"
    elif DIFICULTAD[0] == 3:
        lemario = "lemarioAvanzado.txt"


    archivo = open(lemario,"r")
    #lectura del diccionario
    lectura(archivo, listaPalabrasDiccionario, LARGO[0])
    print(lemario)

    #elige una al azar
    palabraCorrecta = nuevaPalabra(listaPalabrasDiccionario)

    intentos = 5
    dibujar(screen, ListaDePalabrasUsuario, palabraUsuario, puntos, intentos, segundos, gano, correctas, incorrectas, casi)
    print(palabraCorrecta)

    while segundos > fps/1000 and intentos > 0 and not gano:
    # 1 frame cada 1/fps segundos
        gameClock.tick(fps)
        totaltime += gameClock.get_time()

        if True:
            fps = 3

        #Buscar la tecla apretada del modulo de eventos de pygame
        for e in pygame.event.get():

            #QUIT es apretar la X en la ventana
            if e.type == QUIT:
                pygame.quit()
                return()

            #Ver si fue apretada alguna tecla
            if e.type == KEYDOWN:
                letra = dameLetraApretada(e.key)
                palabraUsuario += letra #es la palabra que escribe el usuario
                if e.key == K_BACKSPACE:
                    palabraUsuario = palabraUsuario[0:len(palabraUsuario)-1]
                if e.key == K_RETURN:
                    #falta hacer un control para que sea una palabra de la longitud deseada
                    #falta controlar que la palabra este en el diccionario
                    palabraUsuario += "\n"
                    if buscarPalabra(listaPalabrasDiccionario, palabraUsuario) == True and not buscarPalabra(ListaDePalabrasUsuario, palabraUsuario) and len(palabraUsuario) == (int(LARGO)+1):
                        revision(palabraCorrecta, palabraUsuario, correctas, incorrectas, casi)
                        if len(correctas) != 0 and len(incorrectas) == 0 and len(casi) == 0:
                            #Limpiar pantalla anterior
                            screen.fill((0,0,255))
                            puntos = (len(correctas)*50)
                            gano = True
                        else:
                            puntos = (len(correctas)*50) + (len(casi)*25) - (len(incorrectas)* 10)
                            palabraUsuarioNew = palabraUsuario.replace("\n","")
                            ListaDePalabrasUsuario.append(palabraUsuarioNew)
                            palabraUsuario = ""
                            intentos -= 1
                    else:
                        palabraUsuarioNew = palabraUsuario.replace("\n","")
                        ListaDePalabrasUsuario.append(palabraUsuarioNew)
                        palabraUsuario = ""
                        intentos -= 1
                        


        segundos = TIEMPO_MAX - pygame.time.get_ticks()/1000

        #Limpiar pantalla anterior
        screen.fill(COLOR_FONDO)

        #Dibujar de nuevo todo
        dibujar(screen, ListaDePalabrasUsuario, palabraUsuario, puntos, intentos, segundos, gano, correctas, incorrectas, casi)

        pygame.display.flip()

    #Fin del juego
   
    if gano:
        defaultFont= pygame.font.Font(pygame_menu.font.FONT_NEVIS, TAMANNO_LETRA)
        screen.fill((0,0,0))
        screen.blit(defaultFont.render("HAS GANADO, LA PALABRA" + palabraCorrecta + "ES LA CORRECTA!", 1, COLOR_TEXTO), (190, 570))
        pygame.display.flip()


    """while 1:
        #Esperar el QUIT del usuario
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return"""

    archivo.close()
#Programa Principal ejecuta Main
if __name__ == "__main__":
    menu.mainloop(surface)
