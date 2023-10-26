import pygame
import math
# Iniciar programa
pygame.init()

#Millora rendiment
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

# Definir els colors bàsics
negre = (0, 0, 0)
blanc = (255, 255, 255)
vermell = (255, 0, 0)
vermell2 = (200, 0, 0)
verd = (0, 255, 0)
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
fons = (80, 80, 255)
gris=(50,50,50)
pedra = (139,140,122)

# Definim la gravetat
gravetat = 0.05

# Preparar la pantalla
info = pygame.display.Info() 
pantalla_amplada,pantalla_alçada = info.current_w,info.current_h
from pygame.locals import *
flags = FULLSCREEN | DOUBLEBUF
pantalla = pygame.display.set_mode((pantalla_amplada, pantalla_alçada), flags, 16)
pygame.display.set_caption("Angry Birds")

# Eines per escriure
font = pygame.font.Font(None, 50)
text = font.render("Hello world!", True, negre)
pantalla.blit(text, (pantalla_amplada // 2 - text.get_width() // 2, pantalla_alçada // 2 - text.get_height() // 2))

# LListes
llista_objectes_rodons = []
llista_objectes_rectangulars = []
llista_objectes_pantalla = []
llista_ocells_llançats = []
sprites = []
llista_ocells = []
llista_porcs = []
#Posició inicial ocells
posició_inicial = [150, pantalla_alçada-150]
nombre_porcs = 0

#Creació funcions basiques
def calcular_angle():
    angle = math.degrees(math.atan2(pygame.mouse.get_pos()[0] - posició_inicial[0], pygame.mouse.get_pos()[1] - posició_inicial[1]))
    return angle

def distancia_ocell_ratoli():
    amplada = math.sqrt(((pygame.mouse.get_pos()[0] - posició_inicial[0]) **2 + (pygame.mouse.get_pos()[1] - posició_inicial[1]) ** 2))
    return amplada
def colisió_cercles(self,x):
    global nombre_porcs
    if self in llista_ocells:    
        self.calcul_posició_primer_xoc()
    if self.c == 0:
        self.c =1
    if x in llista_objectes_rodons:
        if self.velocitat.length()*self.massa/x.massa > 3 and x in llista_porcs and self in llista_ocells:
            x.destrucció()
            self.velocitat *= 0.4
            nombre_porcs -=1
        elif x.velocitat.length()*x.massa/self.massa > 3 and self in llista_porcs and x in llista_ocells:
            self.destrucció()
            x.velocitat *= 0.4 
            nombre_porcs -=1       
        else:
            if x.c == 0:
                x.c = 1    
            if x in llista_ocells:     
                x.calcul_posició_primer_xoc()
            self.angle_rampa = self.calcul_angle_cercle(x.rectangle.center)
            x.angle_rampa = self.angle_rampa + 180
            if x.angle_rampa >= 360:
                x.angle_rampa -= 360
            velocitat_inicial = self.velocitat.copy()
            if self.angle_rampa <= 180:    
                angle_z = 180-self.angle_rampa
            else:
                angle_z = 360-self.angle_rampa + 180
            z = pygame.math.Vector2.from_polar((1, angle_z))
            diferencia_angle_self = math.sqrt((self.velocitat.angle_to((-1,0)) - self.angle_rampa)**2)
            if diferencia_angle_self > 180:
                diferencia_angle_self = 360 - diferencia_angle_self
            diferencia_angle_x = math.sqrt((x.velocitat.angle_to((-1,0)) - x.angle_rampa)**2)
            if diferencia_angle_x > 180:
                diferencia_angle_x = 360 - diferencia_angle_x
            if diferencia_angle_self > 90 and self.velocitat.length() > 0:
                while self.mask.overlap(x.mask,(x.rectangle.x-self.rectangle.x, x.rectangle.y-self.rectangle.y)):
                    self.rectangle.center+=z
            elif diferencia_angle_x > 90 and x.velocitat.length() > 0: 
                if x.angle_rampa <= 180:    
                    angle_zx = 180-x.angle_rampa
                else:
                    angle_zx = 360-x.angle_rampa + 180
                z_x = pygame.math.Vector2.from_polar((1, angle_zx))
                while self.mask.overlap(x.mask,(x.rectangle.x-self.rectangle.x, x.rectangle.y-self.rectangle.y)):
                    x.rectangle.center+=z_x
            else:
                while self.mask.overlap(x.mask,(x.rectangle.x-self.rectangle.x, x.rectangle.y-self.rectangle.y)):
                    self.rectangle.center+=z
            if diferencia_angle_self > 90 and self.velocitat.length() > 0 :    
                nou_angle_velocitat = 180+2*self.velocitat.angle_to((-1,0)) - 2*self.angle_rampa 
                self.velocitat.rotate_ip(nou_angle_velocitat)
                self.velocitat[0] *=0.3 + 0.59*math.sqrt(math.sin(math.radians(x.angle_rampa))**2)
                self.velocitat[1] *=0.3 + 0.59*math.sqrt(math.cos(math.radians(x.angle_rampa))**2)
            elif diferencia_angle_x > 90 and x.velocitat.length() >= 2:
                self.velocitat[0] += x.velocitat[0]*0.4
                self.velocitat[1] += x.velocitat[1]*0.4           
            if diferencia_angle_x > 90 and x.velocitat.length() > 0:
                nou_angle_velocitat_2 = 180 + 2*x.velocitat.angle_to((-1,0)) - 2*x.angle_rampa 
                x.velocitat.rotate_ip(nou_angle_velocitat_2)
                x.velocitat[0] *=0.3 + 0.59*math.sqrt(math.sin(math.radians(x.angle_rampa))**2)
                x.velocitat[1] *=0.3 + 0.59*math.sqrt(math.cos(math.radians(x.angle_rampa))**2)
            elif diferencia_angle_self > 90 and velocitat_inicial.length() >= 2:
                x.velocitat[0] += velocitat_inicial[0]*0.4
                x.velocitat[1] += velocitat_inicial[1]*0.4
    if x in llista_objectes_rectangulars:
        x.colisionats.append(self)
        if self.velocitat.length()*self.massa/x.massa > 4 and x.movible and self in llista_ocells:
            x.destrucció()
            self.velocitat *= 0.4
        elif self in llista_porcs and (self.velocitat.length()>10*self.massa/50 or x.velocitat.length()*x.massa/self.massa>20):
            nombre_porcs-=1
            x.velocitat *=0.4
        else:
            if self.velocitat.length()*self.massa/x.massa > 1.5 and x.movible and self in llista_ocells:
                x.mig_trencat(self.velocitat.length()*self.massa/x.massa)
            if x.caixa == False:
                self.velocitat *= 0.4
            else:    
                if x.angle%90 == 0:
                    xesquina1, xesquina2, xesquina3, xesquina4 = x.rectangle.topleft, x.rectangle.topright, x.rectangle.bottomleft, x.rectangle.bottomright
                else:
                    xesquina1, xesquina2, xesquina3, xesquina4 = pygame.math.Vector2(-0.5*x.amplada,-0.5*x.alçada).rotate(-x.angle) + x.rectangle.center,  pygame.math.Vector2(0.5*x.amplada,-0.5*x.alçada).rotate(-x.angle) + x.rectangle.center, pygame.math.Vector2(-0.5*x.amplada,0.5*x.alçada).rotate(-x.angle) + x.rectangle.center,  pygame.math.Vector2(0.5*x.amplada,0.5*x.alçada).rotate(-x.angle) + x.rectangle.center
                    xesquinas = [xesquina1, xesquina2, xesquina3, xesquina4]
                    xesquina1 = min(xesquinas, key = lambda i: i[1])
                    xesquina2 = max(xesquinas, key = lambda i: i[0])
                    xesquina3 = min(xesquinas, key = lambda i: i[0])
                    xesquina4 = max(xesquinas, key = lambda i: i[1])
                xesquines = [xesquina1, xesquina2, xesquina3, xesquina4]
                n= 0
                for i in xesquines:
                    if self.rectangle.collidepoint(i):
                        i = list(i)
                        i[0] -= self.rectangle.topleft[0]
                        i[1] -= self.rectangle.topleft[1]
                        if self.mask.get_at(i) == 1:
                            n+=1
                            i[0] += self.rectangle.topleft[0]
                            i[1] += self.rectangle.topleft[1]
                            rampa = self
                            if n == 2:
                                xcentre  = (pygame.math.Vector2(i)-posició_xoc)*0.5 + posició_xoc
                                xcentre2 = (xcentre - x.rectangle.center).rotate(180)
                                xcentre = [xcentre[0], xcentre[1], xcentre2[0], xcentre2[1]]
                            posició_xoc = i                      
                if n == 0 or n == 2:
                    mask_xoc = self.mask.overlap_mask(x.mask,(x.rectangle.x- self.rectangle.x, x.rectangle.y- self.rectangle.y))        
                    rectangle_xoc = mask_xoc.get_bounding_rects()
                    posició_xoc = rectangle_xoc[0].center + pygame.math.Vector2(self.rectangle.topleft)
                    rampa = x
                    if n == 2:
                        x.rotar = False
                        x.centre_no_rotar = xcentre 
                if rampa == self:
                    self.angle_rampa = self.calcul_angle_cercle(posició_xoc)
                else:
                    self.angle_rampa = x.calcul_angle_rampa(posició_xoc)
                    if self.angle_rampa == "no":
                        self.angle_rampa = self.calcul_angle_cercle(posició_xoc)
                if self.angle_rampa <= 180:    
                    angle_z = 180-self.angle_rampa
                else:
                    angle_z = 360-self.angle_rampa + 180
                z = pygame.math.Vector2.from_polar((1, angle_z))
                if x.movible == False:
                    while self.mask.overlap(x.mask,(x.rectangle.x-self.rectangle.x, x.rectangle.y-self.rectangle.y)):
                        self.rectangle.center+=z
                    nou_angle_velocitat =180 + 2*self.velocitat.angle_to((-1,0)) - 2*self.angle_rampa
                    self.velocitat.rotate_ip(nou_angle_velocitat)
                    self.velocitat[0] *=0.3 + 0.59*math.sqrt(math.sin(math.radians(self.angle_rampa))**2)
                    self.velocitat[1] *=0.3 + 0.59*math.sqrt(math.cos(math.radians(self.angle_rampa))**2)
                else:
                    if x.z == 0:
                        x.z =1
                        x.velocitat_angle = 0
                    x.angle_rampa = self.angle_rampa + 180
                    if x.angle_rampa >= 360:
                        x.angle_rampa -= 360
                    velocitat_inicial = self.velocitat.copy()
                    diferencia_angle_self = math.sqrt((self.velocitat.angle_to((-1,0)) - self.angle_rampa)**2)
                    if diferencia_angle_self > 180:
                        diferencia_angle_self = 360 - diferencia_angle_self
                    diferencia_angle_x = math.sqrt((x.velocitat.angle_to((-1,0)) - x.angle_rampa)**2)
                    if diferencia_angle_x > 180:
                        diferencia_angle_x = 360 - diferencia_angle_x    
                    antic_centre_x = x.rectangle.center
                    suma_velocitat_per_rotació_x = pygame.math.Vector2(0,0)
                    if diferencia_angle_self > 90 and self.velocitat.length() > 0:
                        suma_velocitat_per_rotació_x = self.velocitat 
                        while self.mask.overlap(x.mask,(x.rectangle.x-self.rectangle.x, x.rectangle.y-self.rectangle.y)):
                            self.rectangle.center+=z
                    elif diferencia_angle_x > 90 and x.velocitat.length() > 0:
                        if x.angle_rampa <= 180:    
                            angle_zx = 180-x.angle_rampa
                        else:
                            angle_zx = 360-x.angle_rampa + 180
                        z_x = pygame.math.Vector2.from_polar((1, angle_zx))
                        while self.mask.overlap(x.mask,(x.rectangle.x-self.rectangle.x, x.rectangle.y-self.rectangle.y)):
                            x.rectangle.center+=z_x
                        if x.rotar == False:
                            x.centre_no_rotar[0] += x.rectangle.center[0] - antic_centre_x[0] 
                            x.centre_no_rotar[1] += x.rectangle.center[1] - antic_centre_x[1]
                            x.centre_no_rotar[2] += x.rectangle.center[0] - antic_centre_x[0]
                            x.centre_no_rotar[3] += x.rectangle.center[1] - antic_centre_x[1]
                    else:
                        while self.mask.overlap(x.mask,(x.rectangle.x-self.rectangle.x, x.rectangle.y-self.rectangle.y)):
                            self.rectangle.center+=z
                    xcentre1 = ((xesquina1[0]-xesquina2[0])/2 + xesquina2[0], (xesquina1[1]-xesquina2[1])/2 + xesquina2[1], pygame.math.Vector2(xesquina1[0]-xesquina2[0],xesquina1[1]-xesquina2[1])*0.5)
                    xcentre2 = ((xesquina1[0]-xesquina3[0])/2 + xesquina3[0], (xesquina1[1]-xesquina3[1])/2 + xesquina3[1], pygame.math.Vector2(xesquina3[0]-xesquina1[0],xesquina3[1]-xesquina1[1])*0.5)
                    xcentre4 = ((xesquina4[0]-xesquina2[0])/2 + xesquina2[0], (xesquina4[1]-xesquina2[1])/2 + xesquina2[1], pygame.math.Vector2(xesquina2[0]-xesquina4[0],xesquina2[1]-xesquina4[1])*0.5)
                    xcentre3 = ((xesquina4[0]-xesquina3[0])/2 + xesquina3[0], (xesquina4[1]-xesquina3[1])/2 + xesquina3[1], pygame.math.Vector2(xesquina4[0]-xesquina3[0],xesquina4[1]-xesquina3[1])*0.5)
                    xcentres = [xcentre1, xcentre2, xcentre3, xcentre4]
                    posició_xoc_x_2 = posició_xoc - pygame.math.Vector2(antic_centre_x)
                    xvector_colisió = pygame.math.Vector2(100000,100000)
                    for i in xcentres:
                        vector = pygame.math.Vector2(posició_xoc[0]-i[0],posició_xoc[1]-i[1])
                        i2_negatiu = i[2].rotate(180)
                        if vector.length() < i[2].length() and vector.length() < xvector_colisió.length():
                            xcolisió_centre = i
                            xvector_colisió = vector
                            if vector.length()<=self.radi:
                                xvector_colisió = pygame.math.Vector2(100000,100000)    
                            xvector_negatiu = i2_negatiu
                        if vector.length() == i[2].length() and x.rotar and vector.length()>self.radi:
                            if abs(i[2].angle_to((-1,0)) - vector.angle_to((-1,0))) <  abs(i2_negatiu.angle_to((-1,0)) - vector.angle_to((-1,0))):
                                x.velocitat_angle += vector.length()*(abs(math.sin(math.radians(i[2].angle_to((-1,0)) - x.velocitat.angle_to((-1,0)))) * x.velocitat.length()) + (suma_velocitat_per_rotació_x.length()*math.sin(math.radians(i[2].angle_to((-1,0)) - suma_velocitat_per_rotació_x.angle_to((-1,0))))*self.massa/x.massa))/(0.5*x.amplada)
                            else:
                                x.velocitat_angle -= vector.length()*(abs(math.sin(math.radians(i[2].angle_to((-1,0)) - x.velocitat.angle_to((-1,0)))) * x.velocitat.length()) + (suma_velocitat_per_rotació_x.length()*math.sin(math.radians(i[2].angle_to((-1,0)) - suma_velocitat_per_rotació_x.angle_to((-1,0))))*self.massa/x.massa))/(0.5*x.amplada)
                    if n == 0 and xvector_colisió != pygame.math.Vector2(100000,100000):
                        if x.rotar:
                            if abs(xcolisió_centre[2].angle_to((-1,0)) - xvector_colisió.angle_to((-1,0))) <  abs(xvector_negatiu.angle_to((-1,0)) - xvector_colisió.angle_to((-1,0))):
                                x.velocitat_angle += xvector_colisió.length()*(abs(math.sin(math.radians(xcolisió_centre[2].angle_to((-1,0)) - x.velocitat.angle_to((-1,0)))) * x.velocitat.length()) + (suma_velocitat_per_rotació_x.length()*math.sin(math.radians(xcolisió_centre[2].angle_to((-1,0)) - suma_velocitat_per_rotació_x.angle_to((-1,0))))*self.massa/x.massa))/(0.5*x.amplada)
                            else:
                                x.velocitat_angle -= xvector_colisió.length()*(abs(math.sin(math.radians(xcolisió_centre[2].angle_to((-1,0)) - x.velocitat.angle_to((-1,0)))) * x.velocitat.length()) + (suma_velocitat_per_rotació_x.length()*math.sin(math.radians(xcolisió_centre[2].angle_to((-1,0)) - suma_velocitat_per_rotació_x.angle_to((-1,0))))*self.massa/x.massa))/(0.5*x.amplada)
                        elif (xcolisió_centre[0] != x.centre_no_rotar[0] or xcolisió_centre[1] != x.centre_no_rotar[1]) and (xcolisió_centre[0] != x.centre_no_rotar[2] or xcolisió_centre[1] != x.centre_no_rotar[3]): 
                            distancia_esquina_xoc = pygame.math.Vector2(0,0)
                            for i in xesquines:
                                i = list(i)
                                distancia_esquina = pygame.math.Vector2(i[0]- xcolisió_centre[0], i[1]- xcolisió_centre[1])
                                if distancia_esquina != xcolisió_centre[2] and distancia_esquina != xvector_negatiu:
                                    distancia = pygame.math.Vector2(posició_xoc[0]-i[0], posició_xoc[1]- i[1])
                                    if distancia_esquina_xoc.length() < distancia.length():
                                        distancia_esquina_xoc = distancia
                                        if math.sqrt((x.centre_no_rotar[0]-i[0])**2 + (x.centre_no_rotar[1]-i[1])**2) < math.sqrt((x.centre_no_rotar[2]-i[0])**2 + (x.centre_no_rotar[3]-i[1])**2):
                                            i = pygame.math.Vector2(i)
                                            x.pivot_pantalla = i + x.rectangle.center - antic_centre_x
                                            x.pivot =((i-antic_centre_x).rotate(x.angle) + antic_centre_x) - pygame.math.Vector2(antic_centre_x[0]-0.5*x.amplada, antic_centre_x[1]-0.5*x.alçada)
                                        else:
                                            x.pivot_pantalla = x.rectangle.center
                                            x.pivot = (0.5*x.amplada, 0.5*x.alçada)
                            if abs(xcolisió_centre[2].angle_to((-1,0)) - xvector_colisió.angle_to((-1,0))) <  abs(xvector_negatiu.angle_to((-1,0)) - xvector_colisió.angle_to((-1,0))):
                                x.velocitat_angle += xvector_colisió.length()*(abs(math.sin(math.radians(xcolisió_centre[2].angle_to((-1,0)) - x.velocitat.angle_to((-1,0)))) * x.velocitat.length()) + (suma_velocitat_per_rotació_x.length()*math.sin(math.radians(xcolisió_centre[2].angle_to((-1,0)) - suma_velocitat_per_rotació_x.angle_to((-1,0))))*self.massa/x.massa))/(0.5*x.amplada)
                            else:
                                x.velocitat_angle -= xvector_colisió.length()*(abs(math.sin(math.radians(xcolisió_centre[2].angle_to((-1,0)) - x.velocitat.angle_to((-1,0)))) * x.velocitat.length()) + (suma_velocitat_per_rotació_x.length()*math.sin(math.radians(xcolisió_centre[2].angle_to((-1,0)) - suma_velocitat_per_rotació_x.angle_to((-1,0))))*self.massa/x.massa))/(0.5*x.amplada)
                    if x.rotar == False or x.velocitat.length()>=3 or x.velocitat_angle>=1:
                        x.pivot_pantalla = x.rectangle.center
                        x.pivot = (0.5*x.amplada, x.alçada*0.5)
                    else: 
                        x.pivot_pantalla = posició_xoc_x_2 + x.rectangle.center
                        x.pivot =(posició_xoc_x_2.rotate(x.angle) + antic_centre_x) - pygame.math.Vector2(antic_centre_x[0]-0.5*x.amplada, antic_centre_x[1]-0.5*x.alçada)  
                    if (x.angle%90 == 0 and posició_xoc[1] >= x.rectangle.bottom) or (n == 0 and xesquina4[1] > posició_xoc[1] and ((xesquina2[1] < posició_xoc[1] and xesquina2[0] > posició_xoc[0] and xesquina4[0] < posició_xoc[0])or(xesquina3[1] < posició_xoc[1] and xesquina3[0] < posició_xoc[0] and xesquina4[0] > posició_xoc[0]))) or posició_xoc == xesquina4 or posició_xoc == xesquina2 or posició_xoc == xesquina3:
                        xmeitat1 = 0
                        xmeitat2 = 0
                        xmeitat3 = 0
                        for i in x.mask.outline():
                            i = list(i)
                            i[0] += x.rectangle.left
                            if i[0] > posició_xoc[0]:
                               xmeitat1+=1
                            elif i[0] < posició_xoc[0]:
                                xmeitat2+=1
                            else:
                                xmeitat3+=1
                        xmeitat1 +=1
                        xmeitat2 -=2
                        xmeitat1_orig = xmeitat1
                        xmeitat1 += (x.velocitat[0]- x.velocitat_angle_ax)*(xmeitat2+xmeitat1) 
                        xmeitat2 -= (x.velocitat[0]- x.velocitat_angle_ax)*(xmeitat1_orig + xmeitat2) 
                        xtotal = xmeitat1 + xmeitat2 + xmeitat3
                        if xmeitat1 > xtotal:
                            xmeitat1 = xtotal
                            xmeitat2 = 0
                            xmeitat3 = 0
                        elif xmeitat2 > xtotal:
                            xmeitat2 = xtotal
                            xmeitat1 = 0
                            xmeitat3 = 0  
                        if x.suma_pes!=[]:      
                            for i in x.suma_pes:
                                for s in i[0]:        
                                    s = list(s)
                                    if s[0] > posició_xoc[0]:
                                        xmeitat1+=1
                                    elif s[0] < posició_xoc[0]:
                                        xmeitat2+=1
                                    else:
                                        xmeitat1 +=1 
                        elif 3+xmeitat1 < xmeitat2:
                            x.rotar = True
                            xmeitat2/= 10
                            xmeitat2 = round(xmeitat2)
                            xmeitat2*=10
                            if n != 0:    
                                if abs(xcentre4[2].length() - 0.5*x.amplada) < abs(xcentre4[2].length() - 0.5*x.alçada):
                                    x.velocitat_angle += abs((x.velocitat[1]) * xmeitat2*0.5)/xtotal
                                else:
                                    x.velocitat_angle += abs((x.velocitat[1]) * xmeitat2*0.5*x.alçada)/(xtotal*x.amplada)
                            else:
                                if abs(xcolisió_centre[2].length() - 0.5*x.amplada) < abs(xcolisió_centre[2].length() - 0.5*x.alçada):
                                    x.velocitat_angle += abs((x.velocitat[1]) * xmeitat2*0.5)/xtotal
                                else:
                                    x.velocitat_angle += abs((x.velocitat[1]) * xmeitat2*0.5*x.alçada)/(xtotal*x.amplada) 
                    velocitat = self.velocitat.copy()
                    if diferencia_angle_self > 90 and self.velocitat.length() > 0 :    
                        nou_angle_velocitat = 180+2*self.velocitat.angle_to((-1,0)) - 2*self.angle_rampa 
                        self.velocitat.rotate_ip(nou_angle_velocitat)
                        self.velocitat[0] *=0.3 + 0.59*math.sqrt(math.sin(math.radians(x.angle_rampa))**2)
                        self.velocitat[1] *=0.3 + 0.59*math.sqrt(math.cos(math.radians(x.angle_rampa))**2)
                    if diferencia_angle_self < 100 and diferencia_angle_x >= 90 and x.velocitat.length() >= 2:
                        self.velocitat[0] += x.velocitat[0]*0.4 *x.massa/self.massa
                        self.velocitat[1] += x.velocitat[1]*0.4 *x.massa/self.massa
                    velocitat2 = x.velocitat.copy()           
                    if diferencia_angle_x > 90 and x.velocitat.length() > 0:
                        nou_angle_velocitat_2 = 180 + 2*x.velocitat.angle_to((-1,0)) - 2*x.angle_rampa 
                        velocitat2.rotate_ip(nou_angle_velocitat_2)
                        velocitat2[0] *=0.3 + 0.59*abs(math.sin(math.radians(x.angle_rampa)))
                        velocitat2[1] *=0.3 + 0.59*abs(math.cos(math.radians(x.angle_rampa)))
                        x.conjut_de_velocitats_1.append(velocitat2)
                    if diferencia_angle_x < 100 and diferencia_angle_self >= 90 and velocitat.length() >= 2 :
                        velocitat2*=0
                        velocitat2[0] += velocitat[0]*0.4*self.massa/x.massa
                        velocitat2[1] += velocitat[1]*0.4*self.massa/x.massa
                        x.conjut_de_velocitats_2.append(velocitat2) 
                    if x.rotar:
                        x.pivot = (round(x.pivot[0]), round(x.pivot[1]))
                        x.pivot_pantalla = (round(x.pivot_pantalla[0]), round(x.pivot_pantalla[1]))
# Creació ocells
class ocells():
    def __init__(self, radi, color):
        global gravetat
        self.animació = False
        self.radi = radi
        self.velocitat = pygame.math.Vector2(0,0)
        self.angle = 0
        self.angle_rampa = 0
        self.aire = False
        self.color = color
        self.zona = False
        self.llançat = False
        global llista_objectes_pantalla
        self.cooldown = 0
        self.posició_primer_xoc = [0,0]
        self.tocat_objecte = False
        self.linea_direció = False
        self.linea_direció_radi = 0
        self.linea_direció_velocitat = [0,0]
        self.linea_direció_tocat_objecte = False
        self.linea_direció_moviment = 0
        self.estela_velocitat = [0,0]
        llista_ocells.append(self) 
        self.colisionat = False
        self.superficie_ocell = pygame.Surface((2*self.radi, 2*self.radi), pygame.SRCALPHA)
        self.rectangle = self.superficie_ocell.get_rect()
        self.rectangle.center = (posició_inicial[0], posició_inicial[1])
        pygame.draw.circle(self.superficie_ocell, self.color, (self.radi, self.radi), self.radi)
        self.mask = pygame.mask.from_surface(self.superficie_ocell)
        self.c = 0
        self.posició_real = posició_inicial
        self.massa = self.radi**2 *3.14
        self.activat = False
        self.n = 0
        self.llista_estela = []
        self.llista_copia = []
    
    def calcul_posició_primer_xoc (self):
        if self.tocat_objecte == False:
            self.tocat_objecte = True
            for i in self.llista_copia:
                i.llista_estela.extend(self.llista_estela)
            self.llista_copia.clear()
    def calcul_angle_cercle(self, pos):
        vector_angle = pygame.math.Vector2(pos[0]-self.rectangle.center[0], pos[1]-self.rectangle.center[1])
        s = vector_angle.angle_to((-1,0)) + 180
        if s >= 360:
            s -=360
        return s
    
    def colisió(self,x):
        colisió_cercles(self,x)
    
    def calcul_linea_direció(self):
        self.linea_direció_radi = 5
        self.linea_direció_posició = [posició_inicial[0], posició_inicial[1]]
        self.potencia = distancia_ocell_ratoli() - self.radi
        self.angle = math.radians(calcular_angle())
        if self.potencia >= 100:
            self.potencia = 100
        if self.potencia <= 0 or self.angle > -0.1 or self.angle < -3:
            self.potencia = 0
        if self.potencia !=0:
            self.linea_direció_velocitat[0] = -math.sin(self.angle) * self.potencia * 0.1
            self.linea_direció_velocitat[1] = -math.cos(self.angle) * self.potencia * 0.1
            self.linea_direció_velocitat[1]  += gravetat * 0.2 *(self.linea_direció_moviment%30)
            self.linea_direció_posició[0] += self.linea_direció_velocitat[0] * 0.2 *(self.linea_direció_moviment%30)
            self.linea_direció_posició[1] += self.linea_direció_velocitat[1] * 0.2 *(self.linea_direció_moviment%30)
            pygame.draw.circle(pantalla, blanc, self.linea_direció_posició, self.linea_direció_radi)    
            while self.linea_direció_radi >1:   
                self.linea_direció_radi -= 0.30
                self.linea_direció_velocitat[1]  += gravetat * 6
                self.linea_direció_posició[0] += self.linea_direció_velocitat[0] * 6
                self.linea_direció_posició[1] += self.linea_direció_velocitat[1] * 6
                for i in llista_objectes_pantalla:
                    if i.rectangle.collidepoint(self.linea_direció_posició):
                        break 
                pygame.draw.circle(pantalla, blanc, self.linea_direció_posició, self.linea_direció_radi)
            self.linea_direció_moviment +=0.5
    
    def estela(self): 
        for i in self.llista_estela:
            pygame.draw.circle(pantalla, blanc, i[0] ,i[1])
    
    def update(self):
        if self.linea_direció:
            self.calcul_linea_direció()    
        if self.llançat and self.tocat_objecte == False:
            self.n+=1
            if self.n%5 == 0:
                self.llista_estela.append((self.rectangle.center,2))
            self.estela()
        if self.aire:  
            self.posició_real += self.velocitat
            self.posició_real[1] += 0.5*gravetat
            self.velocitat[1] += gravetat 
            if abs(self.velocitat[1]) < gravetat:
                self.velocitat[1] = 0
            if abs(self.velocitat[0]) < gravetat:
                self.velocitat[0] = 0
        if self.llançat:
            if self.velocitat.length()<gravetat*2:    
                self.cooldown += 1
        else:
            self.cooldown = 0
        if self.cooldown >= 100:     
            llista_objectes_pantalla.remove(self)
        self.colisionat = False
        if self.llançat:    
            self.rectangle.center = self.posició_real
            if self.rectangle.center[0]>pantalla_amplada or self.rectangle.center[0]<0 or self.rectangle.center[1]>pantalla_alçada:
                self.calcul_posició_primer_xoc()
                if self.rectangle.center[0]>pantalla_amplada+100 or self.rectangle.center[0]<-100 or self.rectangle.center[1]>pantalla_alçada+100:     
                    llista_objectes_pantalla.remove(self)
        if self.animació:
            if self.n%5 == 0:    
                n=pygame.math.Vector2(5,5)
                for i in self.objecte_animació:
                    i[0] -= 2
                    i[1] +=n
                    n.rotate_ip(90)
                if self.objecte_animació[0][0] <=1:
                    self.animació =False
            self.n+=1

    def dibuixar(self):
        if self.c == 1:
            self.posició_real = self.rectangle.center
            self.c = 0
        pantalla.blit(self.superficie_ocell, self.rectangle)
        if self.animació:
            for i in self.objecte_animació:
                pygame.draw.circle(pantalla,self.color_animació,i[1],i[0])

    def llançament(self):
        self.rectangle.center = posició_inicial
        self.potencia = distancia_ocell_ratoli() - self.radi
        self.angle = math.radians(calcular_angle())
        if self.potencia >= 100:
            self.potencia = 100
        if self.potencia <= 0 or self.angle > -0.1 or self.angle < -3:
            self.potencia = 0
        if self.potencia != 0:
            self.velocitat[0] = -math.sin(self.angle) * self.potencia * 0.1
            self.velocitat[1] = -math.cos(self.angle) * self.potencia * 0.1
            self.llançat = True
            self.aire = True
            self.velocitat_sortida = self.velocitat.copy()
    
    def zona_llançament(self):
        self.zona = self.rectangle.collidepoint(pygame.mouse.get_pos())
        return self.zona
    def habilitat(self):
        if self.activat == False and self.color != vermell:
            self.llista_estela.append((self.rectangle.center, 10))
            self.n = 0    
            if self.color == groc:
                self.activar_animació(blanc,1) 
                self.velocitat[0] *= 2.5
            elif self.color == cian:
                self.activar_animació(blanc,1) 
                self.copia1 = self.copy()
                self.copia2 = self.copy() 
                self.copia1.llançat = True
                self.copia2.llançat = True
                self.copia1.aire = True
                self.copia2.aire = True
                self.copia1.tocat_objecte = False
                self.copia2.tocat_objecte = False
                self.copia1.posició_real = self.rectangle.center+pygame.math.Vector2(25,10)
                self.copia2.posició_real = self.rectangle.center+pygame.math.Vector2(25,-10)
                llista_objectes_pantalla.append(self.copia1) 
                llista_objectes_pantalla.append(self.copia2)
                sprites.append(self.copia1)
                sprites.append(self.copia2)
                self.copia1.velocitat = self.velocitat.rotate(20)
                self.copia2.velocitat = self.velocitat.rotate(-20)
                self.copia1.rectangle = self.rectangle.copy()
                self.copia2.rectangle = self.rectangle.copy()
                while self.rectangle.colliderect(self.copia1.rectangle):
                    self.copia1.posició_real += self.copia1.velocitat
                    self.copia1.rectangle.center = self.copia1.posició_real
                while self.rectangle.colliderect(self.copia2.rectangle):
                    self.copia2.posició_real += self.copia2.velocitat
                    self.copia2.rectangle.center = self.copia2.posició_real
                self.copia1.posició_real = self.copia1.rectangle.center
                self.copia2.posició_real = self.copia2.rectangle.center
                self.copia1.llista_copia.append(self)
                self.copia2.llista_copia.append(self)
            else:
                if self.color == negre:    
                    self.activar_animació(taronja2,1.5)
                else:
                    self.activar_animació(negre,1.5)
                for i in llista_objectes_pantalla:
                    if i != self:
                        if i in llista_porcs:    
                            if i.porc:    
                                distancia_explosió = pygame.math.Vector2(self.rectangle.center) - i.rectangle.center
                                potencia = 200 - distancia_explosió.length() + self.radi
                                if potencia >0:
                                    angle = self.calcul_angle_cercle(i.rectangle.center) +180
                                    if angle <= 180:    
                                        angle = 180- angle
                                    else:
                                        angle = 360-angle + 180
                                    if self.color == blanc:
                                        angle +=180
                                        potencia *=2
                                    else:
                                        potencia +=50
                                        if potencia > 200:
                                            potencia = 200
                                    i.velocitat += pygame.math.Vector2.from_polar((potencia*50/i.massa, angle))
                        elif i in llista_ocells:    
                            if i.llançat:    
                                distancia_explosió = pygame.math.Vector2(self.rectangle.center) - i.rectangle.center
                                potencia = 200 - distancia_explosió.length() + self.radi
                                if potencia >0:
                                    angle = self.calcul_angle_cercle(i.rectangle.center)
                                    if angle <= 180:    
                                        angle = 180- angle
                                    else:
                                        angle = 360-angle +180
                                    if self.color == blanc:
                                        angle +=180
                                        potencia *=2
                                    else:
                                        potencia +=50
                                        if potencia > 200:
                                            potencia = 200
                                    i.velocitat += pygame.math.Vector2.from_polar((potencia*50/i.massa, angle))
                        if i in llista_objectes_rectangulars:    
                            if i.caixa and i.movible:    
                                distancia_explosió = pygame.math.Vector2(self.rectangle.center) - i.rectangle.center
                                potencia = 200 - distancia_explosió.length() + self.radi
                                if potencia >0:
                                    angle = self.calcul_angle_cercle(i.rectangle.center) + 180
                                    if angle <= 180:    
                                        angle = 180- angle
                                    else:
                                        angle = 360-angle + 180
                                    if self.color == blanc:
                                        angle +=180
                                        potencia *=2
                                    else:
                                        potencia +=50
                                        if potencia > 200:
                                            potencia = 200
                                    i.velocitat += pygame.math.Vector2.from_polar((potencia*50/i.massa, angle))
            self.activat = True
    def copy(self):
        x = ocells(self.radi, self.color)
        return x
    def reinici(self):
        self.activat = False
        self.aire = False
        self.velocitat *= 0
        self.llançat = False
        self.llista_estela.clear()
        self.n = 0
        self.rectangle.center = [posició_inicial[0], posició_inicial[1]]
        self.posició_real = [posició_inicial[0], posició_inicial[1]]
        self.zona = False
        self.cooldown = 0
        self.tocat_objecte = False
        self.linea_direció = False
        self.posició_primer_xoc = [0,0] 
        self.animació = False
        self.llista_copia.clear()
    
    def activar_animació(self, color,radi2):
        radi = self.radi /radi2
        self.color_animació = color
        self.animació=True
        self.objecte_animació = [[radi,self.rectangle.center],[radi,self.rectangle.center],[radi,self.rectangle.center],[radi,self.rectangle.center]]

# Ocells creats 
vermellet = ocells(18, vermell)
bombardero = ocells(22, negre)
estrella = ocells(22, blanc)
pequeñin = ocells(13, cian)
racista = ocells(18, groc)
no_ocell = ocells(0, fons)
llista_ocells_llançats = [no_ocell]
llista_objectes_rodons.extend(llista_ocells)

#Creació ordre d'ocells
def següent_ocell(ocell1, ocell2, ocell3, ocell4, ocell5, ocell6):
    ordre_ocells = [ocell1, ocell2, ocell3, ocell4, ocell5, ocell6]
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
                    if n==6:
                        x = llista_ocells_llançats.index(no_ocell)  
    return x

# Creació linea ocells
def linea_ocells(ocell1, ocell2, ocell3, ocell4, ocell5, ocell6):
    ordre_ocells = [ocell1, ocell2, ocell3, ocell4, ocell5, ocell6]
    n = 0
    for i in ordre_ocells:
        if i not in llista_ocells_llançats:    
            pygame.draw.circle(pantalla, i.color, (180 - n*50, pantalla_alçada - i.radi), i.radi)
            n+=1
#Tirachines
rectangle_base = pygame.Rect(posició_inicial[0]-10, posició_inicial[1]+55, 20, pantalla_alçada-posició_inicial[1])
punt_t1 = (posició_inicial[0], posició_inicial[1]+55)
punt_t2 = (posició_inicial[0]+50,posició_inicial[1]-50)
punt_t3 = (posició_inicial[0]-60,posició_inicial[1]-50)
punt_t4 = (posició_inicial[0]+50,posició_inicial[1]-45)
punt_t5 = (posició_inicial[0]-60,posició_inicial[1]-45)
# Creació linea que indica direcció ocell
def linea(ocell, x):
    pygame.draw.rect(pantalla, marró, rectangle_base)
    pygame.draw.line(pantalla, marró2, punt_t1, punt_t3, width = 18)
    if x == True:
        pos = pygame.mouse.get_pos()
        angle = math.atan2(pos[0]-posició_inicial[0], pos[1]-posició_inicial[1])
        if distancia_ocell_ratoli() < (100+ocell.radi):
            if angle > -0.1 or angle < -3:
                color = vermell
            else:
                color = blau
            pos = list(pos)
            rectangle = pygame.Rect(pos[0]-ocell.radi, pos[1]-ocell.radi, 2*ocell.radi, 2*ocell.radi)
            if rectangle_base.colliderect(rectangle):
                pos[1] = punt_t1[1]-ocell.radi
            pygame.draw.line(pantalla, (160,160,160), punt_t5, pos, width = 8)
            pygame.draw.line(pantalla, (160,160,160), punt_t4, pos, width = 8)
            ocell.rectangle.center = pos
            pygame.draw.line(pantalla, marró, punt_t1, punt_t2, width = 20)
        else:
            if angle > -0.1 or angle < -3:
                color = vermell
            else:
                color = verd
            distancia = distancia_ocell_ratoli() - 100 - ocell.radi
            pos = [pygame.mouse.get_pos()[0]-math.sin(angle)*distancia, pygame.mouse.get_pos()[1]-math.cos(angle)*distancia]
            rectangle = pygame.Rect(pos[0]-ocell.radi, pos[1]-ocell.radi, 2*ocell.radi, 2*ocell.radi)
            if rectangle_base.colliderect(rectangle):
                pos[1] = punt_t1[1]-ocell.radi
            pygame.draw.line(pantalla, (160,160,160),punt_t5, pos, width = 8)
            pygame.draw.line(pantalla, (160,160,160),punt_t4, pos, width = 8)
            pygame.draw.line(pantalla, marró, punt_t1, punt_t2, width = 20)
            ocell.rectangle.center = pos

    else:
        pygame.draw.line(pantalla, (160,160,160),punt_t5, posició_inicial, width = 8)
        pygame.draw.line(pantalla, (160,160,160),punt_t4, posició_inicial, width = 8)
# Creació porcs
class porc():
    def __init__(self, radi, posició,):    
        global gravetat
        self.radi = radi
        self.velocitat = pygame.math.Vector2(0,0)
        self.angle_rampa = 0
        global llista_objectes_pantalla
        llista_porcs.append(self) 
        llista_objectes_rodons.append(self)
        self.colisionat = False
        self.superficie_porc = pygame.Surface((2*self.radi, 2*self.radi), pygame.SRCALPHA)
        self.rectangle = self.superficie_porc.get_rect()
        self.rectangle.center = posició
        pygame.draw.circle(self.superficie_porc, verd, (self.radi, self.radi), self.radi)
        self.mask = pygame.mask.from_surface(self.superficie_porc)
        self.c = 0
        self.posició_real = posició
        self.massa = self.radi**2 *3.14
        self.posició_inicial = posició
        self.rectangle.center = posició
        self.porc = True
        self.n = 0
    
    def update(self):
        if self.porc:    
            self.colisionat = False
            self.posició_real += self.velocitat
            self.posició_real[1] += 0.5*gravetat
            self.velocitat[1] += gravetat 
            if abs(self.velocitat[1]) < gravetat:
                self.velocitat[1] = 0
            if abs(self.velocitat[0]) < gravetat:
                self.velocitat[0] = 0
            self.rectangle.center = self.posició_real
            if self.rectangle.center[0]>pantalla_amplada+ self.radi or self.rectangle.center[0]<-self.radi or self.rectangle.center[1]>pantalla_alçada+self.radi:
                global nombre_porcs
                llista_objectes_pantalla.remove(self)
                nombre_porcs-=1
        else:
            if self.n%5 == 0:    
                n=pygame.math.Vector2(5,5)
                for i in self.animació:
                    i[0] -= 1
                    i[1] +=n
                    n.rotate_ip(90)
                if self.animació[0][0] <=1:
                    llista_objectes_pantalla.remove(self)
            self.n+=1
    def dibuixar(self):
        if self.porc:    
            if self.c == 1:
                self.posició_real = self.rectangle.center
                self.c = 0
            pantalla.blit(self.superficie_porc, self.rectangle)
        else:    
            for i in self.animació:
                pygame.draw.circle(pantalla,verd,i[1],i[0])
    def reinici(self):
        self.velocitat *= 0
        self.rectangle.center = self.posició_inicial
        self.posició_real = self.posició_inicial
        self.porc = True
        self.n = 0

    def colisió(self,x):
        colisió_cercles(self,x)

    def calcul_angle_cercle(self, pos):
        vector_angle = pygame.math.Vector2(pos[0]-self.rectangle.center[0], pos[1]-self.rectangle.center[1])
        s = vector_angle.angle_to((-1,0)) + 180
        if s >= 360:
            s -=360
        return s


    def destrucció(self):
        self.velocitat *= 0
        self.angle_rampa = 90
        radi = self.radi/2
        self.porc  = False
        self.animació = [[radi,self.rectangle.center],[radi,self.rectangle.center],[radi,self.rectangle.center],[radi,self.rectangle.center]]
    def copy(self, posició):
        x = porc(self.radi, posició)
        return x
porc_estandar = porc(20, (pantalla_amplada - 180, pantalla_alçada - 160))
#Caixes 
class caixa():
    def __init__(self, posició, alçada, amplada, movible, angle, tipo):
        self.alçada = alçada
        self.amplada = amplada
        self.massa = self.alçada*self.amplada*(tipo/2)
        self.posició_inicial = posició
        self.velocitat = pygame.math.Vector2(0,0)
        self.movible = movible
        llista_objectes_rectangulars.append(self)
        self.superficie_rectangle = pygame.Surface((self.amplada, self.alçada))
        self.rectangle = self.superficie_rectangle.get_rect()
        self.rectangle.center = posició
        self.superficie_rectangle.set_colorkey(fons)
        self.angle = angle
        self.angle_inicial = angle
        self.superficie_rectangle.fill(marró)
        if tipo == 1:
            self.color_borde = blau_fosc
            self.color = cian
        elif tipo == 2:
            self.color_borde = marró_fosc  
            self.color = marró
        elif tipo == 3:
            self.color_borde = gris 
            self.color   = pedra
        self.tipo = tipo 
        self.superficie_rectangle.fill(self.color)
        if self.amplada < self.alçada:    
            pygame.draw.rect(self.superficie_rectangle, self.color_borde , ((0,0), (self.amplada, self.alçada)), 10 - (100//self.amplada))
        else:
            pygame.draw.rect(self.superficie_rectangle, self.color_borde , ((0,0), (self.amplada, self.alçada)), 10 - (100//self.alçada))
        self.colisionat = False
        self.rectangle_nou = pygame.transform.rotate(self.superficie_rectangle, self.angle)
        self.rectangle = self.rectangle_nou.get_rect()
        self.rectangle.center = posició
        self.posició_real = posició
        self.mask = pygame.mask.from_surface(self.rectangle_nou)
        self.velocitat_angle = 0
        self.conjut_de_velocitats_1 = []
        self.conjut_de_velocitats_2 = []
        self.vector_centre1 = pygame.math.Vector2(-0.25*amplada, 0)
        self.vector_centre2 = pygame.math.Vector2(0.25*amplada, 0)
        self.colisionats = []
        self.rotar = True
        self.n = 0
        self.suma_pes = []
        self.rotacions = []
        self.caixa = True
        self.vida = 4 
    
    def update(self):
        if self.movible == True and self.caixa:
            if self.rotar == False:
                if self.n == 0:
                    self.posició_no_rotació = pygame.math.Vector2(self.rectangle.center)
                    self.n +=1
                    self.angle_no_rotar = pygame.math.Vector2(self.centre_no_rotar[0]-self.centre_no_rotar[2], self.centre_no_rotar[1]- self.centre_no_rotar[3]).angle_to((-1,0))
                    self.angle_no_rotar +=90
                    if self.angle_no_rotar >=360:
                        self.angle_no_rotar -=360
                    if self.angle_no_rotar >=180:
                        self.angle_no_rotar -=180
                    self.centre_no_rotar_orig = [self.centre_no_rotar[0], self.centre_no_rotar[1],self.centre_no_rotar[2],self.centre_no_rotar[3]]
            if self.angle >= 360:
                self.angle -= 360
            if self.angle < 0:
                self.angle += 360
            self.posició_real += self.velocitat
            self.posició_real[1] += 0.5*gravetat
            self.velocitat[1] += gravetat
            if abs(self.velocitat[1]) < gravetat:
                self.velocitat[1] = 0
            if abs(self.velocitat[0]) < gravetat:
                self.velocitat[0] = 0
            self.angle += self.velocitat_angle
            self.rectangle.center = self.posició_real
            if self.rotar == False:
                if abs(self.posició_no_rotació[1] - self.rectangle.center[1]) > 1 or abs(self.posició_no_rotació[0] - self.rectangle.center[0]) > 1:
                    self.centre_no_rotar[0] = self.rectangle.center[0] - self.posició_no_rotació[0] + self.centre_no_rotar_orig[0]
                    self.centre_no_rotar[2] = self.rectangle.center[0] - self.posició_no_rotació[0] + self.centre_no_rotar_orig[2]
                    self.centre_no_rotar[1] = self.rectangle.center[1] - self.posició_no_rotació[1] + self.centre_no_rotar_orig[1]
                    self.centre_no_rotar[3] = self.rectangle.center[1] - self.posició_no_rotació[1] + self.centre_no_rotar_orig[3]
                    angle =(self.posició_no_rotació-self.rectangle.center).angle_to((-1,0)) 
                    if angle >=180:
                        angle -=180
                    if abs(angle - self.angle_no_rotar) > 5:
                        self.rotar = True
                        self.n = 0
            if self.velocitat_angle != 0: 
                self.pivot_pantalla += self.velocitat
                self.rectangle_2 = self.superficie_rectangle.get_rect(topleft = (self.pivot_pantalla[0]- self.pivot[0], self.pivot_pantalla[1]- self.pivot[1]))
                offset = pygame.math.Vector2(self.pivot_pantalla) - self.rectangle_2.center
                offset_rotado = offset.rotate(-self.angle)
                imagen_centro = (self.pivot_pantalla[0]- offset_rotado.x, self.pivot_pantalla[1]- offset_rotado.y)
                self.rectangle_nou = pygame.transform.rotate(self.superficie_rectangle, self.angle)
                self.rectangle = self.rectangle_nou.get_rect(center = imagen_centro)
                pivote_real = (pygame.math.Vector2(self.pivot)-(0.5*self.amplada, 0.5*self.alçada)).rotate(-self.angle) + self.rectangle.center
                error = self.pivot_pantalla - pivote_real
                self.rectangle.center += error
                self.mask = pygame.mask.from_surface(self.rectangle_nou)
            if self.rotacions != []:
                if abs(self.rotacions[0][1] - round(self.rectangle.bottom)) >=2:
                    self.rotacions.clear()
            self.velocitat_angle_ax = self.velocitat_angle  
        self.colisionat = False
        self.z = 0
        if self.caixa == False:
            n=pygame.math.Vector2(1,1)
            for i in self.animació:
                i[0] -= 0.5
                i[1] +=n
                n.rotate_ip(90)
            if self.animació[0][0] <=1:
                llista_objectes_pantalla.remove(self)
    def dibuixar(self):
        if self.caixa:    
            if self.colisionats != [] and self.movible:
                self.posició_real = self.rectangle.center
                if self.conjut_de_velocitats_1 != []:
                    self.velocitat*=0    
                    for i in self.conjut_de_velocitats_1:
                        self.velocitat += i
                    self.velocitat /= len(self.conjut_de_velocitats_1)
                for i in self.conjut_de_velocitats_2:
                    self.velocitat += i
                self.conjut_de_velocitats_1.clear()
                self.conjut_de_velocitats_2.clear()
                if self.rotacions != []:
                    if min(self.rotacions, key = lambda i: i[0])[0] * max(self.rotacions, key = lambda i: i[0])[0] >0:
                        self.velocitat_angle += max(self.rotacions, key = lambda i: i[1])[0]
                        self.rotacions = [max(self.rotacions, key = lambda i: i[1])]
                    else:
                        self.angle=round(self.angle)
                        self.rotacions.clear()
                self.rectangle_2 = self.superficie_rectangle.get_rect(topleft = (self.pivot_pantalla[0]- self.pivot[0], self.pivot_pantalla[1]- self.pivot[1]))
                offset = pygame.math.Vector2(self.pivot_pantalla) - self.rectangle_2.center
                offset_rotado = offset.rotate(-self.angle)
                imagen_centro = (self.pivot_pantalla[0]- offset_rotado.x, self.pivot_pantalla[1]- offset_rotado.y)
                self.rectangle_nou = pygame.transform.rotate(self.superficie_rectangle, self.angle)
                self.rectangle = self.rectangle_nou.get_rect(center = imagen_centro)
                pivote_real = (pygame.math.Vector2(self.pivot)-(0.5*self.amplada, 0.5*self.alçada)).rotate(-self.angle) + self.rectangle.center
                error = self.pivot_pantalla - pivote_real
                self.rectangle.center += error
                self.mask = pygame.mask.from_surface(self.rectangle_nou)
                self.colisionats.clear()
            pantalla.blit(self.rectangle_nou, self.rectangle)
        else:
            for i in self.animació:
                pygame.draw.circle(pantalla,blanc,i[1],i[0])
    def calcul_angle_rampa(self, pos):
        if self.amplada < self.alçada*2:    
            vector_angle = pygame.math.Vector2(pos[0]-self.rectangle.center[0], pos[1]-self.rectangle.center[1])
            s = vector_angle.angle_to((-1,0))
            if s >= 180:
                s = s-180
            else:
                s = s + 180 
            y = self.angle-s
            if abs(y) < (math.degrees(math.atan2(self.alçada, self.amplada))) or abs(y) > (360-(math.degrees(math.atan2(self.alçada, self.amplada))) +self.angle):
                z = self.angle
            elif (y > -(math.degrees(math.atan2(self.alçada, self.amplada) + 2*math.atan2(self.amplada, self.alçada))) and y < 0) or (y-360)> -(math.degrees(math.atan2(self.alçada, self.amplada) + 2*math.atan2(self.amplada, self.alçada))):
                z = self.angle + 90
            elif (y < (math.degrees(math.atan2(self.alçada, self.amplada) + 2*math.atan2(self.amplada, self.alçada))) and y > 0) or (y+360)< (math.degrees(math.atan2(self.alçada, self.amplada) + 2*math.atan2(self.amplada, self.alçada))):
                z = self.angle + 270
            elif abs(y) > (math.degrees(math.atan2(self.alçada, self.amplada) + 2*math.atan2(self.amplada, self.alçada))):
                z = self.angle +180
            else:
                return("no")
        else:
            pos_centre1 = self.vector_centre1.rotate(-self.angle)+ self.rectangle.center
            pos_centre2 = self.vector_centre2.rotate(-self.angle)+ self.rectangle.center
            vector_angle1 = pygame.math.Vector2(pos[0]-pos_centre1[0], pos[1]-pos_centre1[1])
            vector_angle2 = pygame.math.Vector2(pos[0]-pos_centre2[0], pos[1]-pos_centre2[1])
            s1 = vector_angle1.angle_to((-1,0))
            s2 = vector_angle2.angle_to((-1,0))
            y1 = self.angle-s1
            angle2 = self.angle + 180
            if angle2>= 360:
                angle2-=360
            y2 = angle2-s2
            z11 = math.degrees(math.atan2(self.alçada, 0.5*self.amplada))
            z22 = 90 - z11
            if math.sqrt((y2)**2) < (z11) or math.sqrt((y2)**2) > (360-(z11)):
                 z = self.angle
            elif math.sqrt((y1)**2) < (z11) or math.sqrt((y1)**2) > (360-(z11)):
                 z = self.angle + 180
            elif (y1 < 180 and y1 > 0) or (y1 < -180 and y1 < 0):
                z = self.angle + 90
            elif (y1 > 180 and y1 > 0) or (y1 > -180 and y1 < 0):
                z = self.angle + 270
            else:
                return("no")
        if z >= 360:
            z -= 360
        if z >= 180:
            z = z-180
        else:
            z = z + 180  
        return z
    
    def colisió(self, x):
        self.colisionats.append(x)
        x.colisionats.append(self)
        xesquines_xoc = []
        esquines_xoc = []
        rotar = True
        if self.angle%90 == 0:
            esquina1, esquina2, esquina3, esquina4 = self.rectangle.topleft, self.rectangle.topright, self.rectangle.bottomleft, self.rectangle.bottomright
        else:
            esquina1, esquina2, esquina3, esquina4 = pygame.math.Vector2(-0.5*self.amplada,-0.5*self.alçada).rotate(-self.angle) + self.rectangle.center,  pygame.math.Vector2(0.5*self.amplada,-0.5*self.alçada).rotate(-self.angle) + self.rectangle.center, pygame.math.Vector2(-0.5*self.amplada,0.5*self.alçada).rotate(-self.angle) + self.rectangle.center,  pygame.math.Vector2(0.5*self.amplada,0.5*self.alçada).rotate(-self.angle) + self.rectangle.center
            esquinas = [esquina1, esquina2, esquina3, esquina4]
            esquina1 = min(esquinas, key = lambda i: i[1])
            esquina2 = max(esquinas, key = lambda i: i[0])
            esquina3 = min(esquinas, key = lambda i: i[0])
            esquina4 = max(esquinas, key = lambda i: i[1])
        esquines = [pygame.math.Vector2(esquina1), pygame.math.Vector2(esquina2), pygame.math.Vector2(esquina3), pygame.math.Vector2(esquina4)]
        if x.angle%90 == 0:
            xesquina1, xesquina2, xesquina3, xesquina4 = x.rectangle.topleft, x.rectangle.topright, x.rectangle.bottomleft, x.rectangle.bottomright
        else:
            xesquina1, xesquina2, xesquina3, xesquina4 = pygame.math.Vector2(-0.5*x.amplada,-0.5*x.alçada).rotate(-x.angle) + x.rectangle.center,  pygame.math.Vector2(0.5*x.amplada,-0.5*x.alçada).rotate(-x.angle) + x.rectangle.center, pygame.math.Vector2(-0.5*x.amplada,0.5*x.alçada).rotate(-x.angle) + x.rectangle.center,  pygame.math.Vector2(0.5*x.amplada,0.5*x.alçada).rotate(-x.angle) + x.rectangle.center
            xesquinas = [xesquina1, xesquina2, xesquina3, xesquina4]
            xesquina1 = min(xesquinas, key = lambda i: i[1])
            xesquina2 = max(xesquinas, key = lambda i: i[0])
            xesquina3 = min(xesquinas, key = lambda i: i[0])
            xesquina4 = max(xesquinas, key = lambda i: i[1])
        xesquines = [pygame.math.Vector2(xesquina1), pygame.math.Vector2(xesquina2), pygame.math.Vector2(xesquina3), pygame.math.Vector2(xesquina4)]
        n= 0
        ns = 0
        for i in esquines:
            if x.rectangle.collidepoint(i) or ((i[0] >= x.rectangle.left and i[0] <= x.rectangle.right) and i[1] == x.rectangle.bottom) or ((i[1] >= x.rectangle.top and i[1] <= x.rectangle.bottom) and i[0] == x.rectangle.right):
                suma_1 = False
                suma_2 = False
                i = list(i)
                i[0] -= x.rectangle.topleft[0]
                i[1] -= x.rectangle.topleft[1]
                if i[0] == x.rectangle.width:
                    i[0] -= 1
                    suma_1 = True
                if i[1] == x.rectangle.height:
                    i[1] -= 1
                    suma_2 == True
                if x.mask.get_at(i) == 1:
                    n+=1
                    ns += 1
                    if suma_1 == True:
                        i[0] += 1
                    if suma_2 == True:
                        i[1] += 1
                    i[0] += x.rectangle.topleft[0]
                    i[1] += x.rectangle.topleft[1]
                    if ns == 2:
                        centre  = (pygame.math.Vector2(i)-posició_xoc_s)*0.5 + posició_xoc_s
                        centre2 = (centre - self.rectangle.center).rotate(180) + self.rectangle.center
                        centre = [centre[0], centre[1], centre2[0], centre2[1]]
                    posició_xoc_s = i
                    posició_xoc_x = i
                    rampa_s = x
                    rampa_x = x
                    esquines_xoc.append(pygame.math.Vector2(i))
        nx = 0
        for i in xesquines:
            if self.rectangle.collidepoint(i) or ((i[0] >= self.rectangle.left and i[0] <= self.rectangle.right) and i[1] == self.rectangle.bottom) or ((i[1] >= self.rectangle.top and i[1] <= self.rectangle.bottom) and i[0] == self.rectangle.right):
                i = list(i)
                suma_1 = False
                suma_2 = False
                i[0] -= self.rectangle.topleft[0]
                i[1] -= self.rectangle.topleft[1]
                if i[0] == self.rectangle.width:
                    i[0] -= 1
                    suma_1 = True
                if i[1] == self.rectangle.height:
                    i[1] -= 1
                    suma_2 == True
                if self.mask.get_at(i) == 1:
                    n+=1
                    nx +=1
                    if suma_1 == True:
                        i[0] += 1
                    if suma_2 == True:
                        i[1] += 1
                    i[0] += self.rectangle.topleft[0]
                    i[1] += self.rectangle.topleft[1]
                    if nx == 2:
                        xcentre  = (pygame.math.Vector2(i)-posició_xoc_s)*0.5 + posició_xoc_s
                        xcentre2 = (xcentre - x.rectangle.center).rotate(180) + x.rectangle.center
                        xcentre = [xcentre[0], xcentre[1], xcentre2[0], xcentre2[1]]     
                    if n == 1:
                        posició_xoc_s = i
                        posició_xoc_x = i
                    else:
                        posició_xoc_s = i                      
                    rampa_s = self
                    rampa_x = self
                    xesquines_xoc.append(pygame.math.Vector2(i))
        if ns ==2 and round(self.angle)%90 != round(x.angle)%90 and self.velocitat.length()>1:    
            ns -=1
            n -=1
            if (esquines_xoc[0]-x.rectangle.center).length() < (esquines_xoc[1]-x.rectangle.center).length():
                posició_xoc_s = esquines_xoc[0]
                posició_xoc_x = esquines_xoc[0]
            else:
                posició_xoc_s = esquines_xoc[1]
                posició_xoc_x = esquines_xoc[1]
            rampa_x = x
            rampa_s = x
        if nx ==2 and round(self.angle)%90 != round(x.angle)%90 and x.velocitat.length()>1:    
            nx -=1
            n -=1
            if (xesquines_xoc[0]-self.rectangle.center).length() < (xesquines_xoc[1]-self.rectangle.center).length():
                if n ==1:    
                    posició_xoc_x = xesquines_xoc[0]
                    posició_xoc_s = xesquines_xoc[0]
                else:
                    posició_xoc_s = xesquines_xoc[0]
            else:
                if n ==1:    
                    posició_xoc_x = xesquines_xoc[1]
                    posició_xoc_s = xesquines_xoc[1]
                else:
                    posició_xoc_s = xesquines_xoc[1]
            rampa_x = self
            rampa_s = self
        if n>=2:    
            rampa_x = x
            rampa_s = self
            mask_xoc = self.mask.overlap_mask(x.mask,(x.rectangle.x- self.rectangle.x, x.rectangle.y- self.rectangle.y))        
            rectangle_xoc = mask_xoc.get_bounding_rects()
            posició_xoc = rectangle_xoc[0].center + pygame.math.Vector2(self.rectangle.topleft)
            if ns == 2 or nx == 2:
                rampa_s = x
                rampa_x = self
                rotar = False
                if ns ==2:
                    posició_xoc = (esquines_xoc[0]-esquines_xoc[1])*0.5 +esquines_xoc[1] 
                    if nx == 1:
                        nx -=1
                        n -=1
                    if self.rotar:    
                        self.rotar = False
                        self.centre_no_rotar = centre
                        nou_angle = abs(round(x.angle)%90 + -1*(round(self.angle)%90))
                        nou_angle2 = abs(-1*(round(x.angle)%90)+round(self.angle)%90)
                        if nou_angle >45:
                            nou_angle = 90 -nou_angle
                        if nou_angle2 >45:
                            nou_angle2 = 90 -nou_angle2
                        if nou_angle > nou_angle2:
                            nou_angle = nou_angle2
                        if round(x.angle)%90 == (round(self.angle)- nou_angle)%90:
                            self.angle = round(self.angle) - nou_angle
                        else:
                            self.angle = round(self.angle) + nou_angle
                if nx == 2 and x.movible:
                    if ns == 1:
                        ns -=1
                        n -=1
                    posició_xoc = (xesquines_xoc[0]-xesquines_xoc[1])*0.5 +xesquines_xoc[1]
                    if x.rotar:    
                        x.rotar = False
                        nou_angle = abs(round(x.angle)%90 + -1*(round(self.angle)%90))
                        nou_angle2 = abs(-1*(round(x.angle)%90)+round(self.angle)%90)
                        if nou_angle >45:
                            nou_angle = 90 -nou_angle
                        if nou_angle2 >45:
                            nou_angle2 = 90 -nou_angle2
                        if nou_angle > nou_angle2:
                            nou_angle = nou_angle2
                        if round(self.angle)%90 == (round(x.angle)- nou_angle)%90:
                            x.angle = round(x.angle) - nou_angle
                        else:
                            x.angle = round(x.angle) + nou_angle
                        x.centre_no_rotar = xcentre
                posició_xoc_s = posició_xoc
                posició_xoc_x = posició_xoc
        elif ns == 1:
            mask_xoc = self.mask.overlap_mask(x.mask,(x.rectangle.x- self.rectangle.x, x.rectangle.y- self.rectangle.y))        
            rectangle_xoc = mask_xoc.get_bounding_rects()
            posició_xoc_x = rectangle_xoc[0].center + pygame.math.Vector2(self.rectangle.topleft)
            posició_xoc = posició_xoc_x
        elif nx == 1:
            mask_xoc = self.mask.overlap_mask(x.mask,(x.rectangle.x- self.rectangle.x, x.rectangle.y- self.rectangle.y))        
            rectangle_xoc = mask_xoc.get_bounding_rects()
            posició_xoc_s = rectangle_xoc[0].center + pygame.math.Vector2(self.rectangle.topleft)
            posició_xoc = posició_xoc_s
        elif n == 0:
            rampa_s = x
            rampa_x = self
            mask_xoc = self.mask.overlap_mask(x.mask,(x.rectangle.x- self.rectangle.x, x.rectangle.y- self.rectangle.y))        
            rectangle_xoc = mask_xoc.get_bounding_rects()
            posició_xoc_s = rectangle_xoc[0].center + pygame.math.Vector2(self.rectangle.topleft)
            posició_xoc_x = posició_xoc_s
            posició_xoc = posició_xoc_s
        if n == 3:
            print(nx, ns,n)
        if self.z == 0:
            self.velocitat_angle = 0
            self.z = 1
            llista = []
            for i in self.suma_pes:
                i[2] +=1
                if i[2] == 2:
                    llista.append(i)
            for i in llista:
                self.suma_pes.remove(i)
        if x.z == 0:
            x.z = 1
            x.velocitat_angle = 0
            llista = []
            for i in x.suma_pes:
                i[2] +=1
                if i[2] == 1:
                    llista.append(i)
            for i in llista:
                x.suma_pes.remove(i)
        centre1 = ((esquina1[0]-esquina2[0])/2 + esquina2[0], (esquina1[1]-esquina2[1])/2 + esquina2[1], pygame.math.Vector2(esquina1[0]-esquina2[0],esquina1[1]-esquina2[1])*0.5)
        centre2 = ((esquina1[0]-esquina3[0])/2 + esquina3[0], (esquina1[1]-esquina3[1])/2 + esquina3[1], pygame.math.Vector2(esquina3[0]-esquina1[0],esquina3[1]-esquina1[1])*0.5)
        centre4 = ((esquina4[0]-esquina2[0])/2 + esquina2[0], (esquina4[1]-esquina2[1])/2 + esquina2[1], pygame.math.Vector2(esquina2[0]-esquina4[0],esquina2[1]-esquina4[1])*0.5)
        centre3 = ((esquina4[0]-esquina3[0])/2 + esquina3[0], (esquina4[1]-esquina3[1])/2 + esquina3[1], pygame.math.Vector2(esquina4[0]-esquina3[0],esquina4[1]-esquina3[1])*0.5)
        centres = [centre1, centre2, centre3, centre4]
        if rampa_s == self:
            self.angle_rampa = rampa_s.calcul_angle_rampa(posició_xoc)
            if self.angle_rampa != "no":
                self.angle_rampa += 180
        else:
            self.angle_rampa = rampa_s.calcul_angle_rampa(posició_xoc)
        if self.angle_rampa == "no":
            if rampa_x == self:    
                self.angle_rampa = rampa_x.calcul_angle_rampa(posició_xoc)
                if self.angle_rampa != "no":
                    self.angle_rampa += 180
            else:
                self.angle_rampa = rampa_x.calcul_angle_rampa(posició_xoc)
            if self.angle_rampa == "no":
                self.angle_rampa = 180
        if self.angle_rampa>=360:
            self.angle_rampa-=360
        if self.angle_rampa <= 180:    
            angle_z = 180-self.angle_rampa
        else:
            angle_z = 360-self.angle_rampa + 180
        z = pygame.math.Vector2.from_polar((1, angle_z))
        velocitat = self.velocitat.copy()
        if x.movible == False and n != 0:
            antic_centre = self.rectangle.center
            posició_xoc_s_2 = posició_xoc_s - pygame.math.Vector2(antic_centre)
            while self.mask.overlap(x.mask,(x.rectangle.x-self.rectangle.x, x.rectangle.y-self.rectangle.y)):
                self.rectangle.center+=z
                if self.rotar == False:
                    self.centre_no_rotar[0] += z[0]
                    self.centre_no_rotar[1] += z[1]
                    self.centre_no_rotar[2] += z[0]
                    self.centre_no_rotar[3] += z[1]
            if self.rotar:    
                if nx != 0:
                    for i in centres:
                        vector = pygame.math.Vector2(posició_xoc_s[0]-i[0],posició_xoc_s[1]-i[1])
                        i2_negatiu = i[2].rotate(180)
                        if vector.length() <= i[2].length() and (abs(i[2].angle_to((-1,0)) - vector.angle_to((-1,0))) < 15 or abs(i2_negatiu.angle_to((-1,0)) - vector.angle_to((-1,0)))<15):
                            if abs(i[2].angle_to((-1,0)) - vector.angle_to((-1,0))) <  abs(i2_negatiu.angle_to((-1,0)) - vector.angle_to((-1,0))):
                                self.velocitat_angle += vector.length() * self.velocitat.length()/(0.5*self.amplada)
                            else:
                                self.velocitat_angle -= vector.length() * self.velocitat.length()/(0.5*self.amplada)
            if rotar == False or self.velocitat.length()>=3 or self.velocitat_angle>=1:
                self.pivot_pantalla = self.rectangle.center
                self.pivot = (0.5*self.amplada, self.alçada*0.5)
            else:
                self.pivot_pantalla = posició_xoc_s_2 + self.rectangle.center
                self.pivot =(posició_xoc_s_2.rotate(self.angle) + antic_centre) - pygame.math.Vector2(antic_centre[0]-0.5*self.amplada, antic_centre[1]-0.5*self.alçada)
            if round(x.angle)%90 != round(self.angle)%90 or (nx!=0 and ns ==0) or (nx == 1 and ns == 1 and ((rectangle_xoc[0].width < self.amplada/2) or abs(self.velocitat[1])>0.5)):    
                if (self.angle%90 == 0 and posició_xoc_s[1] >= self.rectangle.bottom) or (nx!= 0 and esquina4[1] > posició_xoc_s[1] and ((esquina2[1] < posició_xoc_s[1] and esquina2[0] > posició_xoc_s[0] and esquina4[0] < posició_xoc_s[0])or(esquina3[1] < posició_xoc_s[1] and esquina3[0] < posició_xoc_s[0] and esquina4[0] > posició_xoc_s[0]))) or posició_xoc_s == esquina4 or posició_xoc_s == esquina3 or posició_xoc_s == esquina2:
                    meitat1 = 0
                    meitat2 = 0
                    for i in self.mask.outline(5):
                        i = list(i)
                        i[0] += self.rectangle.left
                        if i[0] > posició_xoc_s[0]:
                            meitat1+=1
                        elif i[0] < posició_xoc_s[0]:
                            meitat2+=1
                    meitat1+=1
                    meitat2 -=2
                    meitat1_orig = meitat1
                    meitat1 += (self.velocitat[0]- self.velocitat_angle_ax)*(meitat2+meitat1) 
                    meitat2 -= (self.velocitat[0]- self.velocitat_angle_ax)*(meitat1_orig + meitat2) 
                    if meitat1 > (meitat1 + meitat2):
                        meitat1 = (meitat1 + meitat2)
                        meitat2 = 0
                    elif meitat2 > (meitat1 + meitat2):
                        meitat2 = (meitat1 + meitat2)
                        meitat1 = 0
                    total = meitat1 + meitat2
                    if self.suma_pes!=[]:    
                        for i in self.suma_pes:
                            for s in i[0]:      
                                s = list(s)
                                if s[0] > posició_xoc_s[0]:
                                    meitat1+=1
                                elif s[0] < posició_xoc_s[0]:
                                    meitat2+=1
                                else:
                                    meitat1+=1
                    if meitat1 > meitat2 + 3:
                        if abs(centre4[2].length() - 0.5*self.amplada) < abs(centre4[2].length() - 0.5*self.alçada):
                            svelocitat_angle = -abs(self.velocitat[1] * meitat1)/total
                        else:
                            svelocitat_angle = -abs(self.velocitat[1] * meitat1*self.alçada)/(total*self.amplada)
                        if self.rotacions != []:    
                            if round(posició_xoc_s[1]) == self.rotacions[0][1]:
                                self.rotacions.remove(self.rotacions[0])
                        self.rotacions.append((svelocitat_angle, round(posició_xoc_s[1])))
                    elif meitat1 + 3 < meitat2:
                        if abs(centre3[2].length() - 0.5*self.amplada) < abs(centre3[2].length() - 0.5*self.alçada):
                            svelocitat_angle = abs(self.velocitat[1] * meitat2)/total
                        else:
                            svelocitat_angle = abs(self.velocitat[1] * meitat2*self.alçada)/(total*self.amplada)
                        if self.rotacions != []:    
                            if round(posició_xoc_s[1]) == self.rotacions[0][1]:
                                self.rotacions.remove(self.rotacions[0])
                        self.rotacions.append((svelocitat_angle, round(posició_xoc_s[1])))
            elif self.rotar:
                self.angle = round(self.angle)
                self.velocitat_angle = 0
                self.rotar = False
                if self.angle%90 <= 45:
                    self.centre_no_rotar = [centre4[0], centre4[1], centre2[0], centre2[1]]
                else:
                    self.centre_no_rotar = [centre3[0], centre3[1], centre1[0], centre1[1]]
            if self.rotar:
                self.pivot = (round(self.pivot[0]), round(self.pivot[1]))
                self.pivot_pantalla = (round(self.pivot_pantalla[0]), round(self.pivot_pantalla[1]))
            nou_angle_velocitat =180 + 2*self.velocitat.angle_to((-1,0)) - 2*self.angle_rampa
            velocitat.rotate_ip(nou_angle_velocitat)
            velocitat[0] *=0.3 + 0.59*abs(math.sin(math.radians(self.angle_rampa)))
            velocitat[1] *=0.3 + 0.59*abs(math.cos(math.radians(self.angle_rampa)))
            self.conjut_de_velocitats_1.append(velocitat)
        elif n!= 0:
            for i in x.suma_pes:
                if i[1] == self:
                    x.suma_pes.remove(i)
            xsuma_pes = []
            for i in self.mask.outline(5):
                s = pygame.math.Vector2(i)+self.rectangle.topleft  - x.rectangle.topleft
                if s[0] >= 0 and s[0] <= (x.rectangle.width-1):
                    i = list(s+x.rectangle.topleft)
                    xsuma_pes.append(i)
            x.suma_pes.append([xsuma_pes, self, 0])
            if rampa_x == x:    
                x.angle_rampa = rampa_x.calcul_angle_rampa(posició_xoc)
                if x.angle_rampa != "no":
                    x.angle_rampa += 180
            else:
                x.angle_rampa = rampa_x.calcul_angle_rampa(posició_xoc)
            if x.angle_rampa == "no":
                if rampa_s == x:    
                    x.angle_rampa = rampa_s.calcul_angle_rampa(posició_xoc)
                    if x.angle_rampa != "no":
                        x.angle_rampa += 180
                else:
                    x.angle_rampa = rampa_s.calcul_angle_rampa(posició_xoc)
                if x.angle_rampa == "no":
                    x.angle_rampa = 180
            if x.angle_rampa >= 360:
                x.angle_rampa -=360
            xcentre1 = ((xesquina1[0]-xesquina2[0])/2 + xesquina2[0], (xesquina1[1]-xesquina2[1])/2 + xesquina2[1], pygame.math.Vector2(xesquina1[0]-xesquina2[0],xesquina1[1]-xesquina2[1])*0.5)
            xcentre2 = ((xesquina1[0]-xesquina3[0])/2 + xesquina3[0], (xesquina1[1]-xesquina3[1])/2 + xesquina3[1], pygame.math.Vector2(xesquina3[0]-xesquina1[0],xesquina3[1]-xesquina1[1])*0.5)
            xcentre4 = ((xesquina4[0]-xesquina2[0])/2 + xesquina2[0], (xesquina4[1]-xesquina2[1])/2 + xesquina2[1], pygame.math.Vector2(xesquina2[0]-xesquina4[0],xesquina2[1]-xesquina4[1])*0.5)
            xcentre3 = ((xesquina4[0]-xesquina3[0])/2 + xesquina3[0], (xesquina4[1]-xesquina3[1])/2 + xesquina3[1], pygame.math.Vector2(xesquina4[0]-xesquina3[0],xesquina4[1]-xesquina3[1])*0.5)
            xcentres = [xcentre1, xcentre2, xcentre3, xcentre4]
            diferencia_angle_self = abs(self.velocitat.angle_to((-1,0)) - self.angle_rampa)
            if diferencia_angle_self > 180:
                diferencia_angle_self = 360 - diferencia_angle_self
            diferencia_angle_x = abs(x.velocitat.angle_to((-1,0)) - x.angle_rampa)
            if diferencia_angle_x > 180:
                diferencia_angle_x = 360 - diferencia_angle_x
            esperar = False
            suma_velocitat_per_rotació_x = pygame.math.Vector2(0,0)
            esperarx = False
            suma_velocitat_per_rotació = pygame.math.Vector2(0,0)
            antic_centre = self.rectangle.center
            antic_centre_x = x.rectangle.center
            if (diferencia_angle_self > 90 and self.velocitat.length() > 0) or (diferencia_angle_x <= 90 or x.velocitat.length() == 0):
                suma_velocitat_per_rotació_x = self.velocitat 
                while self.mask.overlap(x.mask,(x.rectangle.x-self.rectangle.x, x.rectangle.y-self.rectangle.y)):
                    self.rectangle.center+=z
                nou_centre = self.rectangle.center
                self.rectangle.center = antic_centre 
                for i in llista_objectes_pantalla:
                    if i in llista_objectes_rectangulars and i != self:
                        if i not in self.colisionats and i.movible and i.caixa: 
                            if self.mask.overlap(i.mask,(i.rectangle.x-self.rectangle.x, i.rectangle.y-self.rectangle.y)):
                                self.rectangle.center = nou_centre
                                if not self.mask.overlap(i.mask,(i.rectangle.x-self.rectangle.x, i.rectangle.y-self.rectangle.y)):
                                    esperar = True
                                self.rectangle.center = antic_centre
                if esperar == False:
                    self.rectangle.center = nou_centre
                    if self.rotar == False:    
                        self.centre_no_rotar[0] += nou_centre[0] - antic_centre[0]
                        self.centre_no_rotar[1] += nou_centre[1] - antic_centre[1]
                        self.centre_no_rotar[2] += nou_centre[0] - antic_centre[0]
                        self.centre_no_rotar[3] += nou_centre[1] - antic_centre[1]
            else:
                if x.angle_rampa <= 180:    
                    angle_x = 180-x.angle_rampa
                else:
                    angle_x = 360-x.angle_rampa + 180
                zx = pygame.math.Vector2.from_polar((1, angle_x))   
                while self.mask.overlap(x.mask,(x.rectangle.x-self.rectangle.x, x.rectangle.y-self.rectangle.y)):
                    x.rectangle.center+=zx
                nou_centre = x.rectangle.center
                x.rectangle.center = antic_centre_x 
                for i in llista_objectes_pantalla:
                    if i in llista_objectes_rectangulars and i != x:
                        if i not in x.colisionats and i.movible and i.caixa: 
                            if x.mask.overlap(i.mask,(i.rectangle.x-x.rectangle.x, i.rectangle.y-x.rectangle.y)):
                                x.rectangle.center = nou_centre
                                if not x.mask.overlap(i.mask,(i.rectangle.x-x.rectangle.x, i.rectangle.y-x.rectangle.y)):
                                    esperarx = True
                                x.rectangle.center = antic_centre_x
                if esperarx == False:
                    x.rectangle.center = nou_centre
                    if x.rotar == False:    
                        x.centre_no_rotar[0] += nou_centre[0] - antic_centre_x[0] 
                        x.centre_no_rotar[1] += nou_centre[1] - antic_centre_x[1]
                        x.centre_no_rotar[2] += nou_centre[0] - antic_centre_x[0]
                        x.centre_no_rotar[3] += nou_centre[1] - antic_centre_x[1]
            if diferencia_angle_x > 90 and x.velocitat.length() > 0:
                suma_velocitat_per_rotació = x.velocitat
            posició_xoc_s_2 = posició_xoc_s - pygame.math.Vector2(antic_centre)
            posició_xoc_x_2 = posició_xoc_x - pygame.math.Vector2(antic_centre_x) 
            vector_colisió = pygame.math.Vector2(100000,100000)
            colisió_centre = 0
            if posició_xoc_s not in esquines:
                colisió = False
                for i in centres:
                    vector = pygame.math.Vector2(posició_xoc_s[0]-i[0],posició_xoc_s[1]-i[1])
                    i2_negatiu = i[2].rotate(180)
                    if vector.length() < i[2].length() and vector.length() < vector_colisió.length():
                        colisió_centre = i
                        vector_colisió = vector
                        vector_negatiu = i2_negatiu
                        if i == centre3 or (i == centre4 and self.angle%90 !=0):
                            velocitats = 0
                        else:
                            velocitats = 1
                    if vector.length() == i[2].length() and self.rotar:
                        colisió = True
                        if abs(i[2].angle_to((-1,0)) - vector.angle_to((-1,0))) <  abs(i2_negatiu.angle_to((-1,0)) - vector.angle_to((-1,0))):
                            self.velocitat_angle += vector.length()*(abs(math.sin(math.radians(i[2].angle_to((-1,0)) - self.velocitat.angle_to((-1,0)))) * self.velocitat.length()))/(0.5*self.amplada)
                        else:
                            self.velocitat_angle -= vector.length()*(abs(math.sin(math.radians(i[2].angle_to((-1,0)) - self.velocitat.angle_to((-1,0)))) * self.velocitat.length()))/(0.5*self.amplada)
                if colisió_centre==0:
                    colisió = True
                if nx == 2 and vector_colisió.length() < rectangle_xoc[0].width*0.5:
                    vector_colisió *= 0
                if posició_xoc_s not in esquines and colisió == False:    
                    if self.rotar:
                        if vector_colisió.length()>=2:    
                            if abs(colisió_centre[2].angle_to((-1,0)) - vector_colisió.angle_to((-1,0))) <  abs(vector_negatiu.angle_to((-1,0)) - vector_colisió.angle_to((-1,0))):
                                self.velocitat_angle += vector_colisió.length()*(abs(math.sin(math.radians(colisió_centre[2].angle_to((-1,0)) - self.velocitat.angle_to((-1,0)))) * self.velocitat.length())*velocitats + (suma_velocitat_per_rotació.length()*math.sin(math.radians(colisió_centre[2].angle_to((-1,0)) - suma_velocitat_per_rotació.angle_to((-1,0))))*x.massa/self.massa))/(0.5*self.amplada)
                            else:
                                self.velocitat_angle -= vector_colisió.length()*(abs(math.sin(math.radians(colisió_centre[2].angle_to((-1,0)) - self.velocitat.angle_to((-1,0)))) * self.velocitat.length())*velocitats + (suma_velocitat_per_rotació.length()*math.sin(math.radians(colisió_centre[2].angle_to((-1,0)) - suma_velocitat_per_rotació.angle_to((-1,0))))*x.massa/self.massa))/(0.5*self.amplada)
                    elif (colisió_centre[0] != self.centre_no_rotar[0] or colisió_centre[1] != self.centre_no_rotar[1]) and (colisió_centre[0] != self.centre_no_rotar[2] or colisió_centre[1] != self.centre_no_rotar[3]):
                        distancia_esquina_xoc = pygame.math.Vector2(0,0)
                        for i in esquines:
                            i = list(i)
                            distancia_esquina = pygame.math.Vector2(i[0]- colisió_centre[0], i[1]- colisió_centre[1])
                            if distancia_esquina != colisió_centre[2] and distancia_esquina != vector_negatiu:
                                distancia = pygame.math.Vector2(posició_xoc_s[0]-i[0], posició_xoc_s[1]- i[1])
                                if distancia_esquina_xoc.length() < distancia.length():
                                    distancia_esquina_xoc = distancia
                                    if math.sqrt((self.centre_no_rotar[0]-i[0])**2 + (self.centre_no_rotar[1]-i[1])**2) < math.sqrt((self.centre_no_rotar[2]-i[0])**2 + (self.centre_no_rotar[3]-i[1])**2):
                                        i = pygame.math.Vector2(i)
                                        self.pivot_pantalla = i + self.rectangle.center - antic_centre
                                        self.pivot =((i-antic_centre).rotate(self.angle) + antic_centre) - pygame.math.Vector2(antic_centre[0]-0.5*self.amplada, antic_centre[1]-0.5*self.alçada)
                                    else:
                                        self.pivot_pantalla = self.rectangle.center
                                        self.pivot = (0.5*self.amplada, 0.5*self.alçada)
                        self.rotar = True
                        if abs(colisió_centre[2].angle_to((-1,0)) - vector_colisió.angle_to((-1,0))) <  abs(vector_negatiu.angle_to((-1,0)) - vector_colisió.angle_to((-1,0))):
                            self.velocitat_angle += vector_colisió.length()*(abs(math.sin(math.radians(colisió_centre[2].angle_to((-1,0)) - self.velocitat.angle_to((-1,0)))) * self.velocitat.length())*velocitats + (suma_velocitat_per_rotació.length()*math.sin(math.radians(colisió_centre[2].angle_to((-1,0)) - suma_velocitat_per_rotació.angle_to((-1,0))))*x.massa/self.massa))/(0.5*self.amplada)
                        else:
                            self.velocitat_angle -= vector_colisió.length()*(abs(math.sin(math.radians(colisió_centre[2].angle_to((-1,0)) - self.velocitat.angle_to((-1,0)))) * self.velocitat.length())*velocitats + (suma_velocitat_per_rotació.length()*math.sin(math.radians(colisió_centre[2].angle_to((-1,0)) - suma_velocitat_per_rotació.angle_to((-1,0))))*x.massa/self.massa))/(0.5*self.amplada)
            if rotar == False or self.velocitat.length()>=3 or self.velocitat_angle>=1:
                self.pivot_pantalla = self.rectangle.center
                self.pivot = (0.5*self.amplada, self.alçada*0.5)
            else:
                self.pivot_pantalla = posició_xoc_s_2 + self.rectangle.center
                self.pivot =(posició_xoc_s_2.rotate(self.angle) + antic_centre) - pygame.math.Vector2(antic_centre[0]-0.5*self.amplada, antic_centre[1]-0.5*self.alçada)
            if round(x.angle)%90 != round(self.angle)%90 or (nx!=0 and ns ==0) or (nx == 1 and ns == 1 and ((rectangle_xoc[0].width < self.amplada/2) or abs(self.velocitat[1])>0.5)):    
                if (self.angle%90 == 0 and colisió_centre == centre3) or (self.angle%90!=0 and (colisió_centre == centre3 or colisió_centre == centre4)) or posició_xoc_s == esquina4 or posició_xoc_s == esquina2  or posició_xoc_x == esquina3:
                    meitat1 = 0
                    meitat2 = 0
                    meitat3 = 0
                    if nx !=2:    
                        for i in self.mask.outline(5):
                            i = list(i)
                            i[0] += self.rectangle.left
                            if i[0] > posició_xoc_s[0]:
                                meitat1+=1
                            elif i[0] < posició_xoc_s[0]:
                                meitat2+=1
                            else:
                                meitat3 += 1
                        meitat2-=2
                        meitat1 +=1
                        meitat1_orig = meitat1
                        meitat1 += (self.velocitat[0]- self.velocitat_angle_ax)*(meitat2+meitat1) 
                        meitat2 -= (self.velocitat[0]- self.velocitat_angle_ax)*(meitat1_orig + meitat2) 
                        total = meitat2 + meitat3 + meitat1
                        if meitat1 > total:
                            meitat1 = total
                            meitat2 = 0
                            meitat3 = 0
                        elif meitat2 > total:
                            meitat2 = total
                            meitat1 = 0
                            meitat3 = 0
                        if self.suma_pes!=[]:  
                            meitat4 = 0  
                            for i in self.suma_pes:
                                for s in i[0]:      
                                    s = list(s)
                                    if s[0] > posició_xoc_s[0]:
                                        meitat1+=1
                                    elif s[0] < posició_xoc_s[0]:
                                        meitat2+=1
                                    else:
                                        meitat1+=1
                    else:
                        meitat4 = 0
                        meitat5 = 0
                        meitat6 = 0
                        for i in self.mask.outline(5):
                            i = list(i)
                            i[0] += self.rectangle.left
                            if i[0] > xesquines_xoc[0][0]:
                                meitat1+=1
                            elif i[0] < xesquines_xoc[0][0]:
                                meitat2+=1
                            else:
                                meitat3 += 1
                            if i[0] > xesquines_xoc[1][0]:
                                meitat4+=1
                            elif i[0] < xesquines_xoc[1][0]:
                                meitat5+=1
                            else:
                                meitat6 += 1
                        meitat2-=2
                        meitat1 +=1
                        meitat1_orig = meitat1
                        meitat1 += (self.velocitat[0]- self.velocitat_angle_ax)*(meitat2+meitat1) 
                        meitat2 -= (self.velocitat[0]- self.velocitat_angle_ax)*(meitat1_orig + meitat2)
                        meitat5-=2
                        meitat4 +=1
                        meitat4_orig = meitat4
                        meitat4 += (self.velocitat[0]- self.velocitat_angle_ax)*(meitat5+meitat4) 
                        meitat5 -= (self.velocitat[0]- self.velocitat_angle_ax)*(meitat4_orig + meitat5) 
                        total = meitat2 + meitat3 + meitat1
                        if meitat1 > total:
                            meitat1 = total
                            meitat2 = 0
                            meitat3 = 0
                        elif meitat2 > total:
                            meitat2 = total
                            meitat1 = 0
                            meitat3 = 0
                        if meitat4 > total:
                            meitat4 = total
                            meitat5 = 0
                            meitat6 = 0
                        elif meitat5 > total:
                            meitat5 = total
                            meitat4 = 0
                            meitat6 = 0
                        if self.suma_pes!=[]:  
                            for i in self.suma_pes:
                                for s in i[0]:      
                                    s = list(s)
                                    if s[0] > xesquines_xoc[0][0]:
                                        meitat1+=1
                                    elif s[0] < xesquines_xoc[0][0]:
                                        meitat2+=1
                                    else:
                                        meitat1+=1
                                    if s[0] > xesquines_xoc[1][0]:
                                        meitat4+=1
                                    elif s[0] < xesquines_xoc[1][0]:
                                        meitat5+=1
                                    else:
                                        meitat4+=1
                        if xesquines_xoc[0][0] - xesquines_xoc[1][0]>0:
                            if meitat1<(meitat1+meitat2+meitat3)/2 and meitat5<(meitat4+meitat5+meitat6)/2:
                                meitat1 = 0
                                meitat2 = 0
                                self.rotacions.append((-1,0))
                                self.rotacions.append((1,0))
                            elif meitat5>(meitat4+meitat5+meitat6)/2:
                                meitat1 = meitat4
                                meitat2 = meitat5
                        if xesquines_xoc[0][0] - xesquines_xoc[1][0]<0:
                            if meitat2<(meitat1+meitat2+meitat3)/2 and meitat4<(meitat4+meitat5+meitat6)/2:
                                meitat1 = 0
                                meitat2 = 0
                                self.rotacions.append((-1,0))
                                self.rotacions.append((1,0))
                            elif meitat4>(meitat4+meitat5+meitat6)/2:
                                meitat1 = meitat4
                                meitat2 = meitat5
                    if meitat1 > meitat2+3:
                        self.rotar = True
                        meitat1/= 10
                        meitat1 = round(meitat1)
                        meitat1*=10
                        if posició_xoc_s in esquines:    
                            if abs(centre4[2].length() - 0.5*self.amplada) < abs(centre4[2].length() - 0.5*self.alçada):
                                svelocitat_angle = -abs((self.velocitat[1]) * meitat1*0.5)/(total)
                            else:
                                svelocitat_angle = -abs((self.velocitat[1]) * meitat1*0.5*self.alçada)/((total)*self.amplada)
                        else:
                            if abs(colisió_centre[2].length() - 0.5*self.amplada) < abs(colisió_centre[2].length() - 0.5*self.alçada):
                                svelocitat_angle = -abs((self.velocitat[1]) * meitat1*0.5)/(total)
                            else:
                                svelocitat_angle = -abs((self.velocitat[1]) * meitat1*0.5*self.alçada)/((total)*self.amplada)
                        self.rotacions.append((svelocitat_angle, round(posició_xoc_s[1])))
                    elif meitat1+3 < meitat2:
                        self.rotar = True
                        meitat2/= 10
                        meitat2 = round(meitat2)
                        meitat2*=10
                        if posició_xoc_s in esquines:    
                            if abs(centre3[2].length() - 0.5*self.amplada) < abs(centre3[2].length() - 0.5*self.alçada):
                                svelocitat_angle = abs((self.velocitat[1]) * meitat2*0.5)/(total)
                            else:
                                svelocitat_angle = abs((self.velocitat[1]) * meitat2*0.5*self.alçada)/((total)*self.amplada)
                        else:
                            if abs(colisió_centre[2].length() - 0.5*self.amplada) < abs(colisió_centre[2].length() - 0.5*self.alçada):
                                svelocitat_angle = abs((self.velocitat[1]) * meitat2*0.5)/(total)
                            else:
                                svelocitat_angle = abs((self.velocitat[1]) * meitat2*0.5*self.alçada)/((total)*self.amplada)
                        self.rotacions.append((svelocitat_angle, round(posició_xoc_s[1])))
            elif self.rotar:
                self.angle = round(self.angle)
                self.velocitat_angle = 0
                self.rotar = False
                if self.angle%90 <= 45:
                    self.centre_no_rotar = [centre4[0], centre4[1], centre2[0], centre2[1]]
                else:
                    self.centre_no_rotar = [centre3[0], centre3[1], centre1[0], centre1[1]]
            xvector_colisió = pygame.math.Vector2(100000,100000)
            xcolisió_centre = 0
            xcolisió = False
            if posició_xoc_x not in xesquines:
                for i in xcentres:
                    vector = pygame.math.Vector2(posició_xoc_x[0]-i[0],posició_xoc_x[1]-i[1])
                    i2_negatiu = i[2].rotate(180)
                    if vector.length() <= i[2].length() and vector.length() < xvector_colisió.length():
                        xcolisió_centre = i
                        xvector_colisió = vector
                        xvector_negatiu = i2_negatiu
                        if i == xcentre3 or (i == xcentre4 and x.angle%90 !=0):
                            xvelocitat = 0
                        else:
                            xvelocitat = 1
                    if vector.length() == i[2].length() and x.rotar:
                        xcolisió = True
                        if abs(i[2].angle_to((-1,0)) - vector.angle_to((-1,0))) <  abs(i2_negatiu.angle_to((-1,0)) - vector.angle_to((-1,0))):
                            x.velocitat_angle += vector.length()*(abs(math.sin(math.radians(i[2].angle_to((-1,0)) - x.velocitat.angle_to((-1,0)))) * x.velocitat.length()))/(0.5*x.amplada)
                        else:
                            x.velocitat_angle -= vector.length()*(abs(math.sin(math.radians(i[2].angle_to((-1,0)) - x.velocitat.angle_to((-1,0)))) * x.velocitat.length()))/(0.5*x.amplada)
                if xcolisió_centre==0:
                    xcolisió = True
                if ns == 2 and vector_colisió.length() < rectangle_xoc[0].width*0.5:
                    xvector_colisió *= 0
                if posició_xoc_x not in xesquines and xcolisió == False:    
                    if x.rotar:
                        if xvector_colisió.length()>=2:
                            if abs(xcolisió_centre[2].angle_to((-1,0)) - xvector_colisió.angle_to((-1,0))) <  abs(xvector_negatiu.angle_to((-1,0)) - xvector_colisió.angle_to((-1,0))):
                                x.velocitat_angle += xvector_colisió.length()*(abs(math.sin(math.radians(xcolisió_centre[2].angle_to((-1,0)) - x.velocitat.angle_to((-1,0)))) * x.velocitat.length())*xvelocitat + (suma_velocitat_per_rotació_x.length()*math.sin(math.radians(xcolisió_centre[2].angle_to((-1,0)) - suma_velocitat_per_rotació_x.angle_to((-1,0))))*self.massa/x.massa))/(0.5*x.amplada)
                            else:
                                x.velocitat_angle -= xvector_colisió.length()*(abs(math.sin(math.radians(xcolisió_centre[2].angle_to((-1,0)) - x.velocitat.angle_to((-1,0)))) * x.velocitat.length())*xvelocitat + (suma_velocitat_per_rotació_x.length()*math.sin(math.radians(xcolisió_centre[2].angle_to((-1,0)) - suma_velocitat_per_rotació_x.angle_to((-1,0))))*self.massa/x.massa))/(0.5*x.amplada)
                    elif (xcolisió_centre[0] != x.centre_no_rotar[0] or xcolisió_centre[1] != x.centre_no_rotar[1]) and (xcolisió_centre[0] != x.centre_no_rotar[2] or xcolisió_centre[1] != x.centre_no_rotar[3]):   
                        distancia_esquina_xoc = pygame.math.Vector2(0,0)
                        for i in xesquines:
                            i = list(i)
                            distancia_esquina = pygame.math.Vector2(i[0]- xcolisió_centre[0], i[1]- xcolisió_centre[1])
                            if distancia_esquina != xcolisió_centre[2] and distancia_esquina != xvector_negatiu:
                                distancia = pygame.math.Vector2(posició_xoc_x[0]-i[0], posició_xoc_x[1]- i[1])
                                if distancia_esquina_xoc.length() < distancia.length():
                                    distancia_esquina_xoc = distancia
                                    if math.sqrt((x.centre_no_rotar[0]-i[0])**2 + (x.centre_no_rotar[1]-i[1])**2) < math.sqrt((x.centre_no_rotar[2]-i[0])**2 + (x.centre_no_rotar[3]-i[1])**2):
                                        i = pygame.math.Vector2(i)
                                        x.pivot_pantalla = i + x.rectangle.center - antic_centre_x
                                        x.pivot =((i-antic_centre_x).rotate(x.angle) + antic_centre_x) - pygame.math.Vector2(antic_centre_x[0]-0.5*x.amplada, antic_centre_x[1]-0.5*x.alçada)
                                    else:
                                        x.pivot_pantalla = x.rectangle.center
                                        x.pivot = (0.5*x.amplada, 0.5*x.alçada)
                        x.rotar = True
                        if abs(xcolisió_centre[2].angle_to((-1,0)) - xvector_colisió.angle_to((-1,0))) <  abs(xvector_negatiu.angle_to((-1,0)) - xvector_colisió.angle_to((-1,0))):
                            x.velocitat_angle += xvector_colisió.length()*(abs(math.sin(math.radians(xcolisió_centre[2].angle_to((-1,0)) - x.velocitat.angle_to((-1,0)))) * x.velocitat.length())*xvelocitat + (suma_velocitat_per_rotació_x.length()*math.sin(math.radians(xcolisió_centre[2].angle_to((-1,0)) - suma_velocitat_per_rotació_x.angle_to((-1,0))))*self.massa/x.massa))/(0.5*x.amplada)
                        else:
                            x.velocitat_angle -= xvector_colisió.length()*(abs(math.sin(math.radians(xcolisió_centre[2].angle_to((-1,0)) - x.velocitat.angle_to((-1,0)))) * x.velocitat.length())*xvelocitat + (suma_velocitat_per_rotació_x.length()*math.sin(math.radians(xcolisió_centre[2].angle_to((-1,0)) - suma_velocitat_per_rotació_x.angle_to((-1,0))))*self.massa/x.massa))/(0.5*x.amplada)
            if rotar == False or x.velocitat.length()>=3 or x.velocitat_angle>=1:
                x.pivot_pantalla = x.rectangle.center
                x.pivot = (0.5*x.amplada, x.alçada*0.5)
            else:
                x.pivot_pantalla = posició_xoc_x_2 + x.rectangle.center
                x.pivot =(posició_xoc_x_2.rotate(x.angle) + antic_centre_x) - pygame.math.Vector2(antic_centre_x[0]-0.5*x.amplada, antic_centre_x[1]-0.5*x.alçada)    
            if round(x.angle)%90 != round(self.angle)%90 or (ns!=0 and nx ==0) or (nx == 1 and ns == 1 and ((rectangle_xoc[0].width < x.amplada/2) or abs(x.velocitat[1])>0.5)):    
                if (x.angle%90 == 0 and xcolisió_centre == xcentre3) or (x.angle%90!=0 and (xcolisió_centre == xcentre3 or xcolisió_centre == xcentre4)) or posició_xoc_x == xesquina4 or posició_xoc_x == xesquina2  or posició_xoc_x == xesquina3:
                    xmeitat1 = 0
                    xmeitat2 = 0
                    xmeitat3 = 0
                    if ns != 2:     
                        for i in x.mask.outline(5):
                            i = list(i)
                            i[0] += x.rectangle.left
                            if i[0] > posició_xoc_x[0]:
                                xmeitat1+=1
                            elif i[0] < posició_xoc_x[0]:
                                xmeitat2+=1
                            else:
                                xmeitat3+=1
                        xmeitat2 -=2
                        xmeitat1 +=1
                        xmeitat1_orig = xmeitat1
                        xmeitat1 += (x.velocitat[0]- x.velocitat_angle_ax)*(xmeitat2+xmeitat1) 
                        xmeitat2 -= (x.velocitat[0]- x.velocitat_angle_ax)*(xmeitat1_orig + xmeitat2) 
                        xtotal = xmeitat1 + xmeitat2 + xmeitat3
                        if xmeitat1 > xtotal:
                            xmeitat1 = xtotal
                            xmeitat2 = 0
                            xmeitat3 = 0
                        elif xmeitat2 > xtotal:
                            xmeitat2 = xtotal
                            xmeitat1 = 0
                            xmeitat3 = 0 
                        if x.suma_pes!=[]:      
                            for i in x.suma_pes:
                                for s in i[0]:        
                                    s = list(s)
                                    if s[0] > posició_xoc_x[0]:
                                        xmeitat1+=1
                                    elif s[0] < posició_xoc_x[0]:
                                        xmeitat2+=1
                                    else:
                                        xmeitat1 +=1
                    else:
                        xmeitat4 = 0
                        xmeitat5 = 0
                        xmeitat6 = 0
                        for i in x.mask.outline(5):
                            i = list(i)
                            i[0] += x.rectangle.left
                            if i[0] > esquines_xoc[0][0]:
                                xmeitat1+=1
                            elif i[0] < esquines_xoc[0][0]:
                                xmeitat2+=1
                            else:
                                xmeitat3 += 1
                            if i[0] > esquines_xoc[1][0]:
                                xmeitat4+=1
                            elif i[0] < esquines_xoc[1][0]:
                                xmeitat5+=1
                            else:
                                xmeitat6 += 1
                        xmeitat2-=2
                        xmeitat1 +=1
                        xmeitat1_orig = xmeitat1
                        xmeitat1 += (x.velocitat[0]- x.velocitat_angle_ax)*(xmeitat2+xmeitat1) 
                        xmeitat2 -= (x.velocitat[0]- x.velocitat_angle_ax)*(xmeitat1_orig + xmeitat2)
                        xmeitat5-=2
                        xmeitat4 +=1
                        xmeitat4_orig = xmeitat4
                        xmeitat4 += (x.velocitat[0]- x.velocitat_angle_ax)*(xmeitat5+xmeitat4) 
                        xmeitat5 -= (x.velocitat[0]- x.velocitat_angle_ax)*(xmeitat4_orig + xmeitat5) 
                        xtotal = xmeitat2 + xmeitat3 + xmeitat1
                        if xmeitat1 > xtotal:
                            xmeitat1 = xtotal
                            xmeitat2 = 0
                            xmeitat3 = 0
                        elif xmeitat2 > xtotal:
                            xmeitat2 = xtotal
                            xmeitat1 = 0
                            xmeitat3 = 0
                        if xmeitat4 > xtotal:
                            xmeitat4 = xtotal
                            xmeitat5 = 0
                            xmeitat6 = 0
                        elif xmeitat5 > xtotal:
                            xmeitat5 = xtotal
                            xmeitat4 = 0
                            xmeitat6 = 0
                        if x.suma_pes!=[]:  
                            for i in x.suma_pes:
                                for s in i[0]:      
                                    s = list(s)
                                    if s[0] > esquines_xoc[0][0]:
                                        xmeitat1+=1
                                    elif s[0] < esquines_xoc[0][0]:
                                        xmeitat2+=1
                                    else:
                                        xmeitat1+=1
                                    if s[0] > esquines_xoc[1][0]:
                                        xmeitat4+=1
                                    elif s[0] < esquines_xoc[1][0]:
                                        xmeitat5+=1
                                    else:
                                        xmeitat4+=1
                        if esquines_xoc[0][0] - esquines_xoc[1][0]>0:
                            if xmeitat1<(xmeitat1+xmeitat2+xmeitat3)/2 and xmeitat5<(xmeitat4+xmeitat5+xmeitat6)/2:
                                xmeitat1 = 0
                                xmeitat2 = 0
                                x.rotacions.append((-1,0))
                                x.rotacions.append((1,0))
                            elif xmeitat5>(xmeitat4+xmeitat5+xmeitat6)/2:
                                xmeitat1 = xmeitat4
                                xmeitat2 = xmeitat5
                        if esquines_xoc[0][0] - esquines_xoc[1][0]<0:
                            if xmeitat2<(xmeitat1+xmeitat2+xmeitat3)/2 and xmeitat4<(xmeitat4+xmeitat5+xmeitat6)/2:
                                xmeitat1 = 0
                                xmeitat2 = 0
                                x.rotacions.append((-1,0))
                                x.rotacions.append((1,0))
                            elif xmeitat4>(xmeitat4+xmeitat5+xmeitat6)/2:
                                xmeitat1 = xmeitat4
                                xmeitat2 = xmeitat5 
                    if xmeitat1 > xmeitat2+3:
                        x.rotar = True
                        xmeitat1/= 10
                        xmeitat1 = round(xmeitat1)
                        xmeitat1*=10
                        if posició_xoc_x in xesquines:    
                            if abs(xcentre4[2].length() - 0.5*x.amplada) < abs(xcentre4[2].length() - 0.5*x.alçada):
                                xvelocitat_angle = -abs((x.velocitat[1]) * xmeitat1*0.5)/xtotal
                            else:
                                xvelocitat_angle = -abs((x.velocitat[1]) * xmeitat1*0.5*x.alçada)/(xtotal*x.amplada)
                        else:
                            if abs(xcolisió_centre[2].length() - 0.5*x.amplada) < abs(xcolisió_centre[2].length() - 0.5*x.alçada):
                                xvelocitat_angle = -abs((x.velocitat[1]) * xmeitat1*0.5)/xtotal
                            else:
                                xvelocitat_angle =- abs((x.velocitat[1]) * xmeitat1*0.5*x.alçada)/(xtotal*x.amplada)
                        x.rotacions.append((xvelocitat_angle, round(posició_xoc_x[1])))
                    elif 3+xmeitat1 < xmeitat2:
                        x.rotar = True
                        xmeitat2/= 10
                        xmeitat2 = round(xmeitat2)
                        xmeitat2*=10
                        if posició_xoc_x in xesquines:    
                            if abs(xcentre3[2].length() - 0.5*x.amplada) < abs(xcentre3[2].length() - 0.5*x.alçada):
                                xvelocitat_angle = abs((x.velocitat[1]) * xmeitat2*0.5)/xtotal
                            else:
                                xvelocitat_angle = abs((x.velocitat[1]) * xmeitat2*0.5*x.alçada)/(xtotal*x.amplada)
                        else:
                            if abs(xcolisió_centre[2].length() - 0.5*x.amplada) < abs(xcolisió_centre[2].length() - 0.5*x.alçada):
                                xvelocitat_angle = abs((x.velocitat[1]) * xmeitat2*0.5)/xtotal
                            else:
                                xvelocitat_angle = abs((x.velocitat[1]) * xmeitat2*0.5*x.alçada)/(xtotal*x.amplada)
                        x.rotacions.append((xvelocitat_angle, round(posició_xoc_s[1]))) 
            elif self.rotar:
                x.angle = round(x.angle)
                x.velocitat_angle = 0
                x.rotar = False
                if x.angle%90 <= 45:
                    x.centre_no_rotar = [xcentre4[0], xcentre4[1], xcentre2[0], xcentre2[1]]
                else:
                    x.centre_no_rotar = [xcentre3[0], xcentre3[1], xcentre1[0], xcentre1[1]]
            if diferencia_angle_self > 90 and self.velocitat.length() > 0 :    
                nou_angle_velocitat = 180+2*self.velocitat.angle_to((-1,0)) - 2*self.angle_rampa 
                velocitat.rotate_ip(nou_angle_velocitat)
                velocitat[0] *=0.3 + 0.59*abs(math.sin(math.radians(self.angle_rampa)))
                velocitat[1] *=0.3 + 0.59*abs(math.cos(math.radians(self.angle_rampa)))
                self.conjut_de_velocitats_1.append(velocitat)
            if diferencia_angle_self < 100 and diferencia_angle_x >= 90 and x.velocitat.length() >= 2:
                velocitat*=0
                velocitat[0] += x.velocitat[0]*0.4*x.massa/self.massa
                velocitat[1] += x.velocitat[1]*0.4*x.massa/self.massa
                self.conjut_de_velocitats_2.append(velocitat)
            velocitat2 = x.velocitat.copy()            
            if diferencia_angle_x > 90 and x.velocitat.length() > 0:
                nou_angle_velocitat_2 = 180 + 2*x.velocitat.angle_to((-1,0)) - 2*x.angle_rampa 
                velocitat2.rotate_ip(nou_angle_velocitat_2)
                velocitat2[0] *=0.3 + 0.59*abs(math.sin(math.radians(x.angle_rampa)))
                velocitat2[1] *=0.3 + 0.59*abs(math.cos(math.radians(x.angle_rampa)))
                x.conjut_de_velocitats_1.append(velocitat2)
            if diferencia_angle_x < 100 and diferencia_angle_self >= 90 and self.velocitat.length() >= 2:
                velocitat2*=0
                velocitat2[0] += self.velocitat[0]*0.4*self.massa/x.massa
                velocitat2[1] += self.velocitat[1]*0.4**self.massa/x.massa
                x.conjut_de_velocitats_2.append(velocitat2)
            self.velocitat_angle = round(self.velocitat_angle,3)
            x.velocitat_angle = round(x.velocitat_angle,3)
            if x.rotar:
                x.pivot = (round(x.pivot[0]), round(x.pivot[1]))
                x.pivot_pantalla = (round(x.pivot_pantalla[0]), round(x.pivot_pantalla[1]))
            if self.rotar:
                self.pivot = (round(self.pivot[0]), round(self.pivot[1]))
                self.pivot_pantalla = (round(self.pivot_pantalla[0]), round(self.pivot_pantalla[1]))
    def destrucció(self):
        self.velocitat *= 0
        self.angle_rampa = 90
        self.velocitat_angle = 0
        self.colisionats.clear()
        self.conjut_de_velocitats_1.clear()
        self.conjut_de_velocitats_2.clear()
        self.suma_pes.clear()
        self.rotacions.clear()
        self.caixa = False
        radi = self.massa/100
        self.animació = [[radi,self.rectangle.center],[radi,self.rectangle.center],[radi,self.rectangle.center],[radi,self.rectangle.center]]
    def mig_trencat(self, força):
        self.vida -= round(força)
        if self.vida <= 0:
            self.destrucció()
        elif self.vida <=2:
            self.superficie_rectangle.fill(vermell2)
            if self.amplada < self.alçada:    
                pygame.draw.rect(self.superficie_rectangle, self.color_borde , ((0,0), (self.amplada, self.alçada)), 10 - (100//self.amplada))
            else:
                pygame.draw.rect(self.superficie_rectangle, self.color_borde , ((0,0), (self.amplada, self.alçada)), 10 - (100//self.alçada))
    def copy(self, posició):
        x = caixa(posició,self.alçada, self.amplada,self.movible,self.angle_inicial, self.tipo)
        return x
    def reinici(self):
        self.superficie_rectangle.fill(self.color)
        if self.amplada < self.alçada:    
            pygame.draw.rect(self.superficie_rectangle, self.color_borde , ((0,0), (self.amplada, self.alçada)), 10 - (100//self.amplada))
        else:
            pygame.draw.rect(self.superficie_rectangle, self.color_borde , ((0,0), (self.amplada, self.alçada)), 10 - (100//self.alçada))
        self.velocitat *= 0
        self.angle = self.angle_inicial
        self.rectangle_nou = pygame.transform.rotate(self.superficie_rectangle, self.angle)
        self.rectangle = self.rectangle_nou.get_rect()
        self.rectangle.center = self.posició_inicial 
        self.posició_real = self.posició_inicial
        self.mask = pygame.mask.from_surface(self.rectangle_nou)
        self.x = self.mask.outline(5)
        self.angle_rampa = 90
        self.velocitat_angle = 0
        self.colisionats.clear()
        self.conjut_de_velocitats_1.clear()
        self.conjut_de_velocitats_2.clear()
        self.suma_pes.clear()
        self.rotacions.clear()
        self.caixa = True

terra = caixa([pantalla_amplada/2, pantalla_alçada + 50], 100, pantalla_amplada+100, False, 0,2)
quadrat_petit = caixa([pantalla_amplada - 255, pantalla_alçada-48], 50, 50, True, 0,1)
rectangle_petit = caixa([pantalla_amplada - 230, pantalla_alçada-175], 20, 70, True, 90,2)
rectangle_normal = caixa([pantalla_amplada - 180, pantalla_alçada-245], 20, 150, True, 0,2)
quadrat_gran = caixa([pantalla_amplada - 180, pantalla_alçada-315], 60, 60, True, 0,3)
rectangle_gran = caixa([pantalla_amplada - 180, pantalla_alçada-105], 20, 200, True, 0,2)

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
        
        pantalla.fill(fons)
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

        pantalla.fill(fons)

        font = pygame.font.Font(None, 300)
        text = font.render("Angry Birds", True, taronja)
        pantalla.blit(text, (pantalla_amplada // 2 - text.get_width() // 2, pantalla_alçada // 2 - text.get_height() // 2))

        pygame.display.flip()
def pantalla_final(tipo, estrelles):
    if tipo == True:
        texto = "VICTORIA"
    else:
        texto = "DERROTA"
    while True:
        color = estrelles
        n = 3
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE:
                    return False
        pantalla.fill(fons)
        
        font = pygame.font.Font(None, 300)
        text = font.render(texto, True, taronja)
        pantalla.blit(text, (pantalla_amplada // 2 - text.get_width() // 2, pantalla_alçada // 3 - text.get_height() // 2))
        while n >0:
            if color >0:
                color_estrella = taronja
            else:
                color_estrella = gris
            z = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
            x = [pygame.math.Vector2(0, -100),pygame.math.Vector2(0, 50).rotate(72*3) , pygame.math.Vector2(0, -100).rotate(72),pygame.math.Vector2(0, 50).rotate(72*4), pygame.math.Vector2(0, -100).rotate(72*2), pygame.math.Vector2(0, 50), pygame.math.Vector2(0, -100).rotate(72*3),pygame.math.Vector2(0, 50).rotate(72), pygame.math.Vector2(0, -100).rotate(72*4), pygame.math.Vector2(0, 50).rotate(72*2)]
            for i in z:
                i*=1.3
                i +=(pantalla_amplada*(3-n)/3+225,pantalla_alçada-250)
            for i in x:
                i += (pantalla_amplada*(3-n)/3+225,pantalla_alçada-250)
            pygame.draw.polygon(pantalla, taronja3, z)
            pygame.draw.polygon(pantalla, color_estrella, x)
            n-=1
            color-=1
        pygame.display.flip()
#Definim reinici al sortir del nivell
def reinici():
    global llista_objectes_pantalla
    global sprites
    global llista_ocells_llançats
    for i in sprites:
        i.reinici()
    llista_objectes_pantalla = [terra]
    sprites = [terra]
    llista_ocells_llançats = [no_ocell]
# Game GameLoop
def GameLoop():
    global nivell_actual
    global nombre_porcs
    zona_ocell = False
    mantenint_ocell = False
    partida = False
    nivell = [bombardero.copy(), pequeñin.copy(), estrella.copy(), racista.copy(), vermellet.copy(), racista.copy()]
    nivell1 = [rectangle_gran, quadrat_petit,quadrat_petit.copy([pantalla_amplada - 105, pantalla_alçada-48]),rectangle_petit,rectangle_petit.copy([pantalla_amplada - 130, pantalla_alçada-175]),rectangle_normal, quadrat_gran,quadrat_petit.copy([pantalla_amplada - 505, pantalla_alçada-48]),quadrat_petit.copy([pantalla_amplada - 355, pantalla_alçada-48]),rectangle_petit.copy([pantalla_amplada - 480, pantalla_alçada-175]),rectangle_petit.copy([pantalla_amplada - 380, pantalla_alçada-175]),rectangle_normal.copy([pantalla_amplada - 430, pantalla_alçada-245]),quadrat_gran.copy([pantalla_amplada - 430, pantalla_alçada-315]),rectangle_gran.copy([pantalla_amplada - 430, pantalla_alçada-105]), porc_estandar, porc_estandar.copy((pantalla_amplada - 430, pantalla_alçada - 160))]
    nivell2 = []
    while True:
        if not partida:
            reinici()
            mantenint_ocell = False
            if not menú():
                break
            partida = True
            n = 0
            nombre_porcs = 0
            nombre_porcs_orig = 0
        else:
            perdut = True
            if n==0:
                if nivell_actual == 1:
                    sprites.extend(nivell1)
                    llista_objectes_pantalla.extend(nivell1)
                if nivell_actual == 2:
                    sprites.extend(nivell2)
                    llista_objectes_pantalla.extend(nivell2)
                for i in llista_objectes_pantalla:
                    if i in llista_porcs:
                        nombre_porcs+=1
                        nombre_porcs_orig += 1
                n =1
            ocell_actual =  llista_ocells_llançats[següent_ocell(nivell[0], nivell[1], nivell[2], nivell[3], nivell[4], nivell[5])]
            if len(llista_ocells_llançats) > 1:
                ocell_anterior =  llista_ocells_llançats[següent_ocell(nivell[0], nivell[1], nivell[2], nivell[3], nivell[4], nivell[5])-1]
            zona_ocell = ocell_actual.zona_llançament()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    partida = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        partida = False
                if event.type == pygame.MOUSEBUTTONDOWN and zona_ocell:
                    mantenint_ocell = True
                    ocell_actual.linea_direció = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if mantenint_ocell:
                        mantenint_ocell = False
                        ocell_actual.linea_direció = False
                        ocell_actual.llançament()
                    elif ocell_anterior.tocat_objecte == False:
                        ocell_anterior.habilitat()
            # Netejar la pantalla
            pantalla.fill(fons)
            # Aparèixer porcs, ocells i linea
            linea(ocell_actual,mantenint_ocell)
            if ocell_anterior.llançat:    
                ocell_anterior.estela()
            for i in  llista_objectes_pantalla:
                i.update()
                if i in llista_ocells and i !=  no_ocell:
                    perdut = False
            llista_objectes_pantalla.sort(key=lambda i: i.rectangle.center[1])
            for self in llista_objectes_pantalla:
                if self in llista_ocells:
                    if self.llançat:    
                        for i in llista_objectes_pantalla:
                            if i in llista_ocells:    
                                if i.llançat and i.colisionat==False and i!= self: 
                                    if self.rectangle.colliderect(i.rectangle):
                                        if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):
                                            self.colisió(i)
                            elif i in llista_objectes_rectangulars:    
                                if self.rectangle.colliderect(i.rectangle) and i.caixa: 
                                    if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):    
                                        self.colisió(i)
                            else:    
                                if self.rectangle.colliderect(i.rectangle) and i.porc: 
                                    if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):    
                                        self.colisió(i)
                    self.colisionat = True
                if self in llista_objectes_rectangulars:
                    if self.movible and self.caixa:    
                        for i in llista_objectes_pantalla:
                            if i != self and i.colisionat == False and i in llista_objectes_rectangulars:
                                if self.rectangle.colliderect(i.rectangle) and i.caixa:
                                    if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):
                                        self.colisió(i)
                if self in llista_porcs:
                    if self.porc:    
                        for i in llista_objectes_pantalla:
                            if i in llista_ocells:    
                                if i.llançat and i.colisionat==False: 
                                    if self.rectangle.colliderect(i.rectangle):
                                        if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):
                                            self.colisió(i)
                            elif i in llista_objectes_rectangulars:    
                                if self.rectangle.colliderect(i.rectangle) and i.caixa: 
                                    if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):    
                                        self.colisió(i)
                            elif i!= self and i.porc:    
                                if self.rectangle.colliderect(i.rectangle): 
                                    if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):    
                                        self.colisió(i)
                            self.colisionat = True
            for i in  llista_objectes_pantalla:
                i.dibuixar()
            linea_ocells(nivell[0], nivell[1], nivell[2], nivell[3], nivell[4], nivell[5],)
            pygame.draw.line(pantalla, marró, punt_t1, punt_t2, width = 20)
            if nombre_porcs == 0:
                z = nombre_porcs_orig - (len(llista_ocells_llançats)-3)
                z+=3
                if z < 1:
                    z = 1
                pantalla_final(True,z)
                partida = False
            if perdut == True:
                pantalla_final(False,0)
                partida = False
        # Recarregar la pantalla
        pygame.display.flip()
    # Sortir del joc
    pygame.quit()

# Córrer el joc
GameLoop()
