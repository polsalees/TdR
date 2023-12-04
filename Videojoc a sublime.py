import pygame
import math
import random
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
vermell2 = (150, 0, 0)
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
groc2 = (159,120,0)

# Preparar la pantalla
info = pygame.display.Info() 
pantalla_amplada,pantalla_alçada = info.current_w,info.current_h
from pygame.locals import *
flags = FULLSCREEN | DOUBLEBUF
pantalla = pygame.display.set_mode((pantalla_amplada, pantalla_alçada), flags, 16)
pygame.display.set_caption("Galactic Pius")
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
skin1 = pygame.image.load("Grafics/skin1.png").convert_alpha()
skin2 = pygame.image.load("Grafics/skin2.png").convert_alpha()
skin3 = pygame.image.load("Grafics/skin3.png").convert_alpha()
skin4 = pygame.image.load("Grafics/skin4.png").convert_alpha()
skin5 = pygame.image.load("Grafics/skin5.png").convert_alpha()
skin6 = pygame.image.load("Grafics/skin6.png").convert_alpha()
skin7 = pygame.image.load("Grafics/skin7.png").convert_alpha()
skin8 = pygame.image.load("Grafics/skin8.png").convert_alpha()
skin9 = pygame.image.load("Grafics/skin9.png").convert_alpha()
skin10 = pygame.image.load("Grafics/skin10.png").convert_alpha()
skin11 = pygame.image.load("Grafics/skin11.png").convert_alpha()
skin12 = pygame.image.load("Grafics/skin12.png").convert_alpha()
tick_imatge = pygame.image.load("Grafics/tick.png").convert_alpha()
fletxa_imatge = pygame.image.load("Grafics/fletxa.png").convert_alpha()
info_imatge = pygame.image.load("Grafics/info.png").convert_alpha()
tenda_imatge = pygame.image.load("Grafics/tenda.png").convert_alpha()
repetir_imatge = pygame.image.load("Grafics/repetir.png").convert_alpha()
home_imatge = pygame.image.load("Grafics/home.png").convert_alpha()
play_imatge = pygame.image.load("Grafics/play.png").convert_alpha()
pausa_imatge = pygame.image.load("Grafics/pausa.png").convert_alpha()
pausa_imatge = pygame.transform.scale(pausa_imatge,(90*0.7,90*0.7))
pausa_imatge_2 = pygame.transform.scale(pausa_imatge,(90*0.7*1.2,90*0.7*1.2))
rectangle_pausa = pygame.Rect(pantalla_amplada/20,pantalla_alçada/14, 90,90)
rectangle_pausa_2 = pygame.Rect(pantalla_amplada/20,pantalla_alçada/14, 90*1.2,90*1.2)
rectangle_pausa_2.center = rectangle_pausa.center
x_imatge = pygame.image.load("Grafics/x.png").convert_alpha()
títol = pygame.image.load("Grafics/GALACTIC-PIUS.png").convert_alpha()
nivells_imatge = pygame.image.load("Grafics/NIVELLS.png").convert_alpha()
nivells_imatge = pygame.transform.scale(nivells_imatge,(pantalla_amplada*0.3,pantalla_amplada*0.3*(66/407)))
nivells_rect = nivells_imatge.get_rect(center = (pantalla_amplada//2, pantalla_alçada//6))
info_imatges = pygame.image.load("Grafics/INFO.png").convert_alpha()
info_imatges = pygame.transform.scale(info_imatges,(pantalla_amplada*0.2,pantalla_amplada*0.2*(66/230)))
info_rect = info_imatges.get_rect(center = (pantalla_amplada//2, pantalla_alçada//8))
victoria_imatge = pygame.image.load("Grafics/VICTORIA.png").convert_alpha()
victoria_imatge = pygame.transform.scale(victoria_imatge,(pantalla_amplada*0.75,pantalla_amplada*0.75*(66/407)))
victoria_rect = victoria_imatge.get_rect(center = (pantalla_amplada//2, pantalla_alçada//4))
derrota_imatge = pygame.image.load("Grafics/DERROTA.png").convert_alpha()
derrota_imatge = pygame.transform.scale(derrota_imatge,(pantalla_amplada*0.75,pantalla_amplada*0.75*(66/407)))
derrota_rect = derrota_imatge.get_rect(center = (pantalla_amplada//2, pantalla_alçada//4))
tendas_imatg = pygame.image.load("Grafics/TENDA.png").convert_alpha()
tendas_imatg = pygame.transform.scale(tendas_imatg,(pantalla_amplada*0.3*(291/407),pantalla_amplada*0.3*(66/407)))
tendas_rect = tendas_imatg.get_rect(center = (pantalla_amplada//2, pantalla_alçada//6))
pausas_imatg = pygame.image.load("Grafics/PAUSA.png").convert_alpha()
pausas_imatg = pygame.transform.scale(pausas_imatg,(pantalla_amplada*0.4*(291/407),pantalla_amplada*0.4*(66/407)))
pausas_rect = pausas_imatg.get_rect(center = (pantalla_amplada//2, pantalla_alçada*3//8))
fons_2 = pygame.image.load("Grafics/fons2.jpg").convert_alpha()
fons_2 = pygame.transform.scale(fons_2,(pantalla_alçada*(728/410)*1.7, pantalla_alçada*1.7))
posar_tick = False
posicio_tick = 0
imatge_skin = None
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
porc_estandar = porc(20, (pantalla_amplada - 180, pantalla_alçada - 160), llista_porcs, llista_objectes_rodons, pantalla, False)
porc_movible = porc(20, (pantalla_amplada - 180, pantalla_alçada - 160), llista_porcs, llista_objectes_rodons, pantalla, True)

#Caixes 
terra = caixa([pantalla_amplada/2, pantalla_alçada + 45], 100, pantalla_amplada*3, False, 0,2, llista_objectes_rectangulars,pantalla)
paret_dreta = caixa([pantalla_amplada*2+100, -pantalla_alçada*0.25+30],300, pantalla_alçada*2.5, False, 90,2, llista_objectes_rectangulars,pantalla)
paret_esquerra = caixa([terra.rectangle.left, pantalla_alçada/2 -250],300, pantalla_alçada+600, False, 90,2, llista_objectes_rectangulars,pantalla)
quadrat_petit = caixa([pantalla_amplada - 255, pantalla_alçada-48], 50, 50, True, 0,3, llista_objectes_rectangulars,pantalla)
rectangle_petit = caixa([pantalla_amplada - 230, pantalla_alçada-175], 20, 70, True, 90,2, llista_objectes_rectangulars,pantalla)
rectangle_petit_2 = caixa([pantalla_amplada - 230, pantalla_alçada-175], 20, 70, True, 90,1, llista_objectes_rectangulars,pantalla)
rectangle_normal = caixa([pantalla_amplada - 180, pantalla_alçada-245], 20, 150, True, 0,2, llista_objectes_rectangulars,pantalla)
quadrat_gran = caixa([pantalla_amplada - 180, pantalla_alçada-315], 60, 60, True, 0,1, llista_objectes_rectangulars,pantalla)
quadrat_gran_2 = caixa([pantalla_amplada - 180, pantalla_alçada-315], 60, 60, True, 0,2, llista_objectes_rectangulars,pantalla)
quadrat_gran_3 = caixa([pantalla_amplada - 180, pantalla_alçada-315], 60, 60, True, 0,3, llista_objectes_rectangulars,pantalla)
rectangle_gran = caixa([pantalla_amplada - 180, pantalla_alçada-105], 20, 200, True, 0,2, llista_objectes_rectangulars,pantalla)
rectangle_gran_3 = caixa([pantalla_amplada - 180, pantalla_alçada-105], 20, 200, True, 0,1, llista_objectes_rectangulars,pantalla)
rectangle_gran_2 = caixa([pantalla_amplada - 180, pantalla_alçada-105], 20, 400, True, 0,3, llista_objectes_rectangulars,pantalla)
tnt = caixa([pantalla_amplada - 280, pantalla_alçada-405], 50, 50, True, 0,5, llista_objectes_rectangulars,pantalla)

# Selecció de nivell
def selecció_nivell(estrelles):
    ratoli = False
    nivell_seleccionat = 1
    selecció_nivell_acabada = False
    sortir_selecció = False
    click = False
    polygon1 = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
    for i in polygon1:
        i*=0.45
        i +=(pantalla_amplada*46.5/50,pantalla_alçada/8.5)
    polygon2 = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
    for i in polygon2:
        i*=0.3
        i += (pantalla_amplada*46.5/50,pantalla_alçada/8.5)
    font = pygame.font.Font(None, 150)
    text1 = font.render("Nivells", True, taronja)
    numeros = [str(i) for i in range(1, 13)]
    textos = [font.render(num, True, taronja) for num in numeros]
    rectangle_esc = pygame.Rect(pantalla_amplada/20,pantalla_alçada/14, 140,90)
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
    while not selecció_nivell_acabada:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and nivell_seleccionat < 12:
                    pygame.mouse.set_visible(False)
                    ratoli = False 
                    nivell_seleccionat += 1
                elif event.key == pygame.K_LEFT and nivell_seleccionat > 1:
                    pygame.mouse.set_visible(False)
                    ratoli = False 
                    nivell_seleccionat -= 1
                elif event.key == pygame.K_DOWN and nivell_seleccionat < 12:
                    nivell_seleccionat += 4
                    pygame.mouse.set_visible(False)
                    ratoli = False 
                    if nivell_seleccionat > 12:
                        nivell_seleccionat = 12
                elif event.key == pygame.K_UP and nivell_seleccionat > 1:
                    nivell_seleccionat -= 4
                    pygame.mouse.set_visible(False)
                    ratoli = False 
                    if nivell_seleccionat < 1:
                        nivell_seleccionat = 1
                elif event.key == pygame.K_SPACE and llista_estrelles[nivell_seleccionat-1][1] == False:
                    if ratoli == False:    
                        selecció_nivell_acabada = True
                    else:
                        ratoli = False
                        pygame.mouse.set_visible(False)    
                elif event.key == pygame.K_ESCAPE:
                    selecció_nivell_acabada = True
                    sortir_selecció = True
                elif event.key == pygame.K_s:
                    for i in llista_estrelles:
                        i[1] = False
            elif event.type == pygame.MOUSEMOTION:
                ratoli = True
                pygame.mouse.set_visible(True)
            elif event.type == pygame.MOUSEBUTTONUP:
                if (ratoli and llista_estrelles[nivell_seleccionat-1][1] == False) or rectangle_esc.collidepoint(pygame.mouse.get_pos()):    
                    click = True
                else:
                    ratoli = True
                    pygame.mouse.set_visible(True)
        pantalla.blit(fons_2, (0,-pantalla_alçada*0.15))
        pantalla.blit(nivells_imatge, nivells_rect)
        # Crear una llista de textos de números de l'1 al 12
        for i, text in enumerate(textos):
            pos = posicions[i]
            estrella = llista_estrelles[i][0]
            nivell_bloquejat = llista_estrelles[i][1]
            if nivell_bloquejat:
                color1 = gris
                color2 = negre
            elif estrella == 3:
                color1 = verd
                color2 = verd_fosc
            elif estrella == 2:
                color1 = groc
                color2 = groc2
            elif estrella == 1:
                color1 = taronja
                color2 = taronja3
            elif estrella == 0:
                color1 = vermell
                color2 = vermell2
            num_text = font_gran.render(str(i+1), True, color2)
            if num_text.get_height() > num_text.get_width():
                amplada = num_text.get_height()*1.2
            else:
                amplada = num_text.get_width()*1.2
            if ratoli:
                rectangle = pygame.Rect((0,0), (amplada, amplada))
                rectangle.center = pos
                if rectangle.collidepoint(pygame.mouse.get_pos()):
                    num_text = pygame.transform.scale(num_text, (num_text.get_width()*1.2,num_text.get_height()*1.2))
                    amplada *=1.2
                    nivell_seleccionat = i+1
                    if click == True:
                        selecció_nivell_acabada = True
            else:     
                if nivell_seleccionat == i+1:
                    num_text = pygame.transform.scale(num_text, (num_text.get_width()*1.2,num_text.get_height()*1.2))
                    amplada *=1.2
            rectangle = pygame.Rect((0,0), (amplada, amplada))
            rectangle.center = pos
            pygame.draw.rect(pantalla, color1, rectangle)
            pygame.draw.rect(pantalla, color2, rectangle, 8)
            rectangle2 = num_text.get_rect(center = pos)
            pantalla.blit(num_text, rectangle2)
        if rectangle_esc.collidepoint(pygame.mouse.get_pos()):
            rectangle_esc_2 = pygame.Rect(pantalla_amplada/20,pantalla_alçada/14, 140*1.2,90*1.2)
            rectangle_esc_2.center = rectangle_esc.center
            fletxa_imatge_2 = pygame.transform.scale(fletxa_imatge,(140*1.2*0.8,90*1.2*0.8))
            if click:
                sortir_selecció = True
                selecció_nivell_acabada = True
            color2 = taronja
        else:
            fletxa_imatge_2 = pygame.transform.scale(fletxa_imatge,(140*0.8,90*0.8))
            rectangle_esc_2 = rectangle_esc
            color2 =(19,64,132)
        color = (29,86,172)
        rectangle_fletxa = fletxa_imatge_2.get_rect(center = rectangle_esc.center)
        pygame.draw.rect(pantalla, color, rectangle_esc_2)
        pygame.draw.rect(pantalla, color2, rectangle_esc_2,8)
        pantalla.blit(fletxa_imatge_2, rectangle_fletxa)
        font = pygame.font.Font(None, 130)
        text4 = font.render(str(estrelles-estrelles_gastades), True, taronja)
        pantalla.blit(text4, (pantalla_amplada*43/50 -text4.get_width()//2, pantalla_alçada/14))
        pygame.draw.polygon(pantalla, taronja3, polygon1)
        pygame.draw.polygon(pantalla, taronja, polygon2)
        pygame.display.flip()
    if sortir_selecció:
        return None
    else:
        return nivell_seleccionat

# Menú principal
def menú(estrelles):
    ratoli = False
    rectangle_x = pygame.Rect(pantalla_amplada/20,pantalla_alçada/14, 90,90)
    global nivell_actual
    posicions = [(pantalla_amplada * 1 // 4, pantalla_alçada * 4 // 5),
          (pantalla_amplada * 2 // 4, pantalla_alçada * 4 // 5),
          (pantalla_amplada * 3 // 4, pantalla_alçada * 4 // 5)]
    z = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
    for i in z:
        i*=0.45
        i +=(pantalla_amplada*46.5/50,pantalla_alçada/8.5)
    x = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
    for i in x:
        i*=0.3
        i += (pantalla_amplada*46.5/50,pantalla_alçada/8.5)
    nivell_seleccionat = 2
    imatges = {0:info_imatge, 1:play_imatge, 2: tenda_imatge}
    seleccionat = False
    selecció = 4
    imatge_títol = pygame.transform.scale(títol,(pantalla_amplada*0.9,pantalla_amplada*0.9*(70/717)))
    títol_rect = imatge_títol.get_rect(center = (pantalla_amplada//2, pantalla_alçada*2//5))
    while True:
        seleccionat = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    if ratoli == False:    
                        seleccionat = True
                    else:
                        ratoli = False
                        pygame.mouse.set_visible(False)
                elif event.key == pygame.K_i:
                    info()
                elif event.key == pygame.K_t:
                    aparença = tenda(estrelles)
                    if aparença != None:
                        if aparença == skin8:
                            invisible = True
                        else:
                            invisible = False
                        for i in llista_ocells:
                            i.posar_skin(aparença)
                            if invisible:
                                i.invisible = True
                            else:
                                i.invisible = False
                    else:
                        for i in llista_ocells:
                            i.treure_skin()
                elif event.key == pygame.K_RIGHT and nivell_seleccionat < 3:
                    pygame.mouse.set_visible(False)
                    ratoli = False
                    nivell_seleccionat += 1
                elif event.key == pygame.K_LEFT and nivell_seleccionat > 1:
                    ratoli = False
                    pygame.mouse.set_visible(False) 
                    nivell_seleccionat -= 1
            elif event.type == pygame.MOUSEMOTION:
                ratoli = True
                pygame.mouse.set_visible(True)
            elif event.type == pygame.MOUSEBUTTONUP:
                if ratoli:    
                    seleccionat = True
                else:
                    ratoli = True
                    pygame.mouse.set_visible(True)
        pantalla.blit(fons_2, (0,-pantalla_alçada*0.15))
        pantalla.blit(imatge_títol, títol_rect)
        font = pygame.font.Font(None, 130)
        text4 = font.render(str(estrelles-estrelles_gastades), True, taronja)
        pantalla.blit(text4, (pantalla_amplada*43/50-text4.get_width()//2, pantalla_alçada/14))
        pygame.draw.polygon(pantalla, taronja3, z)
        pygame.draw.polygon(pantalla, taronja, x)
        for i in range(0,3):
            pos = posicions[i]
            amplada = 130
            color1 = (29,86,172)
            color2 =(19,64,132)
            if ratoli:    
                rectangle = pygame.Rect((0,0), (amplada, amplada))
                rectangle.center = pos
                if rectangle.collidepoint(pygame.mouse.get_pos()):
                    nivell_seleccionat = i+1
                    amplada *=1.2
                    color2 = taronja
                    if seleccionat:
                        selecció = i
            else:
                if nivell_seleccionat == i+1:
                    amplada *=1.2
                    color2 = taronja
                    if seleccionat:
                        selecció = i
            imatge = imatges[i]
            imatge = pygame.transform.scale(imatge, (amplada*0.8,amplada*0.8))
            rectangle2 = imatge.get_rect(center = pos)
            rectangle = pygame.Rect((0,0), (amplada, amplada))
            rectangle.center = pos
            pygame.draw.rect(pantalla, color1, rectangle)
            pygame.draw.rect(pantalla, color2, rectangle, 8)
            pantalla.blit(imatge, rectangle2)
        if rectangle_x.collidepoint(pygame.mouse.get_pos()) and ratoli:
            rectangle_x_2 = pygame.Rect(pantalla_amplada/20,pantalla_alçada/14, 90*1.2,90*1.2)
            rectangle_x_2.center = rectangle_x.center
            x_imatge_2 = pygame.transform.scale(x_imatge,(90*1.2*0.8,90*1.2*0.8))
            if seleccionat:
                return False
            color2 = taronja
        else:
            x_imatge_2 = pygame.transform.scale(x_imatge,(90*0.8,90*0.8))
            rectangle_x_2 = rectangle_x
            color2 =(19,64,132)
        color = (29,86,172)
        rectangle_x_3 = x_imatge_2.get_rect(center = rectangle_x.center)
        pygame.draw.rect(pantalla, color, rectangle_x_2)
        pygame.draw.rect(pantalla, color2, rectangle_x_2,8)
        pantalla.blit(x_imatge_2, rectangle_x_3)
        if seleccionat:
            if selecció == 0:
                info()
            elif selecció == 1:
                dificultat = selecció_nivell(estrelles)
                if dificultat:
                    nivell_actual = dificultat
                    pygame.mouse.set_visible(True)
                    return True
            elif selecció == 2:
                aparença = tenda(estrelles)
                if aparença != None:
                    if aparença == skin8:
                        invisible = True
                    else:
                        invisible = False
                    for i in llista_ocells:
                        i.posar_skin(aparença)
                        if invisible:
                            i.invisible = True
                        else:
                            i.invisible = False
                else:
                    for i in llista_ocells:
                        i.treure_skin()
            seleccionat = False
            selecció = 4
        pygame.display.flip()
def info():
    global nivell_actual
    diferencia = 0
    rectangle_esc = pygame.Rect(pantalla_amplada/20,pantalla_alçada/14, 140,90)
    font = pygame.font.Font(None, 90)
    text = font.render("Camara", True, taronja)
    text5 = font.render("Astres espacials", True, taronja)
    text9 = font.render("Altres objectes", True, taronja)
    text15 = font.render("Objectiu", True, taronja)
    text16 = font.render("Tenda i nivells", True, taronja)
    font = pygame.font.Font(None, 35)
    text17 = font.render("L'objectiu de GALACTIC PIUS és destruir tots els planetes que estan intentant", True, taronja)
    text18 = font.render("suplantar a la Terra. Per tal d'aconseguir aquest objectiu tiraras diferents astres", True, taronja)
    text19 = font.render("espacials a aquests planetes.", True, taronja)
    text2 = font.render("Al començar un nivell, la camara anirà a la part que no és veu. Per ha anar al", True, taronja)
    text3 = font.render("tiratxines pren espai. La camara al llançar un objecte el seguira. Per poder veure el", True, taronja)
    text4 = font.render("mapa amb llibertat utilitza el ratoli, per tornar al tiratxines pren espai un altre", True, taronja)
    text14 = font.render("cop. Alhora de mantenir un astre es farà un zoom out per tal de facilitçar apuntar.", True, taronja)
    text6 = font.render("Per llançar un astre espacial arrastra'l amb el ratoli i deixa'l anar. Alguns astres", True, taronja)
    text7 = font.render("tenen una habilitat especial que s'activa al fer click quan estan en el aire. Els", True, taronja)
    text8 = font.render("astres poden destruir caixes i eliminar planetes Terra.", True, taronja)
    text10 = font.render("Els planetes són l'objectiu d'aquest joc, guanyes el nivell quan has eliminat a tots.", True, taronja)
    text11 = font.render("Les caixes són obstacles que estan protegint als planetes. Hi han de diferents tipos,", True, taronja)
    text12 = font.render("les de pedra són les més difícils de trencar, mentre que les de vidre les més fàcils.", True, taronja)
    text13 = font.render(" La TNT explota al xocar-se.", True, taronja)
    text20 = font.render("La tenda és el lloc on has d'anar si vols personalitzar els teus personatges. Funciona,", True, taronja)
    text21 = font.render("mitjançant estrelles que conseguiras al acabar cada nivell. Depenent de la teva habilitat.", True, taronja)
    text22 = font.render("conseguiras entre 1 i 3 estrelles. Per saber cuantes estrelles tens en un nivell ", True, taronja)
    text23 = font.render("mira el color del icono. Cada objecte de la tenda és una skin per a tots els personatges. ", True, taronja)
    textos =  [text17, text18, text19, text5, text6, text7, text8, text9, text10, text11, text12, text13, text16, text20, text21, text22, text23, text,text2, text3, text4, text14, ]
    while True:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            elif event.type == pygame.MOUSEWHEEL:
                diferencia -= event.x*20
                diferencia += event.y*20
                if diferencia >0:
                    diferencia = 0
                if diferencia< -440:
                    diferencia = -440
            elif event.type == pygame.MOUSEBUTTONUP:
                click = True
        rectangle1 = pygame.Rect(text.get_width()*0.2+30, text.get_height()*1.6+diferencia-10+100, 1050, 170)
        rectangle2 = pygame.Rect(text.get_width()*0.2+30, text.get_height()*2.6 +text2.get_height()*5+diferencia-10+100, 1030, 170)
        rectangle3 = pygame.Rect(text.get_width()*0.2+30, text.get_height()*2.6*2.2 +text2.get_height()*5+diferencia-10+100, 1060, 195)
        rectangle4 = pygame.Rect(text.get_width()*0.2+30, text.get_height()*2.6*3.5 +text2.get_height()*5+diferencia-10+100, 1130, 195)
        rectangle5 = pygame.Rect(text.get_width()*0.2+30, text.get_height()*2.6*4.8 +text2.get_height()*5+diferencia-10+100, 1070, 195)
        rectangles = [rectangle1, rectangle2, rectangle3, rectangle4, rectangle5]
        pantalla.blit(fons_2, (0,-pantalla_alçada*0.1+diferencia*0.1))
        for i in rectangles:
            pygame.draw.rect(pantalla, (29,86,172), i)
            pygame.draw.rect(pantalla, (19,64,132), i,8)
        a = 1
        b = -1
        pantalla.blit(text15, (text.get_width()*0.2+50, text.get_height()*1.6+diferencia+100))
        for i in textos:
            if i.get_height() > text2.get_height()+1:
                amplada = text.get_width()*0.2
                b += 3
            else:
                b+=1
                amplada = 90
            pantalla.blit(i, (amplada+50, text.get_height()*2.6*a +text2.get_height()*b+diferencia+100))
            if i.get_height() > text2.get_height()+1:
                amplada = text.get_width()*0.2
                if b == 5:    
                    a+=1.2
                else:
                    a+=1.3
                b = -1
        rectangle_esc_2 = rectangle_esc.copy()
        rectangle_esc_2.center += pygame.math.Vector2(0,diferencia)
        if rectangle_esc_2.collidepoint(pygame.mouse.get_pos()):
            rectangle_esc_2 = pygame.Rect(pantalla_amplada/20,pantalla_alçada/14, 140*1.2,90*1.2)
            rectangle_esc_2.center = rectangle_esc.center
            fletxa_imatge_2 = pygame.transform.scale(fletxa_imatge,(140*1.2*0.8,90*1.2*0.8))
            rectangle_esc_2.center += pygame.math.Vector2(0,diferencia)
            if click:
                return False
            color2 = taronja
        else:
            fletxa_imatge_2 = pygame.transform.scale(fletxa_imatge,(140*0.8,90*0.8))
            color2 =(19,64,132)
        color = (29,86,172)
        rectangle_fletxa = fletxa_imatge_2.get_rect(center = rectangle_esc.center)
        rectangle_fletxa.center += pygame.math.Vector2(0,diferencia)
        pygame.draw.rect(pantalla, color, rectangle_esc_2)
        pygame.draw.rect(pantalla, color2, rectangle_esc_2,8)
        pantalla.blit(fletxa_imatge_2, rectangle_fletxa)
        info_rect2 = info_rect.copy()
        info_rect2.center += pygame.math.Vector2(0,diferencia)
        pantalla.blit(info_imatges, info_rect2)    
        pygame.display.flip()
def pantalla_final_victoria(estrelles, estrelles2):
    ratoli = False
    global nivell_actual
    posicions = [(pantalla_amplada * 1 // 4, pantalla_alçada * 5 // 6),
          (pantalla_amplada * 2 // 4, pantalla_alçada * 5 // 6),
          (pantalla_amplada * 3 // 4, pantalla_alçada * 5 // 6)]
    nivell_seleccionat = 2
    imatges = {0:home_imatge, 1:play_imatge, 2: repetir_imatge}
    seleccionat = False
    selecció = 4
    final = True
    font4 = pygame.font.Font(None, 130)
    z2 = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
    for i in z2:
        i*=0.45
        i +=(pantalla_amplada*46.5/50,pantalla_alçada/8.5)
    x2 = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
    for i in x2:
        i*=0.3
        i += (pantalla_amplada*46.5/50,pantalla_alçada/8.5)
    text4 = font4.render(str(estrelles2-estrelles_gastades), True, taronja)
    while final:
        seleccionat = False
        color = estrelles
        n = 3
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    y = False
                    final = False
                elif event.key == pygame.K_r:
                    final = False
                    seleccionat = True
                    selecció = 2
                elif event.key == pygame.K_SPACE:
                    if ratoli == False:    
                        seleccionat = True
                    else:
                        ratoli = False
                        pygame.mouse.set_visible(False)
                elif event.key == pygame.K_RIGHT and nivell_seleccionat < 3:
                    pygame.mouse.set_visible(False)
                    ratoli = False
                    nivell_seleccionat += 1
                elif event.key == pygame.K_LEFT and nivell_seleccionat > 1:
                    ratoli = False
                    pygame.mouse.set_visible(False) 
                    nivell_seleccionat -= 1
            elif event.type == pygame.MOUSEMOTION:
                ratoli = True
                pygame.mouse.set_visible(True)
            elif event.type == pygame.MOUSEBUTTONUP:
                if ratoli:    
                    seleccionat = True
                else:
                    ratoli = True
                    pygame.mouse.set_visible(True)
        pantalla.blit(fons_2, (0,-pantalla_alçada*0.15))
        pantalla.blit(victoria_imatge, victoria_rect)
        while n >0:
            if color >0:
                color_estrella = taronja
            else:
                color_estrella = gris
            z = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
            x = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
            for i in z:
                i*=1.3
                i +=(pantalla_amplada*(3-n)/3+225,pantalla_alçada/1.8)
            for i in x:
                i += (pantalla_amplada*(3-n)/3+225,pantalla_alçada/1.8)
            pygame.draw.polygon(pantalla, taronja3, z)
            pygame.draw.polygon(pantalla, color_estrella, x)
            n-=1
            color-=1
        for i in range(0,3):
            pos = posicions[i]
            amplada = 130
            color1 = (29,86,172)
            color2 =(19,64,132)
            if ratoli:    
                rectangle = pygame.Rect((0,0), (amplada, amplada))
                rectangle.center = pos
                if rectangle.collidepoint(pygame.mouse.get_pos()):
                    nivell_seleccionat = i+1
                    amplada *=1.2
                    color2 = taronja
                    if seleccionat:
                        selecció = i
            else:
                if nivell_seleccionat == i+1:
                    amplada *=1.2
                    color2 = taronja
                    if seleccionat:
                        selecció = i
            imatge = imatges[i]
            imatge = pygame.transform.scale(imatge, (amplada*0.8,amplada*0.8))
            rectangle2 = imatge.get_rect(center = pos)
            rectangle = pygame.Rect((0,0), (amplada, amplada))
            rectangle.center = pos
            pygame.draw.rect(pantalla, color1, rectangle)
            pygame.draw.rect(pantalla, color2, rectangle, 8)
            pantalla.blit(imatge, rectangle2)
        pantalla.blit(text4, (pantalla_amplada*43/50-text4.get_width()//2, pantalla_alçada/14))
        pygame.draw.polygon(pantalla, taronja3, z2)
        pygame.draw.polygon(pantalla, taronja, x2)
        pygame.display.flip()
        if seleccionat:
            if selecció == 0:
                y = False
                final = False
            elif selecció == 1:
                y = True
                final = False
                nivell_actual +=1
            elif selecció == 2:
                y = True
                final = False
    return y
def pantalla_final_derrota(estrelles2):
    ratoli = False
    posicions = [(pantalla_amplada * 1 // 3, pantalla_alçada * 5 // 6),
          (pantalla_amplada * 2 // 3, pantalla_alçada * 5 // 6)]
    nivell_seleccionat = 2
    imatges = {0:home_imatge, 1: repetir_imatge}
    seleccionat = False
    selecció = 4
    final = True
    font4 = pygame.font.Font(None, 130)
    z2 = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
    for i in z2:
        i*=0.45
        i +=(pantalla_amplada*46.5/50,pantalla_alçada/8.5)
    x2 = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
    for i in x2:
        i*=0.3
        i += (pantalla_amplada*46.5/50,pantalla_alçada/8.5)
    text4 = font4.render(str(estrelles2-estrelles_gastades), True, taronja)
    while final:
        seleccionat = False
        n = 3
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    y = False
                    final = False
                elif event.key == pygame.K_r:
                    final = False
                    seleccionat = True
                    selecció = 1
                elif event.key == pygame.K_SPACE:
                    if ratoli == False:    
                        seleccionat = True
                    else:
                        ratoli = False
                        pygame.mouse.set_visible(False)
                elif event.key == pygame.K_RIGHT and nivell_seleccionat < 2:
                    pygame.mouse.set_visible(False)
                    ratoli = False
                    nivell_seleccionat += 1
                elif event.key == pygame.K_LEFT and nivell_seleccionat > 1:
                    ratoli = False
                    pygame.mouse.set_visible(False) 
                    nivell_seleccionat -= 1
            elif event.type == pygame.MOUSEMOTION:
                ratoli = True
                pygame.mouse.set_visible(True)
            elif event.type == pygame.MOUSEBUTTONUP:
                if ratoli:    
                    seleccionat = True
                else:
                    ratoli = True
                    pygame.mouse.set_visible(True)
        pantalla.blit(fons_2, (0,-pantalla_alçada*0.15))
        pantalla.blit(derrota_imatge, derrota_rect)
        while n >0:
            color_estrella = gris
            z = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
            x = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
            for i in z:
                i*=1.3
                i +=(pantalla_amplada*(3-n)/3+225,pantalla_alçada/1.8)
            for i in x:
                i += (pantalla_amplada*(3-n)/3+225,pantalla_alçada/1.8)
            pygame.draw.polygon(pantalla, taronja3, z)
            pygame.draw.polygon(pantalla, color_estrella, x)
            n-=1
        for i in range(0,2):
            pos = posicions[i]
            amplada = 130
            color1 = (29,86,172)
            color2 =(19,64,132)
            if ratoli:    
                rectangle = pygame.Rect((0,0), (amplada, amplada))
                rectangle.center = pos
                if rectangle.collidepoint(pygame.mouse.get_pos()):
                    nivell_seleccionat = i+1
                    amplada *=1.2
                    color2 = taronja
                    if seleccionat:
                        selecció = i
            else:
                if nivell_seleccionat == i+1:
                    amplada *=1.2
                    color2 = taronja
                    if seleccionat:
                        selecció = i
            imatge = imatges[i]
            imatge = pygame.transform.scale(imatge, (amplada*0.8,amplada*0.8))
            rectangle2 = imatge.get_rect(center = pos)
            rectangle = pygame.Rect((0,0), (amplada, amplada))
            rectangle.center = pos
            pygame.draw.rect(pantalla, color1, rectangle)
            pygame.draw.rect(pantalla, color2, rectangle, 8)
            pantalla.blit(imatge, rectangle2)
        pantalla.blit(text4, (pantalla_amplada*43/50-text4.get_width()//2, pantalla_alçada/14))
        pygame.draw.polygon(pantalla, taronja3, z2)
        pygame.draw.polygon(pantalla, taronja, x2)
        pygame.display.flip()
        if seleccionat:
            if selecció == 0:
                y = False
                final = False
            elif selecció == 1:
                y = True
                final = False
    return y
def tenda(estrelles):
    tenda = True
    ratoli = False
    global estrelles_gastades
    global posar_tick
    global posicio_tick
    global imatge_skin
    nivell_seleccionat = 1
    font = pygame.font.Font(None, 130)
    z = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
    for i in z:
        i*=0.45
        i +=(pantalla_amplada*46.5/50,pantalla_alçada/8.5)
    x = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
    for i in x:
        i*=0.3
        i += (pantalla_amplada*46.5/50,pantalla_alçada/8.5)
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
    compra = False
    rectangle_esc = pygame.Rect(pantalla_amplada/20,pantalla_alçada/14, 140,90)
    while tenda:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    tenda = False
                elif event.key == pygame.K_SPACE:
                    if ratoli == False:    
                        compra = True
                    else:
                        ratoli = False
                        pygame.mouse.set_visible(False)
                elif event.key == pygame.K_RIGHT and nivell_seleccionat < 12:
                    ratoli = False
                    pygame.mouse.set_visible(False) 
                    nivell_seleccionat += 1
                elif event.key == pygame.K_LEFT and nivell_seleccionat > 1:
                    ratoli = False
                    pygame.mouse.set_visible(False) 
                    nivell_seleccionat -= 1
                elif event.key == pygame.K_DOWN and nivell_seleccionat < 12:
                    ratoli = False
                    pygame.mouse.set_visible(False) 
                    nivell_seleccionat += 4
                    if nivell_seleccionat > 12:
                        nivell_seleccionat = 12
                elif event.key == pygame.K_UP and nivell_seleccionat > 1:
                    ratoli = False
                    pygame.mouse.set_visible(False) 
                    nivell_seleccionat -= 4
                    if nivell_seleccionat < 1:
                        nivell_seleccionat = 1
            elif event.type == pygame.MOUSEMOTION:
                ratoli = True
                pygame.mouse.set_visible(True)
            elif event.type == pygame.MOUSEBUTTONUP:
                if ratoli:    
                    compra = True
                else:
                    ratoli = True
                    pygame.mouse.set_visible(True)
        pantalla.blit(fons_2, (0,-pantalla_alçada*0.15))
        text4 = font.render(str(estrelles-estrelles_gastades), True, taronja)
        pantalla.blit(text4, (pantalla_amplada*43/50 -text4.get_width()//2, pantalla_alçada/14))
        pantalla.blit(tendas_imatg, tendas_rect)
        pygame.draw.polygon(pantalla, taronja3, z)
        pygame.draw.polygon(pantalla, taronja, x)
        if rectangle_esc.collidepoint(pygame.mouse.get_pos()):
            rectangle_esc_2 = pygame.Rect(pantalla_amplada/20,pantalla_alçada/14, 140*1.2,90*1.2)
            rectangle_esc_2.center = rectangle_esc.center
            fletxa_imatge_2 = pygame.transform.scale(fletxa_imatge,(140*1.2*0.8,90*1.2*0.8))
            if compra:
                tenda = False
            color2 = taronja
        else:
            fletxa_imatge_2 = pygame.transform.scale(fletxa_imatge,(140*0.8,90*0.8))
            rectangle_esc_2 = rectangle_esc
            color2 =(19,64,132)
        color = (29,86,172)
        rectangle_fletxa = fletxa_imatge_2.get_rect(center = rectangle_esc.center)
        pygame.draw.rect(pantalla, color, rectangle_esc_2)
        pygame.draw.rect(pantalla, color2, rectangle_esc_2,8)
        pantalla.blit(fletxa_imatge_2, rectangle_fletxa)
        for i, text in enumerate(textos):
            pos = posicions[i]
            comprat = llista_objectes_comprats[i][0]
            numero = llista_objectes_comprats[i][1]
            if comprat:
                color1 = blau
                color2 = blau_fosc
            elif int(estrelles- estrelles_gastades)<numero:
                color1 = vermell
                color2 = vermell2
            else:
                color1 = verd
                color2 = verd_fosc
            num_text = font_gran.render(str(numero), True, blanc)
            if num_text.get_height() > num_text.get_width():
                amplada = num_text.get_height()*1.2
            else:
                amplada = num_text.get_width()*1.2
            if ratoli:
                rectangle = pygame.Rect((0,0), (amplada, amplada))
                rectangle.center = pos
                if rectangle.collidepoint(pygame.mouse.get_pos()):
                    num_text = pygame.transform.scale(num_text, (num_text.get_width()*1.2,num_text.get_height()*1.2))
                    amplada *=1.2
                    if compra == True:
                        compra = False
                        if color1 == verd:
                            estrelles_gastades += numero
                            llista_objectes_comprats[i][0] = True
                        if color1 == verd or color1 == blau:    
                            if posicio_tick != pos or posar_tick == False:
                                posar_tick = True
                                imatge_skin = llista_objectes_comprats[i][2]
                            else:
                                posar_tick = False
                                imatge_skin = None
                            posicio_tick = pos
                    nivell_seleccionat = i+1
            else:    
                if nivell_seleccionat == i+1:
                    num_text = pygame.transform.scale(num_text, (num_text.get_width()*1.2,num_text.get_height()*1.2))
                    amplada *=1.2
                    if compra == True:
                        compra = False
                        if color1 == verd:
                            estrelles_gastades += numero
                            llista_objectes_comprats[i][0] = True
                        if color1 == verd or color1 == blau:    
                            if posicio_tick != pos or posar_tick == False:
                                posar_tick = True
                                imatge_skin = llista_objectes_comprats[i][2]
                            else:
                                posar_tick = False
                                imatge_skin = None
                            posicio_tick = pos

            rectangle = pygame.Rect((0,0), (amplada, amplada))
            rectangle.center = pos
            pygame.draw.rect(pantalla, color1, rectangle)
            pygame.draw.rect(pantalla, color2, rectangle, 8)
            rectangle2 = num_text.get_rect(center = pos)
            imatge_compra = pygame.transform.scale(llista_objectes_comprats[i][2],(amplada,amplada))
            rectangle3 = imatge_compra.get_rect(center = pos)
            if i != 11:    
                rectangle3.center += pygame.math.Vector2(0,18) 
            pantalla.blit(imatge_compra, rectangle3)
            if color1 != blau:
                if ratoli:
                    if rectangle.collidepoint(pygame.mouse.get_pos()): 
                        pantalla.blit(num_text, rectangle2)   
                else:
                    if nivell_seleccionat == i+1:
                        pantalla.blit(num_text, rectangle2)
            if posar_tick and posicio_tick == pos:
                tick_2 = pygame.transform.scale(tick_imatge,(amplada/2,amplada/2))
                pantalla.blit(tick_2,posicio_tick)
        pygame.display.flip()
    return imatge_skin
def pausa():
    ratoli = True
    posicions = [(pantalla_amplada * 1 // 4, pantalla_alçada * 5 // 8),
          (pantalla_amplada * 2 // 4, pantalla_alçada * 5 // 8),
          (pantalla_amplada * 3 // 4, pantalla_alçada * 5 // 8)]
    nivell_seleccionat = 2
    imatges = {0:home_imatge, 1:play_imatge, 2: repetir_imatge}
    seleccionat = False
    selecció = 4
    pausat = True
    rectangle_p = pygame.Rect(0,0,pantalla_amplada*0.7,pantalla_alçada*0.5)
    p = pygame.Surface((pantalla_amplada*0.7,pantalla_alçada*0.5))
    pygame.draw.rect(p,(227,227,208),rectangle_p)
    llista_craters = []
    for i in range(int(pantalla_amplada*0.7*pantalla_alçada*0.5/10000)+1):
        random_amplada = random.randint(40, 80)
        random_alçada = random.randint(random_amplada-10, random_amplada+10)
        random_x = random.randint(-random_amplada, int(pantalla_amplada*0.7+ random_amplada))
        random_y = random.randint(-random_alçada, int(pantalla_alçada*0.5+ random_alçada))
        pygame.draw.ellipse(p, gris,(random_x,random_y, random_amplada, random_alçada))
        llista_craters.append((random_x, random_y, random_amplada, random_alçada))
    for i in llista_craters:
        pygame.draw.ellipse(p, pedra,(i[0]+5,i[1]+5, i[2]-10,i[3]-10))
    pygame.draw.rect(p,gris,rectangle_p,8)
    rectangle_p.center = (pantalla_amplada/2,pantalla_alçada/2)
    while pausat:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    y = False
                    pausat = False
                elif event.key == pygame.K_r:
                    pausat = False
                    seleccionat = True
                    selecció = 2
                elif event.key == pygame.K_SPACE:
                    if ratoli == False:    
                        seleccionat = True
                    else:
                        ratoli = False
                        pygame.mouse.set_visible(False)
                elif event.key == pygame.K_RIGHT and nivell_seleccionat < 3:
                    pygame.mouse.set_visible(False)
                    ratoli = False
                    nivell_seleccionat += 1
                elif event.key == pygame.K_LEFT and nivell_seleccionat > 1:
                    ratoli = False
                    pygame.mouse.set_visible(False) 
                    nivell_seleccionat -= 1
            elif event.type == pygame.MOUSEMOTION:
                ratoli = True
                pygame.mouse.set_visible(True)
            elif event.type == pygame.MOUSEBUTTONUP:
                if ratoli:    
                    seleccionat = True
                else:
                    ratoli = True
                    pygame.mouse.set_visible(True)
        pantalla.blit(p, rectangle_p)
        pantalla.blit(pausas_imatg, pausas_rect)
        for i in range(0,3):
            pos = posicions[i]
            amplada = 130
            color1 = (29,86,172)
            color2 =(19,64,132)
            if ratoli:    
                rectangle = pygame.Rect((0,0), (amplada, amplada))
                rectangle.center = pos
                if rectangle.collidepoint(pygame.mouse.get_pos()):
                    nivell_seleccionat = i+1
                    amplada *=1.2
                    color2 = taronja
                    if seleccionat:
                        selecció = i
            else:
                if nivell_seleccionat == i+1:
                    amplada *=1.2
                    color2 = taronja
                    if seleccionat:
                        selecció = i
            imatge = imatges[i]
            imatge = pygame.transform.scale(imatge, (amplada*0.8,amplada*0.8))
            rectangle2 = imatge.get_rect(center = pos)
            rectangle = pygame.Rect((0,0), (amplada, amplada))
            rectangle.center = pos
            pygame.draw.rect(pantalla, color1, rectangle)
            pygame.draw.rect(pantalla, color2, rectangle, 8)
            pantalla.blit(imatge, rectangle2)
        pygame.display.flip()
        if seleccionat:
            if selecció == 0:
                y = False
                pausat = False
            elif selecció == 1:
                y = True
                pausat = False
            elif selecció == 2:
                reinici()
                y = True
                pausat = False
        seleccionat = False
    pygame.mouse.set_visible(True)
    return y
#Definim reinici al sortir del nivell
def reinici():
    global llista_objectes_pantalla
    global sprites
    global llista_ocells_llançats
    global total_estrelles
    for i in sprites:
        i.reinici()
    llista_objectes_pantalla = [terra, paret_dreta, paret_esquerra]
    sprites = [terra]
    llista_ocells_llançats = [no_ocell]
    camara.diferencia *= 0 
    camara.rectangle_camara.topleft = camara.rectangle_camara_orig
    camara.principi_nivell = True
    total_estrelles = 0
    for i in llista_estrelles:
        total_estrelles+=i[0]

#Definim camera
camara = camera(pantalla_amplada, pantalla_alçada, pantalla)
#Defimin nivells
ocells6 = [estrella.copy(llista_ocells, llista_objectes_rodons),estrella.copy(llista_ocells, llista_objectes_rodons),estrella.copy(llista_ocells, llista_objectes_rodons),vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells1 = [vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons),vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells3 = [racista.copy(llista_ocells, llista_objectes_rodons),racista.copy(llista_ocells, llista_objectes_rodons),racista.copy(llista_ocells, llista_objectes_rodons),vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells4 = [pequeñin.copy(llista_ocells, llista_objectes_rodons),pequeñin.copy(llista_ocells, llista_objectes_rodons),pequeñin.copy(llista_ocells, llista_objectes_rodons),pequeñin.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells5 = [racista.copy(llista_ocells, llista_objectes_rodons), racista.copy(llista_ocells, llista_objectes_rodons), pequeñin.copy(llista_ocells, llista_objectes_rodons), racista.copy(llista_ocells, llista_objectes_rodons), racista.copy(llista_ocells, llista_objectes_rodons), pequeñin.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells2 = [vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), racista.copy(llista_ocells, llista_objectes_rodons), racista.copy(llista_ocells, llista_objectes_rodons)]  
ocells7 = [bombardero.copy(llista_ocells, llista_objectes_rodons), bombardero.copy(llista_ocells, llista_objectes_rodons), bombardero.copy(llista_ocells, llista_objectes_rodons),bombardero.copy(llista_ocells, llista_objectes_rodons),bombardero.copy(llista_ocells, llista_objectes_rodons), bombardero.copy(llista_ocells, llista_objectes_rodons), bombardero.copy(llista_ocells, llista_objectes_rodons),  bombardero.copy(llista_ocells, llista_objectes_rodons)]
ocells8 = [racista.copy(llista_ocells,llista_objectes_rodons),racista.copy(llista_ocells,llista_objectes_rodons),pequeñin.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), pequeñin.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons),pequeñin.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons),pequeñin.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells9 = [vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells10 = [vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells11 = [vermellet.copy(llista_ocells, llista_objectes_rodons)]
ocells12 = [vermellet.copy(llista_ocells, llista_objectes_rodons), vermellet.copy(llista_ocells, llista_objectes_rodons)]
nivells_ocells = {1:ocells1, 2:ocells2, 3:ocells3, 4:ocells4, 5:ocells5, 6:ocells6, 7:ocells7, 8:ocells8, 9:ocells9, 10:ocells10, 11:ocells11, 12:ocells12}

nivell6 = [quadrat_petit.copy([pantalla_amplada - 405, pantalla_alçada-48], llista_objectes_rectangulars),quadrat_petit.copy([pantalla_amplada - 255, pantalla_alçada-48], llista_objectes_rectangulars),rectangle_petit.copy([pantalla_amplada - 380, pantalla_alçada-175], llista_objectes_rectangulars),rectangle_petit.copy([pantalla_amplada - 280, pantalla_alçada-175], llista_objectes_rectangulars),rectangle_normal.copy([pantalla_amplada - 330, pantalla_alçada-245], llista_objectes_rectangulars),quadrat_gran.copy([pantalla_amplada - 330, pantalla_alçada-315], llista_objectes_rectangulars),rectangle_gran.copy([pantalla_amplada - 330, pantalla_alçada-105], llista_objectes_rectangulars), porc_estandar.copy((pantalla_amplada - 330, pantalla_alçada - 160), llista_porcs, llista_objectes_rodons), quadrat_petit.copy([pantalla_amplada - 5, pantalla_alçada-48], llista_objectes_rectangulars),quadrat_petit.copy([pantalla_amplada + 145, pantalla_alçada-48], llista_objectes_rectangulars),rectangle_petit.copy([pantalla_amplada + 20, pantalla_alçada-175], llista_objectes_rectangulars),rectangle_petit.copy([pantalla_amplada +120, pantalla_alçada-175], llista_objectes_rectangulars),rectangle_normal.copy([pantalla_amplada +70, pantalla_alçada-245], llista_objectes_rectangulars),quadrat_gran.copy([pantalla_amplada +70, pantalla_alçada-315], llista_objectes_rectangulars),rectangle_gran.copy([pantalla_amplada +70, pantalla_alçada-105], llista_objectes_rectangulars), porc_estandar.copy((pantalla_amplada +70, pantalla_alçada - 160), llista_porcs, llista_objectes_rodons), quadrat_petit.copy([pantalla_amplada +395, pantalla_alçada-48], llista_objectes_rectangulars),quadrat_petit.copy([pantalla_amplada +545, pantalla_alçada-48], llista_objectes_rectangulars),rectangle_petit.copy([pantalla_amplada + 420, pantalla_alçada-175], llista_objectes_rectangulars),rectangle_petit.copy([pantalla_amplada +520, pantalla_alçada-175], llista_objectes_rectangulars),rectangle_normal.copy([pantalla_amplada + 470, pantalla_alçada-245], llista_objectes_rectangulars),quadrat_gran.copy([pantalla_amplada +470, pantalla_alçada-315], llista_objectes_rectangulars),rectangle_gran.copy([pantalla_amplada +470, pantalla_alçada-105], llista_objectes_rectangulars), porc_estandar.copy((pantalla_amplada +470, pantalla_alçada - 160), llista_porcs, llista_objectes_rodons), quadrat_petit.copy([pantalla_amplada + 795, pantalla_alçada-48], llista_objectes_rectangulars),quadrat_petit.copy([pantalla_amplada +945, pantalla_alçada-48], llista_objectes_rectangulars),rectangle_petit.copy([pantalla_amplada + 820, pantalla_alçada-175], llista_objectes_rectangulars),rectangle_petit.copy([pantalla_amplada + 920, pantalla_alçada-175], llista_objectes_rectangulars),rectangle_normal.copy([pantalla_amplada  + 870, pantalla_alçada-245], llista_objectes_rectangulars),quadrat_gran.copy([pantalla_amplada +870, pantalla_alçada-315], llista_objectes_rectangulars),rectangle_gran.copy([pantalla_amplada + 870, pantalla_alçada-105], llista_objectes_rectangulars), porc_estandar.copy((pantalla_amplada + 870, pantalla_alçada - 160), llista_porcs, llista_objectes_rodons)]
nivell1 = [porc_estandar.copy([pantalla_amplada+260, pantalla_alçada-265], llista_porcs, llista_objectes_rodons), porc_estandar.copy([pantalla_amplada- 140, pantalla_alçada-265], llista_porcs, llista_objectes_rodons), rectangle_petit.copy([pantalla_amplada + 295,pantalla_alçada-40], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada +295,pantalla_alçada-115], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada +295,pantalla_alçada-190], llista_objectes_rectangulars),rectangle_petit.copy([pantalla_amplada + 225,pantalla_alçada-40], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+225,pantalla_alçada-115], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+225,pantalla_alçada-190], llista_objectes_rectangulars), rectangle_normal.copy([pantalla_amplada + 260, pantalla_alçada-255], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada +25,pantalla_alçada-115], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+25,pantalla_alçada-190], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+95,pantalla_alçada-115], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+95,pantalla_alçada-190], llista_objectes_rectangulars), rectangle_normal.copy([pantalla_amplada+60, pantalla_alçada-255], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada- 105,pantalla_alçada-90], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada- 175,pantalla_alçada-90], llista_objectes_rectangulars), rectangle_normal.copy([pantalla_amplada- 140, pantalla_alçada-145], llista_objectes_rectangulars),tnt.copy([pantalla_amplada+60, pantalla_alçada-300], llista_objectes_rectangulars), porc_estandar.copy([pantalla_amplada+ 540, pantalla_alçada-265], llista_porcs, llista_objectes_rodons), porc_estandar.copy([pantalla_amplada+ 940, pantalla_alçada-265], llista_porcs, llista_objectes_rodons), rectangle_petit.copy([pantalla_amplada+ 505,pantalla_alçada-40], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 505,pantalla_alçada-115], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 505,pantalla_alçada-190], llista_objectes_rectangulars),rectangle_petit.copy([pantalla_amplada+ 575,pantalla_alçada-40], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 575,pantalla_alçada-115], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 575,pantalla_alçada-190], llista_objectes_rectangulars), rectangle_normal.copy([pantalla_amplada+ 540, pantalla_alçada-255], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 705,pantalla_alçada-115], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 705,pantalla_alçada-190], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 775,pantalla_alçada-115], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 775,pantalla_alçada-190], llista_objectes_rectangulars), rectangle_normal.copy([pantalla_amplada+ 740, pantalla_alçada-255], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 905,pantalla_alçada-90], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+ 975,pantalla_alçada-90], llista_objectes_rectangulars), rectangle_normal.copy([pantalla_amplada+ 940, pantalla_alçada-145], llista_objectes_rectangulars),tnt.copy([pantalla_amplada+ 740, pantalla_alçada-300], llista_objectes_rectangulars)]
nivell3 = [porc_estandar.copy((pantalla_amplada*0.75,pantalla_alçada-320), llista_porcs, llista_objectes_rodons), porc_estandar.copy((pantalla_amplada*1.05,pantalla_alçada-320), llista_porcs, llista_objectes_rodons), porc_estandar.copy((pantalla_amplada*1.5,pantalla_alçada-420), llista_porcs, llista_objectes_rodons), porc_estandar.copy((pantalla_amplada*1.75,pantalla_alçada-420), llista_porcs, llista_objectes_rodons),caixa([pantalla_amplada*1.6, pantalla_alçada-50], 100, pantalla_amplada*2, False, 0,2, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*0.51, pantalla_alçada*1.082+100], 200, pantalla_amplada/2.5, False, 45,2, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*2.4, pantalla_alçada-150], 200, pantalla_amplada*2, False, 0,2, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*1.31, pantalla_alçada*1.082-50], 200, pantalla_amplada/2.5, False, 45,2, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*0.75,pantalla_alçada-225], 20, 150, True, 90, 3, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*0.75,pantalla_alçada-310], 20, 100, True, 0, 3, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*1.05,pantalla_alçada-225], 20, 150, True, 90, 3, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*1.05,pantalla_alçada-310], 20, 100, True, 0, 3, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*1.5,pantalla_alçada-325], 20, 150, True, 90, 3, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*1.5,pantalla_alçada-410], 20, 100, True, 0, 3, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*1.75,pantalla_alçada-325], 20, 150, True, 90, 3, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*1.75,pantalla_alçada-410], 20, 100, True, 0, 3, llista_objectes_rectangulars,pantalla)]
nivell4 = [porc_estandar.copy((pantalla_amplada+80*-1, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80*2, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80*-2, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80*3, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80*-3, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80*4, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80*5, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80*6, pantalla_alçada-40), llista_porcs, llista_objectes_rodons), porc_estandar.copy((pantalla_amplada+80*7, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80*8, pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada+80, pantalla_alçada-40), llista_porcs, llista_objectes_rodons), porc_estandar.copy((pantalla_amplada, pantalla_alçada-40), llista_porcs, llista_objectes_rodons), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*2), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*3), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*4), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*5), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*6), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*7), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*8), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*9), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*10), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*11), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*12), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*0.75, pantalla_alçada-35-70*13), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*2), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*3), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*4), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*5), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*6), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*7), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*8), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*9), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*10), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*11), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*12), llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada*1.5, pantalla_alçada-35-70*13), llista_objectes_rectangulars)]
nivell5 = [porc_estandar.copy((pantalla_amplada*1.84-100,pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada*1.84-100,pantalla_alçada*0.75-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada*1.84-100,pantalla_alçada*0.4-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada*1.84-100,pantalla_alçada*0.05-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada*1.84-100,pantalla_alçada*-0.3 -40), llista_porcs, llista_objectes_rodons), caixa((pantalla_amplada, pantalla_alçada*0.5),30,500,False,0,1, llista_objectes_rectangulars,pantalla), caixa((pantalla_amplada, pantalla_alçada*-0.5),30,500,False,0,3, llista_objectes_rectangulars,pantalla), caixa((pantalla_amplada*1.84-100, pantalla_alçada*0.75),100,100, False,0,2, llista_objectes_rectangulars,pantalla), caixa((pantalla_amplada*1.84-100, pantalla_alçada*-0.3),100,100, False,0,2, llista_objectes_rectangulars,pantalla), caixa((pantalla_amplada*1.84-100, pantalla_alçada*0.05),100,100, False,0,2, llista_objectes_rectangulars,pantalla), caixa((pantalla_amplada*1.84-100, pantalla_alçada*0.4),100,100, False,0,2, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*1.84+100, 0],300, pantalla_alçada*2, False, 90,2, llista_objectes_rectangulars,pantalla)]
nivell2 = [porc_estandar.copy([pantalla_amplada + 260, pantalla_alçada-485-40], llista_porcs, llista_objectes_rodons), porc_estandar.copy([pantalla_amplada + 760, pantalla_alçada-485-40], llista_porcs, llista_objectes_rodons), porc_estandar.copy([pantalla_amplada + 960, pantalla_alçada-225-40], llista_porcs, llista_objectes_rodons),caixa((pantalla_amplada*1.6, pantalla_alçada-110),210,pantalla_amplada*0.75,False,0,2, llista_objectes_rectangulars,pantalla), rectangle_petit_2.copy((pantalla_amplada, pantalla_alçada-35),llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada, pantalla_alçada-35-70),llista_objectes_rectangulars), rectangle_petit_2.copy((pantalla_amplada, pantalla_alçada-35-70*2),llista_objectes_rectangulars), rectangle_gran_2.copy((pantalla_amplada*1.13,pantalla_alçada-215),llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada + 295,pantalla_alçada-270], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada +295,pantalla_alçada-345], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada +295,pantalla_alçada-420], llista_objectes_rectangulars),rectangle_petit.copy([pantalla_amplada + 225,pantalla_alçada-270], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+225,pantalla_alçada-345], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+225,pantalla_alçada-420], llista_objectes_rectangulars), rectangle_normal.copy([pantalla_amplada + 260, pantalla_alçada-485], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada + 795,pantalla_alçada-270], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada +795,pantalla_alçada-345], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada +795,pantalla_alçada-420], llista_objectes_rectangulars),rectangle_petit.copy([pantalla_amplada + 725,pantalla_alçada-270], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+725,pantalla_alçada-345], llista_objectes_rectangulars), rectangle_petit.copy([pantalla_amplada+725,pantalla_alçada-420], llista_objectes_rectangulars), rectangle_normal.copy([pantalla_amplada + 760, pantalla_alçada-485], llista_objectes_rectangulars), tnt.copy([pantalla_amplada+560, pantalla_alçada-265], llista_objectes_rectangulars)]
nivell7 = [caixa((pantalla_amplada,pantalla_alçada*0.19),20, pantalla_alçada*1.62, False,90,2,llista_objectes_rectangulars, pantalla),porc_estandar.copy((pantalla_amplada+215,pantalla_alçada-490), llista_porcs, llista_objectes_rodons), caixa((pantalla_amplada+137, pantalla_alçada*0.425+50),20+100,255, False,0,2, llista_objectes_rectangulars,pantalla), caixa((pantalla_amplada+137, pantalla_alçada*0.175),20,255, False,0,2, llista_objectes_rectangulars,pantalla), caixa((pantalla_amplada+85, pantalla_alçada*0.362),76,150, False,0,2, llista_objectes_rectangulars,pantalla), quadrat_gran_2.copy((pantalla_amplada+70,pantalla_alçada-600),llista_objectes_rectangulars), porc_estandar.copy((pantalla_amplada+215,pantalla_alçada-190), llista_porcs, llista_objectes_rodons), caixa((pantalla_amplada+137, pantalla_alçada*0.425+365),20+135,255, False,0,2, llista_objectes_rectangulars,pantalla), caixa((pantalla_amplada+137, pantalla_alçada*0.175+300),20,255, False,0,2, llista_objectes_rectangulars,pantalla), caixa((pantalla_amplada+85, pantalla_alçada*0.362+300),76,150, False,0,2, llista_objectes_rectangulars,pantalla), quadrat_gran_2.copy((pantalla_amplada+70,pantalla_alçada-300),llista_objectes_rectangulars),porc_estandar.copy((pantalla_amplada+215,pantalla_alçada-490-300), llista_porcs, llista_objectes_rodons), caixa((pantalla_amplada+137, pantalla_alçada*0.425-300+50),20+100,255, False,0,2, llista_objectes_rectangulars,pantalla), caixa((pantalla_amplada+137, pantalla_alçada*0.175-300),20,255, False,0,2, llista_objectes_rectangulars,pantalla), caixa((pantalla_amplada+85, pantalla_alçada*0.362-300),76,150, False,0,2, llista_objectes_rectangulars,pantalla), quadrat_gran_2.copy((pantalla_amplada+70,pantalla_alçada-600-300),llista_objectes_rectangulars),porc_estandar.copy((pantalla_amplada+215,pantalla_alçada-490-600), llista_porcs, llista_objectes_rodons), caixa((pantalla_amplada+137, pantalla_alçada*0.425-600+50),20+100,255, False,0,2, llista_objectes_rectangulars,pantalla), caixa((pantalla_amplada+137, pantalla_alçada*0.175-600),20,255, False,0,2, llista_objectes_rectangulars,pantalla), caixa((pantalla_amplada+85, pantalla_alçada*0.362-600),76,150, False,0,2, llista_objectes_rectangulars,pantalla), quadrat_gran_2.copy((pantalla_amplada+70,pantalla_alçada-600-600),llista_objectes_rectangulars), caixa((pantalla_amplada*1.58, 0), int(pantalla_amplada*0.8) , pantalla_alçada*2, False, 90, 2,llista_objectes_rectangulars,pantalla)]
nivell8 = [porc_estandar.copy((3000,pantalla_alçada-40), llista_porcs, llista_objectes_rodons), caixa((500, pantalla_alçada-100), 20, 200,False,10,5,llista_objectes_rectangulars,pantalla), caixa((700, pantalla_alçada-100), 20, 200,False,30,5,llista_objectes_rectangulars,pantalla), caixa((900, pantalla_alçada-100), 20, 200,False,50,5,llista_objectes_rectangulars,pantalla), caixa((1100, pantalla_alçada-100), 20, 200,False,70,5,llista_objectes_rectangulars,pantalla), caixa((1300, pantalla_alçada-100), 20, 200,False,90,5,llista_objectes_rectangulars,pantalla), caixa((1500, pantalla_alçada-100), 20, 200,False,110,5,llista_objectes_rectangulars,pantalla), caixa((1700, pantalla_alçada-100), 20, 200,False,130,5,llista_objectes_rectangulars,pantalla), caixa((1900, pantalla_alçada-100), 20, 200,False,150,5,llista_objectes_rectangulars,pantalla),  caixa((2100, pantalla_alçada-100), 20, 200,False,170,5,llista_objectes_rectangulars,pantalla),porc_estandar.copy((pantalla_amplada*1.84-100,pantalla_alçada*0.75-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada*1.84-100,pantalla_alçada*0.4-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada*1.84-100,pantalla_alçada*0.05-40), llista_porcs, llista_objectes_rodons),porc_estandar.copy((pantalla_amplada*1.84-100,pantalla_alçada*-0.3 -40), llista_porcs, llista_objectes_rodons), caixa((pantalla_amplada*1.84-100, pantalla_alçada*0.75),100,100, False,0,2, llista_objectes_rectangulars,pantalla), caixa((pantalla_amplada*1.84-100, pantalla_alçada*-0.3),100,100, False,0,2, llista_objectes_rectangulars,pantalla), caixa((pantalla_amplada*1.84-100, pantalla_alçada*0.05),100,100, False,0,2, llista_objectes_rectangulars,pantalla), caixa((pantalla_amplada*1.84-100, pantalla_alçada*0.4),100,100, False,0,2, llista_objectes_rectangulars,pantalla), caixa([pantalla_amplada*1.84+100, 0],300, pantalla_alçada*2, False, 90,2, llista_objectes_rectangulars,pantalla)]
nivell9 = [porc_movible.copy((1000,pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_movible.copy((1200,pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_movible.copy((1400,pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_movible.copy((1600,pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_movible.copy((1800,pantalla_alçada-40), llista_porcs, llista_objectes_rodons),porc_movible.copy((2000,pantalla_alçada-40), llista_porcs, llista_objectes_rodons), caixa((2400,pantalla_alçada-230),50,450,False,90,2,llista_objectes_rectangulars,pantalla), caixa((900,pantalla_alçada-230),50,450,False,90,2,llista_objectes_rectangulars,pantalla), caixa((1000, pantalla_alçada-500), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), caixa((1100, pantalla_alçada-500), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), rectangle_gran_3.copy((1050,pantalla_alçada-530),llista_objectes_rectangulars), quadrat_gran_3.copy((1050, pantalla_alçada-560),llista_objectes_rectangulars), caixa((1200, pantalla_alçada-700), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), caixa((1300, pantalla_alçada-700), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), rectangle_gran_3.copy((1250,pantalla_alçada-730),llista_objectes_rectangulars), quadrat_gran_3.copy((1250, pantalla_alçada-760),llista_objectes_rectangulars),caixa((1400, pantalla_alçada-500), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), caixa((1500, pantalla_alçada-500), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), rectangle_gran_3.copy((1450,pantalla_alçada-530),llista_objectes_rectangulars), quadrat_gran_3.copy((1450, pantalla_alçada-560),llista_objectes_rectangulars),caixa((1600, pantalla_alçada-700), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), caixa((1700, pantalla_alçada-700), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), rectangle_gran_3.copy((1650,pantalla_alçada-730),llista_objectes_rectangulars), quadrat_gran_3.copy((1650, pantalla_alçada-760),llista_objectes_rectangulars),caixa((1800, pantalla_alçada-500), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), caixa((1900, pantalla_alçada-500), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), rectangle_gran_3.copy((1850,pantalla_alçada-530),llista_objectes_rectangulars), quadrat_gran_3.copy((1850, pantalla_alçada-560),llista_objectes_rectangulars),caixa((2000, pantalla_alçada-700), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), caixa((2100, pantalla_alçada-700), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), rectangle_gran_3.copy((2050,pantalla_alçada-730),llista_objectes_rectangulars), quadrat_gran_3.copy((2050, pantalla_alçada-760),llista_objectes_rectangulars),caixa((2200, pantalla_alçada-500), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), caixa((2300, pantalla_alçada-500), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), rectangle_gran_3.copy((2250,pantalla_alçada-530),llista_objectes_rectangulars), quadrat_gran_3.copy((2250, pantalla_alçada-560),llista_objectes_rectangulars),caixa((1500, pantalla_alçada-900), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), caixa((1600, pantalla_alçada-900), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), rectangle_gran_3.copy((1550,pantalla_alçada-930),llista_objectes_rectangulars), quadrat_gran_3.copy((1550, pantalla_alçada-960),llista_objectes_rectangulars), caixa((1700, pantalla_alçada-900), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), caixa((1800, pantalla_alçada-900), 20, 40, False,90,2,llista_objectes_rectangulars,pantalla), rectangle_gran_3.copy((1750,pantalla_alçada-930),llista_objectes_rectangulars), quadrat_gran_3.copy((1750, pantalla_alçada-960),llista_objectes_rectangulars)]
nivell10 = [porc_estandar.copy((1000,pantalla_alçada-40), llista_porcs, llista_objectes_rodons)]
nivell11 = [porc_estandar.copy((1000,pantalla_alçada-40), llista_porcs, llista_objectes_rodons)]
nivell12 = [porc_estandar.copy((1000,pantalla_alçada-40), llista_porcs, llista_objectes_rodons), porc_estandar.copy((600,pantalla_alçada-40), llista_porcs, llista_objectes_rodons)]
nivells_caixes_i_porcs = {1:nivell1, 2:nivell2, 3:nivell3, 4:nivell4, 5:nivell5, 6:nivell6, 7:nivell7, 8:nivell8, 9:nivell9, 10:nivell10, 11:nivell11, 12:nivell12}

#llista_estrelles_nivells
llista_estrelles = [[0,False],[0,True],[0,True],[0,True],[0,True],[0,True],[0,True],[0,True],[0,True],[0,True],[0,True],[0,True]]
total_estrelles = 0
llista_objectes_comprats = [[False,2,skin1],[False,2,skin2],[False,2,skin3],[False,2,skin6],[False,2,skin5],[False,3,skin10],[False,3,skin7],[False,3,skin11],[False,3,skin4],[False,3,skin12],[False,5,skin9],[False,6,skin8]]
estrelles_gastades = 0
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
            if not menú(total_estrelles):
                break
            reinici()
            partida = True
            n = 0
            nombre_porcs = 0
            nombre_porcs_orig = 0
            nombre_ocells = 0
            n2 = 0
        else:
            click = False
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
                if nivell_actual == 5:
                    factor_de_potencia = 0.13
                elif nivell_actual == 7:
                    factor_de_potencia = 0.12
                elif nivell_actual == 8:
                    llista_objectes_pantalla.remove(terra)
                    factor_de_potencia = 0.08
                elif nivell_actual == 9:
                    factor_de_potencia = 0.125
                else:
                    factor_de_potencia = 0.1
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
                        partida = pausa()
                        if partida and sprites == [terra]:
                            n = 0
                            nombre_porcs = 0
                            nombre_porcs_orig = 0
                            nombre_ocells = 0
                            n2 = 0
                    if event.key == pygame.K_SPACE:
                        camara.principi_nivell = False
                        camara.tornar_ocell = True
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
                        ocell_actual.llançament(factor_de_potencia)
                    elif mantenint:
                        mantenint = False
                    elif ocell_anterior.tocat_objecte == False:
                        nombre_ocells = ocell_anterior.habilitat(llista_ocells, llista_objectes_rodons, llista_objectes_pantalla, llista_porcs, llista_objectes_rectangulars, sprites, nombre_ocells)
                    click = True
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
            if n2%velocitat == 0:
                camara.update(llista_objectes_pantalla,ocell_anterior, ocells_nivell, ocell_actual, mantenint_ocell, ocell_anterior, mantenint,posició_mantenint,rectangle_mantenint, llista_ocells_llançats, factor_de_potencia, llista_ocells)
            if nombre_porcs == 0 and n!=0:
                estrelles = nombre_porcs_orig - (len(llista_ocells_llançats)-3)
                estrelles+=2
                if estrelles < 1:
                    estrelles = 1
                elif estrelles >3:
                    estrelles = 3
                llista_estrelles[nivell_actual-1][0] = estrelles
                if nivell_actual != 12:
                    llista_estrelles[nivell_actual][1] = False
                reinici()
                partida = pantalla_final_victoria(estrelles, total_estrelles)
                n = 0
                nombre_porcs_orig = 0
                nombre_ocells = 0
                n2 = 0
                if nivell_actual == 13:
                    partida = False
            elif nombre_ocells == 0 and n!=0:
                reinici()
                n = 0
                nombre_porcs = 0
                nombre_porcs_orig = 0
                n2 = 0
                partida = pantalla_final_derrota(total_estrelles)
            if rectangle_pausa.collidepoint(pygame.mouse.get_pos()):
                rectangle_pausa_3 = rectangle_pausa_2
                pausa_imatge_3 = pausa_imatge_2
                if click:
                    camara.update(llista_objectes_pantalla,ocell_anterior, ocells_nivell, ocell_actual, mantenint_ocell, ocell_anterior, mantenint,posició_mantenint,rectangle_mantenint, llista_ocells_llançats, factor_de_potencia, llista_ocells)
                    pygame.display.flip()
                    partida = pausa()
                    if partida and sprites == [terra]:
                        n = 0
                        nombre_porcs = 0
                        nombre_porcs_orig = 0
                        nombre_ocells = 0
                        n2 = 0
                color2 = taronja
            else:
                pausa_imatge_3 = pausa_imatge
                rectangle_pausa_3 = rectangle_pausa
                color2 =(19,64,132)
            color = (29,86,172)
            rectangle_pausa_4 = pausa_imatge_3.get_rect(center = rectangle_pausa.center)
            pygame.draw.rect(pantalla, color, rectangle_pausa_3)
            pygame.draw.rect(pantalla, color2, rectangle_pausa_3,8)
            pantalla.blit(pausa_imatge_3, rectangle_pausa_4)
         # Recarregar la pantalla
        pygame.display.flip()
    # Sortir del joc
    pygame.quit()

# Córrer el joc
GameLoop()