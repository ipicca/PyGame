#! /usr/bin/env python
import os, random, sys, math

import pygame
from pygame.locals import *

from configuracion import *
from extras import *
from funcionesSeparador import *
from funcionesVACIAS import *



#Funcion principal
def main():
    #Centrar la ventana y despues inicializar pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    #pygame.mixer.init()

    #Preparar la ventana y cargo imagen de fondo.
    bkImage = pygame.image.load("bkImage00.png")
    pygame.display.set_caption("Silabas...")
    screen = pygame.display.set_mode((ANCHO, ALTO))

    #tiempo total del juego
    gameClock = pygame.time.Clock()

    #SONIDOS
    backMusic = pygame.mixer.music.load('musicwav.wav')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    okWord = pygame.mixer.Sound('succes.wav')
    wrongWord = pygame.mixer.Sound('incorrect.wav')



    totaltime = 0
    segundos = TIEMPO_MAX
    fps = FPS_inicial
    cantPalabras = 0
    puntos = 0
    candidata = ""
    silabasEnPantalla = []
    posiciones = []
    
    
    archivo= open("silabas.txt","r")
    listaDeSilabas = lectura(archivo)
## Agregamos la siguiente linea para cerrar el archivo.
    archivo.close()

    archivo2= open("lemario.txt","r", encoding = "latin-1")
    lemario = lectura(archivo2)       
    archivo2.close()

    
    dibujar(screen, candidata, silabasEnPantalla, posiciones, puntos, segundos)
    
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
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pygame.quit()
                    return()



            #Ver si fue apretada alguna tecla
            if e.type == KEYDOWN:
                letra = dameLetraApretada(e.key)
                candidata += letra
                if e.key == K_BACKSPACE:
                    candidata = candidata[0:len(candidata)-1]
                if e.key == K_RETURN:
                    if esValida(candidata, silabasEnPantalla,lemario):
                        cantPalabras += 1
                    puntos += procesar(candidata, silabasEnPantalla, posiciones, lemario, okWord, wrongWord)
                    candidata = ""                                            


        segundos = TIEMPO_MAX - pygame.time.get_ticks()/1000

        #Limpiar pantalla anterior
        screen.blit(bkImage, (0, 0))
        
        #Dibujar de nuevo todo
        dibujar(screen, candidata, silabasEnPantalla, posiciones, puntos, segundos)
        
        pygame.display.flip()
        
        actualizar(silabasEnPantalla, posiciones, listaDeSilabas)
        
        
    while (segundos < 1):
        screen.blit(bkImage, (0, 0))
        dibujarGameOver(screen, puntos, cantPalabras)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                return
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pygame.quit()
                    return()

    # while 1:
    #     #Esperar el QUIT del usuario
    #     for e in pygame.event.get():
    #         if e.type == QUIT:
    #             pygame.quit()
    #             return

#Programa Principal ejecuta Main
if __name__ == "__main__":
    main()
