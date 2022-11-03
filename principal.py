#! /usr/bin/env python
import os, random, sys, math
from turtle import back

import pygame
from pygame.locals import *
from configuracion import *
from extras import *
from pygame.locals import * 

from funcionesVACIAS import *

#Funcion principal
def main():
    #Centrar la ventana y despues inicializar pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("sonidos/music.wav")
    #pygame.mixer.music.play(3)

    #Preparar la ventana
    pygame.display.set_caption("La palabra escondida...")
    screen = pygame.display.set_mode((ANCHO, ALTO))
    background = pygame.image.load("imagenes/bkImage.png")

    #tiempo total del juego
    gameClock = pygame.time.Clock()
    totaltime = 0
    segundos = TIEMPO_MAX
    fps = FPS_inicial

    puntos = 0
    palabraUsuario = ""
    listaPalabrasDiccionario=[]
    ListaDePalabrasUsuario = []
    correctas = []
    incorrectas = []
    casi = []
    gano = False

    

    archivo= open("lemario.txt","r")
    #lectura del diccionario
    lectura(archivo, listaPalabrasDiccionario, LARGO)

    #elige una al azar
    palabraCorrecta= nuevaPalabra(listaPalabrasDiccionario)

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
                        #Reviso con la funcion buscarPalabra si esta en el diccionario
                    palabraUsuario += '\n'
                    if buscarPalabra(listaPalabrasDiccionario, palabraUsuario) == True and len(palabraUsuario) == LARGO:
                        #revisionLetras(letrasCorrecta, letrasUsuario, correctas, incorrectas)
                        gano = True
                    else:
                        msj = "Debes introducir una palabra que este dentro del diccionario y contenga 4 caracteres!"
                        palabraUsuarioNew = palabraUsuario.replace("\n","",)
                        ListaDePalabrasUsuario.append(palabraUsuarioNew)
                        palabraUsuario = ""
                        intentos -= 1
                        dibujarAlerta(screen,msj)

                            
                        

        segundos = TIEMPO_MAX #- pygame.time.get_ticks()/1000

        #Limpiar pantalla anterior
        screen.blit(background, (0,0))

        #Dibujar de nuevo todo
        dibujar(screen, ListaDePalabrasUsuario, palabraUsuario, puntos, intentos, segundos, gano, correctas, incorrectas, casi)

        pygame.display.flip()

    while 1:
        #Esperar el QUIT del usuario
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return

    archivo.close()

#Programa Principal ejecuta Main
if __name__ == "__main__":
    main()
