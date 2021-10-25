from principal import *
import configuracion
from funcionesSeparador import *

import pygame
import random
import math



def lectura(archivo):
    a = archivo.read()
    lista = a.split("\n")
## Elimina el ultimo elemento de la lista, porque hay un espacio vacio.
    lista.pop(len(lista)-1)
    return lista


def actualizar(silabasEnPantalla,posiciones,listaDeSilabas):
## Extremos para generar una ubicacion al azar entre estos.
    extremoIzquierdo = (configuracion.ANCHO - 750)
    extremoDerecho = (configuracion.ANCHO - 50)  
    nuevaSilabaPosicion = random.randint(extremoIzquierdo, extremoDerecho)
## Paso siguiente nos separa la silaba a crear de la ultima añadida.
    lastSilabaXIndex = len(posiciones) - 1
    if lastSilabaXIndex > 0:   
        while (posiciones[lastSilabaXIndex][0] - 35) <= nuevaSilabaPosicion <= (posiciones[lastSilabaXIndex][0] + 35):        
            nuevaSilabaPosicion = random.randint(extremoIzquierdo, extremoDerecho)    
    silabasEnPantalla.append(nuevaSilaba(listaDeSilabas))
    posiciones.append([nuevaSilabaPosicion, configuracion.ORIGIN])
## Movimiento descendente
    amountOfSilabas = len(silabasEnPantalla)
    i = 0
    while (i < amountOfSilabas):
        posiciones[i][1] += configuracion.VSPEED
        if (posiciones[i][1] >= (configuracion.BOTTOMCLEAR)):
            posiciones.pop(i)
            silabasEnPantalla.pop(i)
            amountOfSilabas = len(silabasEnPantalla)
            ## 
        else:
            i += 1
        


## Del archivo de silabas toma una al azar y la retorna como string
def nuevaSilaba(listaDeSilabas):
    newSilaba = listaDeSilabas[random.randint(0,len(listaDeSilabas)-1)]
    return newSilaba


def quitar(candidata, silabasEnPantalla, posiciones):
# Lista de silabas a eliminar
    toClean = dameSilabas(candidata)
    for elem in toClean:
        indexSilaba = (silabasEnPantalla.index(elem))
        silabasEnPantalla.pop(indexSilaba)
        posiciones.pop(indexSilaba)      


def dameSilabas(candidata):
    n = 0
    toDeleteSilabas = []
    addToDeleteList = ""
    splitedWord = separador(candidata)
    for char in splitedWord:
        if (char == "-"):
            toDeleteSilabas.append(addToDeleteList)
            addToDeleteList = ""
        elif (n == len(splitedWord)-1):
            addToDeleteList += char
            toDeleteSilabas.append(addToDeleteList)                
        else:
             addToDeleteList += char
        n = n + 1 
    return toDeleteSilabas



## Recibe palabra ingresada, silabas en pantalla y lemario. Si no esta en lemario return False, si no esta alguna silaba en pantalla, False. De lo contrario True.
def esValida(candidata, silabasEnPantalla, lemario):
    candidataSeparada = dameSilabas(candidata)
    if candidata in lemario:
        for elem in candidataSeparada:
            if elem not in silabasEnPantalla:
                return False
        return True
    return False



def Puntos(candidata):
## Return puntaje en numero int.
    puntaje = 0
    vowels = ['a', 'e', 'i', 'o', 'u']
    hardConsonant = ['j', 'k', 'q', 'w', 'x', 'y', 'z']
    for char in candidata:
        if char in vowels:
            puntaje += 1
        elif char in hardConsonant:
            puntaje += 5
        else:
            puntaje += 2          
    return puntaje


def procesar(candidata, silabasEnPantalla, posiciones, lemario, okSound, wrongSound):
## Le añadimos un contador para saber la cantidad de palabras acertadas. (cantPalarbas)
## Ademas cuando se apreta enter al validar la palabra ejecuta un sonido, diferido para ok y para erroneo.
    score = 0
    if esValida(candidata, silabasEnPantalla, lemario):        
        score = Puntos(candidata)
        quitar(candidata, silabasEnPantalla, posiciones)
        candidata = ""
        okSound.play()
        return score
    else:
        wrongSound.play()
        return score


## Añadimos la siguiente funcion siguiente para poder darle un final al juego, previamente quedaba colgado al llegar
## a segundos cero, ahora da un resumen de la partida.
def dibujarGameOver(screen, puntos, cantPalabras):
# Paso siguiente para que no quede desprolijo si acertaba 1 palabra, el texto quedaba en plural.
    if cantPalabras == 1:        
        palabra = " palabra!"
    else:
        palabra = " palabras!"
    defaultFont= pygame.font.Font( pygame.font.get_default_font(), configuracion.TAMANNO_LETRA)


    

    renGracias = defaultFont.render("Gracias por jugar 'SILABAS'", 1, configuracion.COLOR_LETRAS_FINAL)
    renCantPalabras = defaultFont.render("Usted acerto: " + str(cantPalabras) + palabra, 1, configuracion.COLOR_TEXTO_FINAL)
    renPuntaje = defaultFont.render("Su puntaje final es: " + str(puntos), 1, configuracion.COLOR_TEXTO_FINAL)


    screen.blit(renGracias, (configuracion.ANCHO - 525,configuracion.ALTO - 150))
    screen.blit(renCantPalabras, (configuracion.ANCHO - 515,configuracion.ALTO - 100))
    screen.blit(renPuntaje, (configuracion.ANCHO - 499, configuracion.ALTO - 50))
