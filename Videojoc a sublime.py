import pygame
import math
pygame.init()
# Iniciar programa

#Millora rendiment
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
#rellotge
rellotge = pygame.time.Clock()
FPS = 140
# Definir els colors bàsics
negre = (0, 0, 0)
blanc = (255, 255, 255)
vermell = (255, 0, 0)
vermell2 = (200, 0, 0)
verd = (0, 255, 0)
verd_fosc = (45,87,44)
blau = (0, 0, 255)
blau_fosc = (0, 0, 155)
cian = (0, 255, 255)
rosa = (255, 0, 255)
groc = (255, 255, 0)
taronja = (255, 165, 0)
taronja2 = (205, 115, 0)
taronja3 = (165, 75, 0)
marró = (128, 64, 0)
marró2 = (118, 54, 0)
marró_fosc = (84, 56, 34)
fons = (30,33,61)
fons2 = (80, 80, 255)
gris=(50,50,50)
pedra = (139,140,122)

# Preparar la pantalla
info = pygame.display.Info() 
pantalla_amplada,pantalla_alçada = info.current_w,info.current_h
from pygame.locals import *
flags = FULLSCREEN | DOUBLEBUF
pantalla = pygame.display.set_mode((pantalla_amplada, pantalla_alçada), flags, 16)
pygame.display.set_caption("Angry Birds")
from codi_ocells import ocell
from codi_porcs import porc
from codi_caixes import caixa
from codi_camera import camera 
# LListes
llista_objectes_rodons = []
llista_objectes_rectangulars = []
llista_objectes_pantalla = []
llista_ocells_llançats = []
sprites = []
llista_ocells = []
llista_porcs = []
#carregem skins
skin = pygame.image.load("Grafics/art4.png").convert_alpha()

#Posició inicial ocells
posició_inicial = [150, pantalla_alçada-150]
nombre_porcs = 0
nombre_ocells = 0

# Ocells creats 
vermellet = ocell(18, vermell, llista_ocells, llista_objectes_rodons, posició_inicial, pantalla)
bombardero = ocell(20, negre, llista_ocells, llista_objectes_rodons, posició_inicial, pantalla)
estrella = ocell(20, blanc, llista_ocells, llista_objectes_rodons, posició_inicial, pantalla)
pequeñin = ocell(13, cian, llista_ocells, llista_objectes_rodons, posició_inicial, pantalla)
racista = ocell(18, groc, llista_ocells, llista_objectes_rodons, posició_inicial, pantalla)
no_ocell = ocell(0, fons, llista_ocells, llista_objectes_rodons, posició_inicial, pantalla)
llista_ocells_llançats = [no_ocell]

#Creació ordre d'ocells
def següent_ocell(ordre_ocells):
    n = 0
    for i in ordre_ocells:
        if n == ordre_ocells.index(i):
            if i.llançat == False:
                if llista_objectes_pantalla.count(i) < 1:
                    llista_objectes_pantalla.append(i)
                    sprites.append(i)
                    llista_ocells_llançats.append(i)
                x = llista_ocells_llançats.index(i)
            if i.llançat: 
                if i.tocat_objecte == False:
                    x = llista_ocells_llançats.index(no_ocell)
                else:
                    n +=1
                    if n==len(ordre_ocells):
                        x = llista_ocells_llançats.index(no_ocell)  
    return x

# Creació porcs
porc_estandar = porc(20, (pantalla_amplada - 180, pantalla_alçada - 160), llista_porcs, llista_objectes_rodons, pantalla)

#Caixes 
terra = caixa([pantalla_amplada/2, pantalla_alçada + 45], 100, pantalla_amplada*3, False, 0,2, llista_objectes_rectangulars,pantalla)
paret_dreta = caixa([pantalla_amplada*2+100, 0],300, pantalla_alçada*2, False, 90,2, llista_objectes_rectangulars,pantalla)
paret_esquerra = caixa([terra.rectangle.left, pantalla_alçada/2 -250],300, pantalla_alçada+600, False, 90,2, llista_objectes_rectangulars,pantalla)
quadrat_petit = caixa([pantalla_amplada - 255, pantalla_alçada-48], 50, 50, True, 0,1, llista_objectes_rectangulars,pantalla)
rectangle_petit = caixa([pantalla_amplada - 230, pantalla_alçada-175], 20, 70, True, 90,2, llista_objectes_rectangulars,pantalla)
rectangle_petit_2 = caixa([pantalla_amplada - 230, pantalla_alçada-175], 20, 70, True, 90,1, llista_objectes_rectangulars,pantalla)
rectangle_normal = caixa([pantalla_amplada - 180, pantalla_alçada-245], 20, 150, True, 0,2, llista_objectes_rectangulars,pantalla)
quadrat_gran = caixa([pantalla_amplada - 180, pantalla_alçada-315], 60, 60, True, 0,3, llista_objectes_rectangulars,pantalla)
rectangle_gran = caixa([pantalla_amplada - 180, pantalla_alçada-105], 20, 200, True, 0,2, llista_objectes_rectangulars,pantalla)
tnt = caixa([pantalla_amplada - 280, pantalla_alçada-405], 50, 50, True, 0,5, llista_objectes_rectangulars,pantalla)

# Selecció de nivell
def selecció_nivell():
    nivell_seleccionat = 1
    selecció_nivell_acabada = False
    sortir_selecció = False
    cercle_pos = 0  # Variable per fer seguiment de la posició del cercle vermell
    cercle_color = vermell  # Color vermell (RGB)
    cercle_transparència = 150  # Valor d'alfa per la transparència (0 a 255)
    while not selecció_nivell_acabada:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and nivell_seleccionat < 12:
                    nivell_seleccionat += 1
                    cercle_pos += 1  # Actualitza la posició del cercle a la dreta
                elif event.key == pygame.K_LEFT and nivell_seleccionat > 1:
                    nivell_seleccionat -= 1
                    cercle_pos -= 1  # Actualitza la posició del cercle a la dreta
                elif event.key == pygame.K_SPACE:
                    selecció_nivell_acabada = True
                elif event.key == pygame.K_ESCAPE:
                    selecció_nivell_acabada = True
                    sortir_selecció = True
        
        pantalla.fill(fons2)
        if cercle_pos > 8:
            cercle_radi = 70
        else:  
            cercle_radi = 60
        font = pygame.font.Font(None, 150)
        text1 = font.render("Nivells", True, taronja)

        pantalla.blit(text1, (pantalla_amplada // 2 - text1.get_width() // 2, pantalla_alçada // 5 - text1.get_height() // 2 ))

        # Crear una llista de textos de números de l'1 al 12
        numeros = [str(i) for i in range(1, 13)]
        textos = [font.render(num, True, taronja) for num in numeros]

        posicions = [(pantalla_amplada // 5, pantalla_alçada * 2 // 5),
              (pantalla_amplada * 2 // 5, pantalla_alçada * 2 // 5),
              (pantalla_amplada * 3 // 5, pantalla_alçada * 2 // 5),
              (pantalla_amplada * 4 // 5, pantalla_alçada * 2 // 5),
              (pantalla_amplada // 5, pantalla_alçada * 3 // 5),
              (pantalla_amplada * 2 // 5, pantalla_alçada * 3 // 5),
              (pantalla_amplada * 3 // 5, pantalla_alçada * 3 // 5),
              (pantalla_amplada * 4 // 5, pantalla_alçada * 3 // 5),
              (pantalla_amplada // 5, pantalla_alçada * 4 // 5),
              (pantalla_amplada * 2 // 5, pantalla_alçada * 4 // 5),
              (pantalla_amplada * 3 // 5, pantalla_alçada * 4 // 5),
              (pantalla_amplada * 4 // 5, pantalla_alçada * 4 // 5)]

        font_gran = pygame.font.Font(None, 150)  # Mida de la font més gran
        cercle_x, cercle_y = posicions[cercle_pos]
        cercle_superficie = pygame.Surface((cercle_radi * 2, cercle_radi * 2), pygame.SRCALPHA)
        pygame.draw.circle(cercle_superficie, cercle_color + (cercle_transparència,), (cercle_radi, cercle_radi), cercle_radi)
        pantalla.blit(cercle_superficie, (cercle_x - cercle_radi, cercle_y - cercle_radi -5))
        for i, text in enumerate(textos):
            pos = posicions[i]
            num_text = font_gran.render(str(i+1), True, taronja)
            num_x = pos[0] - num_text.get_width() // 2
            num_y = pos[1] - num_text.get_height() // 2
            pantalla.blit(num_text, (num_x, num_y))
        pygame.display.flip()

    if sortir_selecció:
        return None
    else:
        return nivell_seleccionat

# Menú principal
def menú():
    global nivell_actual
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    dificultat = selecció_nivell()
                    if dificultat:
                        print("Dificultat seleccionada:", dificultat)
                        nivell_actual = dificultat
                        return True
                elif event.key == pygame.K_i:
                    info()
        pantalla.fill(fons2)

        font = pygame.font.Font(None, 300)
        text = font.render("Angry Birds", True, taronja)
        pantalla.blit(text, (pantalla_amplada // 2 - text.get_width() // 2, pantalla_alçada*2 // 5 - text.get_height() // 2))
        font = pygame.font.Font(None, 75)
        text2 = font.render("ESPAI PER CONTINUAR", True, taronja)
        pantalla.blit(text2, (pantalla_amplada *0.3 - text2.get_width() // 2, pantalla_alçada*4 // 5 - text2.get_height() // 2))
        text3 = font.render("'i' PER INFO", True, taronja)
        pantalla.blit(text3, (pantalla_amplada*0.75 - text3.get_width() // 2, pantalla_alçada*4 // 5 - text3.get_height() // 2))
        font2 = pygame.font.Font(None, 60)
        text1 = font2.render("ESC per a sortir", True, groc)
        pantalla.blit(text1, (text1.get_width()*0.2, text1.get_height()*1.5))
        pygame.display.flip()
def info():
    global nivell_actual
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        pantalla.fill(fons2)

        font = pygame.font.Font(None, 100)
        text = font.render("Camara", True, taronja)
        text5 = font.render("Ocells", True, taronja)
        text9 = font.render("Altres objectes", True, taronja)
        pantalla.blit(text, (text.get_width()*0.2 , text.get_height()*1.6))
        font = pygame.font.Font(None, 50)
        text2 = font.render("Al començar un nivell, la camara anirà a la part que no és veu. Per ha anar al", True, taronja)
        text3 = font.render("tiratxines pren espai. La camara al llançar un ocell el seguira. Per poder veure el", True, taronja)
        text4 = font.render("mapa amb llibertat utilitza el ratoli, per tornar al tiratxines pren espai un altre cop.", True, taronja)
        text6 = font.render("Per llançar un ocell arrastra'l amb el ratoli i deixa'l anar. Alguns ocells tenen una", True, taronja)
        text7 = font.render("habilitat especial que s'activa al fer click quan estan en el aire. Els ocells poden ", True, taronja)
        text8 = font.render("destruir caixes i fer despaeixer els porcs.", True, taronja)
        text10 = font.render("Els porcs són l'objectiu d'aquest joc, guanyes el nivell quan has eliminat a tots.", True, taronja)
        text11 = font.render("Les caixes són obstacles que estan protegint als porcs. Hi han de diferents tipos,", True, taronja)
        text12 = font.render("les de pedra són les més difícils de trencar, mentre que les de vidre les més fàcils.", True, taronja)
        text13 = font.render(" La TNT explota al xocar-se.", True, taronja)
        textos = [text2,text3,text4,text5,text6,text7,text8,text9,text10,text11,text12,text13]
        a = 1
        b = -1
        for i in textos:
            if i.get_height() > text2.get_height()+1:
                amplada = text.get_width()*0.2
                b += 1.5
            else:
                b+=1
                amplada = 10
            pantalla.blit(i, (amplada, text.get_height()*2.6*a +text2.get_height()*b))
            if i.get_height() > text2.get_height()+1:
                amplada = text.get_width()*0.2
                a+=1.1
                b = -1    
        font2 = pygame.font.Font(None, 60)
        text1 = font2.render("ESC per a sortir", True, groc)
        pantalla.blit(text1, (text1.get_width()*0.2, text1.get_height()*1.5))
        pygame.display.flip()
def pantalla_final(tipo, estrelles):
    global partida
    if tipo == True:
        texto = "VICTÒRIA"
        texto2 = "Espai per a següent nivell"
    else:
        texto = "DERROTA"
        texto2 = "Espai per a repetir nivell"
    final = True
    while final:
        color = estrelles
        n = 3
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    y = False
                    final = False
                if event.key == pygame.K_SPACE:
                    y = True
                    final = False
        pantalla.fill(fons2)
        texto1 = "ESC per a menú principal" 
        font = pygame.font.Font(None, 300)
        font2 = pygame.font.Font(None, 60)
        text = font.render(texto, True, taronja)
        text1 = font2.render(texto1, True, groc)
        text2 = font2.render(texto2, True, groc)
        pantalla.blit(text, (pantalla_amplada // 2 - text.get_width() // 2, pantalla_alçada // 2.5 - text.get_height() // 2))
        pantalla.blit(text1, (pantalla_amplada/2-(text1.get_width()+(pantalla_amplada - text2.get_width()-50-pantalla_amplada/2)), 100))
        pantalla.blit(text2, (pantalla_amplada - text2.get_width()-50, 100))

        while n >0:
            if color >0:
                color_estrella = taronja
            else:
                color_estrella = gris
            z = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
            x = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
            for i in z:
                i*=1.3
                i +=(pantalla_amplada*(3-n)/3+225,pantalla_alçada-200)
            for i in x:
                i += (pantalla_amplada*(3-n)/3+225,pantalla_alçada-200)
            pygame.draw.polygon(pantalla, taronja3, z)
            pygame.draw.polygon(pantalla, color_estrella, x)
            n-=1
            color-=1
        pygame.display.flip()
    return y
#Definim reinici al sortir del nivell
def reinici():
    global llista_objectes_pantalla
    global sprites
    global llista_ocells_llançats
    for i in sprites:
        i.reinici()
    llista_objectes_pantalla = [terra, paret_dreta, paret_esquerra]
    sprites = [terra]
    llista_ocells_llançats = [no_ocell]
    camara.diferencia *= 0 
    camara.rectangle_camara.topleft = camara.rectangle_camara_orig
    camara.principi_nivell = True

#Definim camera
camara = camera(pantalla_amplada, pantalla_alçada, pantalla)
#Defimin nivells
ocells4 = [bombardero.copy(llista_ocells, llista_objectes_rodons), pequeñin.copy(llista_ocells, llista_objectes_rodons), estrella.copy(llista_ocells, llista_objectes_rodons), racista.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), racista.copy(llista_ocells, llista_objectes_rodons)]
ocells1 = [vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons),vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells2 = [racista.copy(llista_ocells, llista_objectes_rodons),racista.copy(llista_ocells, llista_objectes_rodons),racista.copy(llista_ocells, llista_objectes_rodons),vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells3 = [pequeñin.copy(llista_ocells, llista_objectes_rodons),pequeñin.copy(llista_ocells, llista_objectes_rodons),pequeñin.copy(llista_ocells, llista_objectes_rodons),pequeñin.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells5 = [vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells6 = [vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells7 = [vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells8 = [vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells9 = [vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells10 = [vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells11 = [vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells12 = [vermellet.copy(llista_ocells, llista_objectes_rodons)]
nivells_ocells = {1:ocells1, 2:ocells2, 3:ocells3, 4:ocells4, 5:ocells5, 6:ocells6, 7:ocells7, 8:ocells8, 9:ocells9, 10:ocells10, 11:ocells11, 12:ocells12}

nivell4 = [rectangle_gran, quadrat_petit,quadrat_petit.copy([pantalla_amplada - 105, pantalla_alçada-48], llista_objectes_rectangulars),rectangle_petit,rectangle_petit.copy([pantalla_amplada - 130, pantalla_alçada-175], llista_objectes_rectangulars),rectangle_normal, quadrat_gran,quadrat_petit.copy([pantalla_amplada - 505, pantalla_alçada-48], llista_objectes_rectangulars),quadrat_petit.copy([pantalla_amplada - 355, pantalla_alçada-48], llista_objectes_rectangulars),rectangle_petit.copy([pantalla_amplada - 480, pantalla_alçada-175], llista_objectes_rectangulars),rectangle_petit.copy([pantalla_amplada - 380, pantalla_alçada-175], llista_objectes_rectangulars),rectangle_normal.copy([pantalla_amplada - 430, pantalla_alçada-245], llista_objectes_rectangulars),quadrat_gran.copy([pantalla_amplada - 430, pantalla_alçada-315], llista_objectes_rectangulars),rectangle_gran.copy([pantalla_amplada - 430, pantalla_alçada-105], llista_objectes_rectangulars), porc_estandar, porc_estandar.copy((pantalla_amplada - 430, pantalla_alçada - 160), llista_porcs, llista_objectes_rodons)]
nivell1 = [porc_estandar.copy([pantalla_amplada+260, pantalla_alçada-265], llista_porcs, llista_objectes_rodons), porc_estandar.copy([pantalla_amplada- 140, pantalla_alçada-265], llista_porcs, llista_objectes_rodons), rectangle_petit.copy([pantalla_amplada + 295,pantalla_alçada-40], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada +295,pantalla_alçada-115], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada +295,pantalla_alçada-190], llista_objectes_rectangulars),rectangle_petit.copy([pantalla_amplada + 225,pantalla_alçada-40], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+225,pantalla_alçada-115], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+225,pantalla_alçada-190], llista_objectes_rectangulars), rectangle_normal.copy([pantalla_amplada + 260, pantalla_alçada-255], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada +25,pantalla_alçada-115], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+25,pantalla_alçada-190], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+95,pantalla_alçada-115], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+95,pantalla_alçada-190], llista_objectes_rectangulars), rectangle_normal.copy([pantalla_amplada+60, pantalla_alçada-255], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada- 105,pantalla_alçada-90], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada- 175,pantalla_alçada-90], llista_objectes_rectangulars), rectangle_normal.copy([pantalla_amplada- 140, pantalla_alçada-145], llista_objectes_rectangulars),tnt.copy([pantalla_amplada+60, pantalla_alçada-300], llista_objectes_rectangulars), porc_estandar.copy([pantalla_amplada+ 540, pantalla_alçada-265], llista_porcs, llista_objectes_rodons), porc_estandar.copy([pantalla_amplada+ 940, pantalla_alçada-265], llista_porcs, llista_objectes_rodons), rectangle_petit.copy([pantalla_amplada+ 505,pantalla_alçada-40], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 505,pantalla_alçada-115], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 505,pantalla_alçada-190], llista_objectes_rectangulars),rectangle_petit.copy([pantalla_amplada+ 575,pantalla_alçada-40], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 575,pantalla_alçada-115], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 575,pantalla_alçada-190], llista_objectes_rectangulars), rectangle_normal.copy([pantalla_amplada+ 540, pantalla_alçada-255], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 705,pantalla_alçada-115], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 705,pantalla_alçada-190], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 775,pantalla_alçada-115], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 775,pantalla_alçada-190], llista_objectes_rectangulars), rectangle_normal.copy([pantalla_amplada+ 740, pantalla_alçada-255], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 905,pantalla_alçada-90], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 975,pantalla_alçada-90], llista_objectes_rectangulars), rectangle_normal.copy([pantalla_amplada+ 940, pantalla_alçada-145], llista_objectes_rectangulars),tnt.copy([pantalla_amplada+ 740, pantalla_alçada-300], llista_objectes_rectangulars)]
nivell2 = [porc_estandar.copy((pantalla_amplada*0.75,pantalla_alçada-320), llista_porcs, llista_objectes_rodons), porc_estandar.copy((pantalla_amplada*1.05,pantalla_alçada-320), llista_porcs, llista_objectes_rodons), porc_estandar.copy((pantalla_amplada*1.5,pantalla_alçada-420), llista_porcs, llista_objectes_rodons), porc_estandar.copy((pantalla_amplada*1.75,pantalla_alçada-420), llista_porcs, llista_objectes_rodons),caixa([pantalla_amplada*1.6, pantalla_alçada-50], 100, pantalla_amplada*2, False, 0,2, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*0.51, pantalla_alçada*1.082+100], 200, pantalla_amplada/2.5, False, 45,2, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*2.4, pantalla_alçada-150], 200, pantalla_amplada*2, False, 0,2, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*1.31, pantalla_alçada*1.082-50], 200, pantalla_amplada/2.5, False, 45,2, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*0.75,pantalla_alçada-225], 20, 150, True, 90, 3, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*0.75,pantalla_alçada-310], 20, 100, True, 0, 3, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*1.05,pantalla_alçada-225], 20, 150, True, 90, 3, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*1.05,pantalla_alçada-310], 20, 100, True, 0, 3, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*1.5,pantalla_alçada-325], 20, 150, True, 90, 3, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*1.5,pantalla_alçada-410], 20, 100, True, 0, 3, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*1.75,pantalla_alçada-325], 20, 150, True, 90, 3, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*1.75,pantalla_alçada-410], 20, 100, True, 0, 3, llista_objectes_rectangulars,pantalla)]
nivell3 = [porc_estandar.copy((pantalla_amplada+80*-1, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80*2, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80*-2, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80*3, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80*-3, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80*4, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80*5, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80*6, pantalla_alçada-40), llista_porcs, llista_objectes_rodons), porc_estandar.copy((pantalla_amplada+80*7, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80*8, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80, pantalla_alçada-40), llista_porcs, llista_objectes_rodons), porc_estandar.copy((pantalla_amplada, pantalla_alçada-40), llista_porcs, llista_objectes_rodons), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*2), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*3), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*4), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*5), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*6), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*7), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*8), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*9), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*10), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*11), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*12), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*13), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*2), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*3), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*4), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*5), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*6), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*7), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*8), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*9), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*10), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*11), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*12), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*13), llista_objectes_rectangulars)]
nivell5 = [porc_estandar.copy((1000,pantalla_alçada-40), llista_porcs, llista_objectes_rodons)]
nivell6 = [porc_estandar.copy((1000,pantalla_alçada-40), llista_porcs, llista_objectes_rodons)]
nivell7 = [porc_estandar.copy((1000,pantalla_alçada-40), llista_porcs, llista_objectes_rodons)]
nivell8 = [porc_estandar.copy((1000,pantalla_alçada-40), llista_porcs, llista_objectes_rodons)]
nivell9 = [porc_estandar.copy((1000,pantalla_alçada-40), llista_porcs, llista_objectes_rodons)]
nivell10 = [porc_estandar.copy((1000,pantalla_alçada-40), llista_porcs, llista_objectes_rodons)]
nivell11 = [porc_estandar.copy((1000,pantalla_alçada-40), llista_porcs, llista_objectes_rodons)]
nivell12 = [porc_estandar.copy((1000,pantalla_alçada-40), llista_porcs, llista_objectes_rodons)]
nivells_caixes_i_porcs = {1:nivell1, 2:nivell2, 3:nivell3, 4:nivell4, 5:nivell5, 6:nivell6, 7:nivell7, 8:nivell8, 9:nivell9, 10:nivell10, 11:nivell11, 12:nivell12}

# Game GameLoop
def GameLoop():
    global nivell_actual
    global nombre_porcs
    global nombre_ocells
    zona_ocell = False
    mantenint_ocell = False
    partida = False
    mantenint = False
    rectangle_mantenint = camara.rectangle_camara.copy()
    posició_mantenint = pygame.mouse.get_pos()
    while True:
        rellotge.tick(FPS)
        if not partida:
            if not menú():
                break
            reinici()
            partida = True
            n = 0
            nombre_porcs = 0
            nombre_porcs_orig = 0
            nombre_ocells = 0
            n2 = 0
        else:
            n2 += 1
            if n==0:
                sprites.extend(nivells_caixes_i_porcs[nivell_actual])
                llista_objectes_pantalla.extend(nivells_caixes_i_porcs[nivell_actual])
                for i in llista_objectes_pantalla:
                    if i in llista_porcs:
                        nombre_porcs+=1
                        nombre_porcs_orig += 1
                ocells_nivell = nivells_ocells[nivell_actual]
                for i in ocells_nivell:
                    if i.radi != 0:
                        nombre_ocells +=1
                n =1
            ocell_actual = llista_ocells_llançats[següent_ocell(ocells_nivell)]
            if len(llista_ocells_llançats) > 1:
                ocell_anterior =  llista_ocells_llançats[següent_ocell(ocells_nivell)-1]
            else:
                ocell_anterior = ocell_actual
            zona_ocell = ocell_actual.zona_llançament(camara.diferencia)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    partida = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        partida = False
                    if event.key == pygame.K_SPACE:
                        camara.principi_nivell = False
                        camara.tornar_ocell = True
                    if event.key == pygame.K_t:
                        for i in llista_ocells:
                            i.posar_skin(skin)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if zona_ocell:    
                        mantenint_ocell = True
                        ocell_actual.linea_direció = True
                    elif (ocell_anterior.llançat and ocell_anterior.tocat_objecte) or (ocell_anterior.llançat==False):
                        mantenint = True
                        rectangle_mantenint = camara.rectangle_camara.copy()
                        posició_mantenint = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if mantenint_ocell:
                        mantenint_ocell = False
                        ocell_actual.linea_direció = False
                        ocell_actual.llançament(camara.diferencia)
                    elif mantenint:
                        mantenint = False
                    elif ocell_anterior.tocat_objecte == False:
                        nombre_ocells = ocell_anterior.habilitat(llista_ocells, llista_objectes_rodons, llista_objectes_pantalla, llista_porcs, llista_objectes_rectangulars, sprites, nombre_ocells)
            # Aparèixer porcs, ocells i linea
            for i in  llista_objectes_pantalla:
                if i in llista_ocells:
                    nombre_ocells = i.update(nombre_ocells, llista_objectes_pantalla)
                else:
                    i.update(llista_objectes_pantalla)
            llista_objectes_pantalla.sort(key=lambda i: i.rectangle.center[1])
            for self in llista_objectes_pantalla:
                if self in llista_ocells:
                    if self.llançat:    
                        for i in llista_objectes_pantalla:
                            if i in llista_ocells:    
                                if i.llançat and i.colisionat==False and i!= self: 
                                    if self.rectangle.colliderect(i.rectangle):
                                        if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):
                                            nombre_porcs = self.colisió(i,llista_ocells, llista_objectes_rectangulars, llista_objectes_rodons, llista_porcs,nombre_porcs, llista_objectes_pantalla)
                            elif i in llista_objectes_rectangulars:    
                                if self.rectangle.colliderect(i.rectangle) and i.caixa: 
                                    if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):    
                                        nombre_porcs = self.colisió(i,llista_ocells, llista_objectes_rectangulars, llista_objectes_rodons, llista_porcs,nombre_porcs, llista_objectes_pantalla)
                            else:    
                                if self.rectangle.colliderect(i.rectangle) and i.porc: 
                                    if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):    
                                        nombre_porcs = self.colisió(i,llista_ocells, llista_objectes_rectangulars, llista_objectes_rodons, llista_porcs,nombre_porcs, llista_objectes_pantalla)
                    self.colisionat = True
                if self in llista_objectes_rectangulars:
                    if self.movible and self.caixa:    
                        for i in llista_objectes_pantalla:
                            if i != self and i.colisionat == False and i in llista_objectes_rectangulars:
                                if self.rectangle.colliderect(i.rectangle) and i.caixa:
                                    if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):
                                        self.colisió(i, llista_objectes_pantalla, llista_objectes_rectangulars)
                        self.colisionat = True
                if self in llista_porcs:
                    if self.porc:    
                        for i in llista_objectes_pantalla:
                            if i in llista_ocells:    
                                if i.llançat and i.colisionat==False: 
                                    if self.rectangle.colliderect(i.rectangle):
                                        if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):
                                            nombre_porcs = self.colisió(i,llista_ocells, llista_objectes_rectangulars, llista_objectes_rodons, llista_porcs,nombre_porcs, llista_objectes_pantalla)
                            elif i in llista_objectes_rectangulars:    
                                if self.rectangle.colliderect(i.rectangle) and i.caixa: 
                                    if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):    
                                        nombre_porcs = self.colisió(i, llista_ocells, llista_objectes_rectangulars, llista_objectes_rodons, llista_porcs,nombre_porcs, llista_objectes_pantalla)
                            elif i!= self and i.porc:    
                                if self.rectangle.colliderect(i.rectangle): 
                                    if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):    
                                        nombre_porcs = self.colisió(i,llista_ocells, llista_objectes_rectangulars, llista_objectes_rodons, llista_porcs,nombre_porcs, llista_objectes_pantalla)
                        self.colisionat = True
            fps_actuals = rellotge.get_fps()
            if fps_actuals!=0:
                if 140-fps_actuals<=40:
                    velocitat = 1
                elif 140-fps_actuals<=70:
                    velocitat = 2
                else:
                    velocitat =3
            else:
                velocitat = 1
            if n2%3 == 0:
                pantalla.fill(fons)
                camara.update(llista_objectes_pantalla,ocell_anterior, ocells_nivell, ocell_actual, mantenint_ocell, ocell_anterior, mantenint,posició_mantenint,rectangle_mantenint, llista_ocells_llançats)
            if nombre_porcs == 0:
                estrelles = nombre_porcs_orig - (len(llista_ocells_llançats)-3)
                estrelles+=2
                if estrelles < 1:
                    estrelles = 1
                partida = pantalla_final(True,estrelles)
                reinici()
                n = 0
                nombre_porcs_orig = 0
                nivell_actual+=1
                nombre_ocells = 0
                n2 = 0
                if nivell_actual == 13:
                    partida = False
            elif nombre_ocells == 0:
                reinici()
                n = 0
                nombre_porcs = 0
                nombre_porcs_orig = 0
                n2 = 0
                partida = pantalla_final(False,0)
         # Recarregar la pantalla
        pygame.display.flip()
    # Sortir del joc
    pygame.quit()

# Córrer el joc
GameLoop()