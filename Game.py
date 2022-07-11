import pygame
import random
import math
from pygame import mixer

#iniciar pygame
pygame.init()

#crear pantalla
pantalla = pygame.display.set_mode((800, 600))

#titulo, icono y fondo
pygame.display.set_caption("Invation")
icono = pygame.image.load("marciano.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("fondo.jpg")

#agregar musica

mixer.music.load("fondo.mp3")
mixer.music.set_volume(0.2)
#mixer.music.play()  --> no funciona

#variables de jugador
img_jugador = pygame.image.load("astronave.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

#variables de enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 6

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("ovni.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(0, 150))
    enemigo_x_cambio.append(0.3)
    enemigo_y_cambio.append(50)

#variables de proyectil
img_proyectil = pygame.image.load("misil.png")
proyectil_x = 0
proyectil_y = 500
proyectil_x_cambio = 0
proyectil_y_cambio = 2
proyectil_visible = False

#variable de puntaje

puntaje = 0
fuente = pygame.font.Font("Those Glitch Regular.ttf", 24)
texto_x = 10
texto_y = 10

#texto final de juego

fuente_final = pygame.font.Font("Those Glitch Regular.ttf", 40)
def texto_final():
    mi_fuente_final = fuente_final.render("GAME OVER", True, (255,255,255))
    pantalla.blit(mi_fuente_final, (200,200))

#funcion mostrar puntaje

def motrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje : {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


#funcion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

#funcion enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

#funcion disparr proyectil

def disparar(x, y):
    global proyectil_visible
    proyectil_visible = True
    pantalla.blit(img_proyectil, (x+16, y+10))

#funcion detectar colisiones

def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1-x_2,2) + math.pow(y_2 - y_1,2))
    if distancia < 27:
        return True
    else:
        return False

#Loop del juego
se_ejecuta = True
while se_ejecuta:
    #imagen de fondo
    pantalla.blit(fondo, (0,0))

    #Iterar eventos
    for evento in pygame.event.get():
        #cerrar programa cuando se le da en la equis
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        #reconocer cuando se oprima una tecla
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE:
                sonido_disparo = mixer.Sound("disparo.mp3")
                sonido_disparo.play()
                if not proyectil_visible:
                    proyectil_x = jugador_x
                    disparar(proyectil_x, proyectil_y)


        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0


    #modificar ubicación del jugador
    jugador_x += jugador_x_cambio

    #mantener dentro de bordes a jugador
    if jugador_x <= 0:
        jugador_x = 0
    if jugador_x >= 736:
        jugador_x = 736

    #modificar ubicación del enemigo

    for e in range(cantidad_enemigos):
        #fin de juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

    #mantener dentro de bordes a enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.3
            enemigo_y[e] += enemigo_y_cambio[e]
        if enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.3
            enemigo_y[e] += enemigo_y_cambio[e]
        # colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e],
proyectil_x, proyectil_y)
        if colision:
            sonido_colision = mixer.Sound("golpe.mp3")
            sonido_colision.play()
            proyectil_y = 500
            proyectil_visible = False
            puntaje += 100
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(0, 150)
        enemigo(enemigo_x[e], enemigo_y[e], e)

    #movimiento proyectil
    if proyectil_y <= 0:
        proyectil_y = 500
        proyectil_visible= False





    if proyectil_visible:
        disparar(proyectil_x, proyectil_y)
        proyectil_y -=  proyectil_y_cambio


    jugador(jugador_x, jugador_y)
    motrar_puntaje(texto_x, texto_y)


    #actualizar pantalla
    pygame.display.update()
