#! /usr/bin/env python
import os, random, sys, math, pygame_menu

import pygame
from pygame.locals import *
from configuracion import *
from extras import *
from fireworkWin import *
from funcionesVACIAS import *
from matrix import *

pygame.init()
surface = pygame.display.set_mode((800, 600))

DIFICULTAD = [1]
NOMBRE = ["Fulanito"]
LARGO = [5]

def seleccionarDificultad(sinUso ,valor):
    DIFICULTAD[0] = valor

def longitud(valor):
    if valor != '':
        valor = int(valor) + 1
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
                #indice = linea.index(":")
                #if letra[i + 1] != " "
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

def fireworkWin(screen):

    fireworks = [Firework() for i in range(1)]  # create the first fireworks
    running = True
    clock = pygame.time.Clock()
    font = pygame.font.Font(pygame.font.get_default_font(), TAMANNO_LETRA) # Fuente
    text = font.render("FELICIDADES, HAS ACERTADO LA PALABRA CORRECTA!", True, (255,255,255)) # Texto
    center_x = (ANCHO // 2) - (text.get_width() // 2) # posicion text
    center_y = (ALTO // 2) - (text.get_height() // 2)
   
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    fireworks.append(Firework())
                elif event.key == pygame.K_2:
                    for i in range(10):
                        fireworks.append(Firework())
        screen.fill(BACKGROUND_COLOR)  # draw background
        screen.blit(text, [center_x, center_y])

        if randint(0, 70) == 1:  # create new firework
            fireworks.append(Firework())
        
        update(screen, fireworks, trails)

def fondoMatrix(palabra):
    class Symbol:
        def __init__(self, x, y, speed):
            self.x, self.y = x, y
            self.speed = speed
            self.value = choice(green_katakana)
            self.interval = randrange(5, 30)

        def draw(self, color):
            frames = pg.time.get_ticks()
            if not frames % self.interval:
                self.value = choice(green_katakana if color == 'green' else lightgreen_katakana)
            self.y = self.y + self.speed if self.y < ALTO else -FONT_SIZE
            surface.blit(self.value, (self.x, self.y))


    class SymbolColumn:
        def __init__(self, x, y):
            self.column_height = randrange(8, 24)
            self.speed = randrange(3, 7)
            self.symbols = [Symbol(x, i, self.speed) for i in range(y, y - FONT_SIZE * self.column_height, -FONT_SIZE)]

        def draw(self):
            [symbol.draw('green') if i else symbol.draw('lightgreen') for i, symbol in enumerate(self.symbols)]
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    RES = ANCHO, ALTO
    FONT_SIZE = 40
    alpha_value = 0

    pg.init()
    screen = pg.display.set_mode(RES)
    surface = pg.Surface(RES)
    surface.set_alpha(alpha_value)
    clock = pg.time.Clock()

    palabraNew = palabra.replace('\n', '')
    frase = "Has perdido, la palabra correcta era " + palabraNew.upper()
    katakana = [chr(int('0x30a0', 16) + i) for i in range(96)]
    font = pg.font.Font('font/ms mincho.ttf', FONT_SIZE, bold=True)
    green_katakana = [font.render(char, True, (40, randrange(160, 256), 40)) for char in katakana]
    lightgreen_katakana = [font.render(char, True, pg.Color('lightgreen')) for char in katakana]

    symbol_columns = [SymbolColumn(x, randrange(-ALTO, 0)) for x in range(0, ANCHO, FONT_SIZE)]

    while True:
        font = pygame.font.Font(pygame.font.get_default_font(), 30) # Fuente
        text = font.render(frase, True, (255,255,255)) # Texto
        center_x = (ANCHO // 2) - (text.get_width() // 2) # posicion text
        center_y = (ALTO // 2) - (text.get_height() // 2)
        screen.blit(surface, (0, 0))
        surface.fill(pg.Color('black'))
        screen.blit(text, [center_x, center_y])

        [symbol_column.draw() for symbol_column in symbol_columns]

        if not pg.time.get_ticks() % 20 and alpha_value < 170:
            alpha_value += 6
            surface.set_alpha(alpha_value)

        [exit() for i in pg.event.get() if i.type == pg.QUIT]
        pg.display.flip()
        clock.tick(60)

def game_over(screen, palabra):
    game = False
    
    screen.fill((91,0,0))
    while game != True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = True 
        fondoMatrix(palabra)
            
def porTiempo(screen, puntos):
    font = pygame.font.Font(pygame.font.get_default_font(), TAMANNO_LETRA) # Fuente
    text = font.render("FELICIDADES, HAS OBTENIDO " + str(puntos) + "PUNTOS!", True, (255,255,255)) # Texto
    center_x = (ANCHO // 2) - (text.get_width() // 2) # posicion text
    center_y = (ALTO // 2) - (text.get_height() // 2)
    game = False
    
    while game != True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = True 
        screen.fill(BACKGROUND_COLOR)
        screen.blit(text, [center_x, center_y])

menu = pygame_menu.Menu('La palabra escondida...', 800, 600, theme = pygame_menu.themes.THEME_DARK)
menu.add.text_input('Nombre: ', default='Fulanito', onchange=cambiarNombre)
menu.add.text_input('Longitud: ', default="4", onchange=longitud)
menu.add.selector('Modo: ', [('Facil = Colores', 1), ('Intermedio = Paises', 2), ('Dificil = Avanzado', 3), ("Extra = Solo por Tiempo", 4)], onchange=seleccionarDificultad)
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
    listaDePalabrasUsuario = []
    listaPuntos = []
    correctas = []
    incorrectas = []
    casi = []
    listRecord = []
    gano = False
    msjRepetido = False
    gameOver = False

    if DIFICULTAD[0] == 1:
        lemario = "lemarioColores.txt"
    elif DIFICULTAD[0] == 2:
        lemario = "lemarioPaises.txt"
    elif DIFICULTAD[0] == 3 or DIFICULTAD[0] == 4:
        lemario = "lemarioAvanzado.txt"

    if DIFICULTAD[0] == 4:
        archivo = open(lemario,"r")
        #lectura del diccionario
        lecturaSinLargo(archivo, listaPalabrasDiccionario)
        #elige una al azar
        palabraCorrecta = nuevaPalabra(listaPalabrasDiccionario)

        dibujarSinIntentos(screen, listaDePalabrasUsuario, palabraUsuario, palabraCorrecta, puntos, segundos, gano, correctas, incorrectas, casi)
        print(palabraCorrecta)

        while segundos > fps/1000:
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
                        palabraUsuario += "\n"
                        #Verifica si la palabra del usuario esta en el lemario y cumple con la longitud
                        if buscarPalabra(listaPalabrasDiccionario, palabraUsuario) == True and len(palabraUsuario) == len(palabraCorrecta):
                            # Verifica si la palabra del usuario no es repetida, es decir, ya ingreso en algun intento anterior
                            if listaDePalabrasUsuario == [] or not buscarPalabra(listaDePalabrasUsuario, palabraUsuario):
                                #Revisa las letras del usuario
                                revision(palabraCorrecta, palabraUsuario, correctas, incorrectas, casi)
                                if palabraUsuario == palabraCorrecta:
                                    puntos = (len(correctas)*50)
                                    palabraCorrecta = nuevaPalabra(listaPalabrasDiccionario)
                                    palabraUsuarioNew = palabraUsuario.replace("\n","")
                                    listaDePalabrasUsuario.append(palabraUsuarioNew)
                                    palabraUsuario = ""
                                    correctas = []
                                    casi = []
                                    incorrectas = []
                                    print(palabraCorrecta)
                                else:
                                    puntos = (len(correctas)*50) + (len(casi)*25) - (len(incorrectas)* 10)
                                    palabraUsuarioNew = palabraUsuario.replace("\n","")
                                    listaDePalabrasUsuario.append(palabraUsuarioNew)
                                    palabraUsuario = ""
                                    print(palabraCorrecta)
                            else:
                                puntos -= 15 
                                palabraUsuarioNew = palabraUsuario.replace("\n","")
                                listaDePalabrasUsuario.append(palabraUsuarioNew)
                                palabraUsuario = ""
                                print(palabraCorrecta)
                        else:
                            puntos -= 15 
                            palabraUsuarioNew = palabraUsuario.replace("\n","")
                            listaDePalabrasUsuario.append(palabraUsuarioNew)
                            palabraUsuario = ""
                            print(palabraCorrecta)

                    

                            


            segundos = TIEMPO_MAX_2 - pygame.time.get_ticks()/1000
            '''if msjRepetido:
                segundosMsj = abs(10 - pygame.time.get_ticks()/1000)
                defaultFont = pygame.font.Font( pygame.font.get_default_font(), TAMANNO_LETRA)
                while segundosMsj > 0:
                    # Imprimir mensaje durante un tiempo
                    screen.blit(defaultFont.render("Has ingresado una palabra que ya has regresado", 1, COLOR_TEXTO), (680, 10))
                segundosMsj = 0'''
            
            #Limpiar pantalla anterior
            screen.fill(COLOR_FONDO)

            #Dibujar de nuevo todo
            dibujarSinIntentos(screen, listaDePalabrasUsuario, palabraUsuario, palabraCorrecta, puntos, segundos, gano, correctas, incorrectas, casi)
           
            pygame.display.flip()

        #Fin del juego

        
        if segundos < 0:
            porTiempo(screen, puntos)
        """while 1:
            #Esperar el QUIT del usuario
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return"""

        archivo.close()
    else:
        archivo = open(lemario,"r")
        #lectura del diccionario
        lectura(archivo, listaPalabrasDiccionario, LARGO[0])
        print(lemario)

        #elige una al azar
        palabraCorrecta = nuevaPalabra(listaPalabrasDiccionario)

        intentos = 5
        dibujar(screen, listaDePalabrasUsuario, palabraUsuario, puntos, intentos, segundos, gano, correctas, incorrectas, casi)
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
                        palabraUsuario += "\n"
                        #Verifica si la palabra del usuario esta en el lemario y cumple con la longitud
                        if buscarPalabra(listaPalabrasDiccionario, palabraUsuario) == True and len(palabraUsuario) == LARGO[0]:
                            # Verifica si la palabra del usuario no es repetida, es decir, ya ingreso en algun intento anterior
                            if listaDePalabrasUsuario == [] or not buscarPalabra(listaDePalabrasUsuario, palabraUsuario):
                                #Revisa las letras del usuario
                                revision(palabraCorrecta, palabraUsuario, correctas, incorrectas, casi)
                                if palabraUsuario == palabraCorrecta:
                                    puntos = (len(correctas)*50)
                                    gano = True
                                else:
                                    puntos = (len(correctas)*50) + (len(casi)*25) - (len(incorrectas)* 10)
                                    palabraUsuarioNew = palabraUsuario.replace("\n","")
                                    listaDePalabrasUsuario.append(palabraUsuarioNew)
                                    palabraUsuario = ""
                                    intentos -= 1
                            else:
                                palabraUsuarioNew = palabraUsuario.replace("\n","")
                                listaDePalabrasUsuario.append(palabraUsuarioNew)
                                palabraUsuario = ""
                                intentos -= 1
                        else:
                            palabraUsuarioNew = palabraUsuario.replace("\n","")
                            listaDePalabrasUsuario.append(palabraUsuarioNew)
                            palabraUsuario = ""
                            intentos -= 1
                            


            segundos = TIEMPO_MAX - pygame.time.get_ticks()/1000
            '''if msjRepetido:
                segundosMsj = abs(10 - pygame.time.get_ticks()/1000)
                defaultFont = pygame.font.Font( pygame.font.get_default_font(), TAMANNO_LETRA)
                while segundosMsj > 0:
                    # Imprimir mensaje durante un tiempo
                    screen.blit(defaultFont.render("Has ingresado una palabra que ya has regresado", 1, COLOR_TEXTO), (680, 10))
                segundosMsj = 0'''
            
            #Limpiar pantalla anterior
            screen.fill(COLOR_FONDO)

            #Dibujar de nuevo todo
            dibujar(screen, listaDePalabrasUsuario, palabraUsuario, puntos, intentos, segundos, gano, correctas, incorrectas, casi)

            pygame.display.flip()

        #Fin del juego

        
        if intentos == 0 or segundos < 0:
            game_over(screen, palabraCorrecta)
        if gano == True:
            # Escribo el puntaje
            records = open("records.txt", "a")
            records.write("\n")
            records.write(NOMBRE[0]+": "+ str(puntos) +" puntos")
            records.close()
            fireworkWin(screen)

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
