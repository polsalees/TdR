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
verd = (0, 255, 0)
blau = (0, 0, 255)
cian = (0, 255, 255)
rosa = (255, 0, 255)
groc = (255, 255, 0)
taronja = (255, 165, 0)
marró = (128, 64, 0)
marró_fosc = (84, 56, 34)
fons = (80, 80, 255)

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

#Posició inicial ocells
posició_inicial = [200, pantalla_alçada-240]

#Creació funcions basiques
def calcular_angle():
    angle = math.degrees(math.atan2(pygame.mouse.get_pos()[0] - posició_inicial[0], pygame.mouse.get_pos()[1] - posició_inicial[1]))
    return angle

def distancia_ocell_ratoli():
    amplada = math.sqrt(((pygame.mouse.get_pos()[0] - posició_inicial[0]) **2 + (pygame.mouse.get_pos()[1] - posició_inicial[1]) ** 2))
    return amplada

# Creació ocells
class ocells():
    def __init__(self, radi, color):
        global gravetat
        self.radi = radi
        self.posició = [posició_inicial[0], posició_inicial[1]]
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
        self.rectangle.center = (self.posició[0], self.posició[1])
        pygame.draw.circle(self.superficie_ocell, self.color, (self.radi, self.radi), self.radi)
        self.mask = pygame.mask.from_surface(self.superficie_ocell)
    
    def calcul_posició_primer_xoc (self):
        if self.tocat_objecte == False:
            self.posició_primer_xoc = [self.posició[0], self.posició[1]]
            self.tocat_objecte = True
    
    def calcul_angle_cercle(self, pos):
        vector_angle = pygame.math.Vector2(pos[0]-self.posició[0], pos[1]-self.posició[1])
        s = vector_angle.angle_to((-1,0)) + 180
        if s >= 360:
            s -=360
        return s
    
    def colisió(self,x):
        self.calcul_posició_primer_xoc()
        if x in llista_objectes_rodons:    
            if x in llista_ocells:     
                x.calcul_posició_primer_xoc()
            self.angle_rampa = self.calcul_angle_cercle(x.posició)
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
            if diferencia_angle_self > 90 and self.velocitat.length() > 0 :    
                self.posició = [self.posició_antiga[0], self.posició_antiga[1]]
                nou_angle_velocitat = 180+2*self.velocitat.angle_to((-1,0)) - 2*self.angle_rampa 
                self.velocitat.rotate_ip(nou_angle_velocitat)
                self.velocitat[0] *=0.3 + 0.59*math.sqrt(math.sin(math.radians(x.angle_rampa))**2)
                self.velocitat[1] *=0.3 + 0.59*math.sqrt(math.cos(math.radians(x.angle_rampa))**2)
            elif diferencia_angle_x > 90 and x.velocitat.length() >= 2:
                self.velocitat[0] += x.velocitat[0]*0.4
                self.velocitat[1] += x.velocitat[1]*0.4           
            if diferencia_angle_x > 90 and x.velocitat.length() > 0:
                x.posició = [x.posició_antiga[0], x.posició_antiga[1]]
                nou_angle_velocitat_2 = 180 + 2*x.velocitat.angle_to((-1,0)) - 2*x.angle_rampa 
                x.velocitat.rotate_ip(nou_angle_velocitat_2)
                x.velocitat[0] *=0.3 + 0.59*math.sqrt(math.sin(math.radians(x.angle_rampa))**2)
                x.velocitat[1] *=0.3 + 0.59*math.sqrt(math.cos(math.radians(x.angle_rampa))**2)
            elif diferencia_angle_self > 90 and velocitat_inicial.length() >= 2 :
                x.velocitat[0] += velocitat_inicial[0]*0.4
                x.velocitat[1] += velocitat_inicial[1]*0.4
        if x in llista_objectes_rectangulars:
            if self.velocitat.length() > 8 and x.movible:
                llista_objectes_pantalla.remove(x)
                self.velocitat *= 0.4
            else:
                self.angle_rampa = x.calcul_angle_rampa(self.posició)
                if x.movible == False:
                    self.posició = [self.posició_antiga[0], self.posició_antiga[1]]
                    nou_angle_velocitat =180 + 2*self.velocitat.angle_to((-1,0)) - 2*self.angle_rampa
                    self.velocitat.rotate_ip(nou_angle_velocitat)
                    self.velocitat[0] *=0.3 + 0.59*math.sqrt(math.sin(math.radians(self.angle_rampa))**2)
                    self.velocitat[1] *=0.3 + 0.59*math.sqrt(math.cos(math.radians(self.angle_rampa))**2)
                else:
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
                    if diferencia_angle_self > 90 and self.velocitat.length() > 0 :    
                        self.posició = [self.posició_antiga[0], self.posició_antiga[1]]
                        nou_angle_velocitat = 180+2*self.velocitat.angle_to((-1,0)) - 2*self.angle_rampa 
                        self.velocitat.rotate_ip(nou_angle_velocitat)
                        self.velocitat[0] *=0.3 + 0.59*math.sqrt(math.sin(math.radians(x.angle_rampa))**2)
                        self.velocitat[1] *=0.3 + 0.59*math.sqrt(math.cos(math.radians(x.angle_rampa))**2)
                    elif diferencia_angle_x > 90 and x.velocitat.length() >= 2:
                        self.velocitat[0] += x.velocitat[0]*0.4
                        self.velocitat[1] += x.velocitat[1]*0.4           
                    if diferencia_angle_x > 90 and x.velocitat.length() > 0:
                        x.posició = [x.posició_antiga[0], x.posició_antiga[1]]
                        nou_angle_velocitat_2 = 180 + 2*x.velocitat.angle_to((-1,0)) - 2*x.angle_rampa 
                        x.velocitat.rotate_ip(nou_angle_velocitat_2)
                        x.velocitat[0] *=0.3 + 0.59*math.sqrt(math.sin(math.radians(x.angle_rampa))**2)
                        x.velocitat[1] *=0.3 + 0.59*math.sqrt(math.cos(math.radians(x.angle_rampa))**2)
                    elif diferencia_angle_self > 90 and velocitat_inicial.length() >= 2 :
                        x.velocitat[0] += velocitat_inicial[0]*0.4
                        x.velocitat[1] += velocitat_inicial[1]*0.4
            
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
        self.estela_radi = 2
        self.estela_posició = [posició_inicial[0],posició_inicial[1]]
        self.estela_velocitat = [self.velocitat_sortida[0] , self.velocitat_sortida[1]]
        if self.tocat_objecte == False:    
            n=-1
            while True:
                if self.rectangle.collidepoint(self.estela_posició) or self.estela_posició[0] > pantalla_amplada:
                    break
                self.estela_posició[0] += self.estela_velocitat[0]*3
                self.estela_posició[1] += self.estela_velocitat[1]*3 + gravetat*6
                self.estela_velocitat[1] += 3*gravetat
                if n%2 ==0:    
                    pygame.draw.circle(pantalla, blanc, self.estela_posició, self.estela_radi)
                    self.estela_radi += 1
                    if self.estela_radi > 3:
                        self.estela_radi = 2
                n+=1
        else:
            while self.estela_posició[0] < self.posició_primer_xoc[0]:
                self.estela_posició[0] += self.estela_velocitat[0]*6
                self.estela_posició[1] += self.estela_velocitat[1]*6 + gravetat*21
                self.estela_velocitat[1] += 6*gravetat   
                pygame.draw.circle(pantalla, blanc, self.estela_posició, self.estela_radi)
                self.estela_radi += 1
                if self.estela_radi > 3:
                    self.estela_radi = 2
    def update(self):     
        self.posició_antiga = [self.posició[0], self.posició[1]]
        if self.linea_direció:
            self.calcul_linea_direció()    
        if self.llançat and self.tocat_objecte == False:
            self.estela()
        if self.aire:  
            if self.angle_rampa > 270:    
                self.velocitat[1] += gravetat*math.cos(math.radians(self.angle_rampa))
                self.velocitat[0] += gravetat*math.sin(math.radians(self.angle_rampa))
            elif self.angle_rampa > 180 and self.angle_rampa < 270:
                self.velocitat[1] -= gravetat*math.cos(math.radians(self.angle_rampa))
                self.velocitat[0] -= gravetat*math.sin(math.radians(self.angle_rampa))
            elif self.angle_rampa <= 180:
                self.velocitat[1] += gravetat
        if abs(self.velocitat[1]) < gravetat:
            self.velocitat[1] = 0
        if abs(self.velocitat[0]) < gravetat:
            self.velocitat[0] = 0
        self.posició[0] += self.velocitat[0]
        self.posició[1] += self.velocitat[1]
        if self.llançat and self.velocitat[0] == 0:
            if self.velocitat[1] == 0 or self.velocitat[1] == gravetat:    
                self.cooldown += 1
        else:
            self.cooldown = 0
        self.angle_rampa = 90
        if self.cooldown >= 500:     
            llista_objectes_pantalla.remove(self)
        self.colisionat = False
        self.rectangle.center = (self.posició[0], self.posició[1])

    def dibuixar(self):
        self.rectangle.center = (self.posició[0], self.posició[1])
        pantalla.blit(self.superficie_ocell, self.rectangle)

    def llançament(self):
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

    def reinici(self):
        self.aire = False
        self.velocitat *= 0
        self.llançat = False
        self.posició = [posició_inicial[0], posició_inicial[1]]
        self.zona = False
        self.cooldown = 0
        self.tocat_objecte = False
        self.linea_direció = False
        self.posició_primer_xoc = [0,0] 

# Ocells creats 
vermellet = ocells(20, vermell)
vermellet2 = ocells(20, vermell)
vermellet3 = ocells(20, vermell)
bombardero = ocells(25, negre)
bombardero2 = ocells(25, negre)
bombardero3 = ocells(25, negre)
pequeñin = ocells(15, cian)
pequeñin2 = ocells(15, cian)
pequeñin3 = ocells(15, cian)
racista = ocells(20, groc)
racista2 = ocells(20, groc)
racista3 = ocells(20, groc)
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

# Creació linea que indica direcció ocell
def linea(ocell):
    pos = pygame.mouse.get_pos()
    if distancia_ocell_ratoli() < (100+ocell.radi):
        pygame.draw.line(pantalla, blau, posició_inicial, pos, width = 8)
    else:
        angle = math.atan2(pos[0]-posició_inicial[0], pos[1]-posició_inicial[1])
        if angle > -0.1 or angle < -3:
            color = vermell
        else:
            color = verd
        distancia = distancia_ocell_ratoli() - 100 - ocell.radi
        pos = (pygame.mouse.get_pos()[0]-math.sin(angle)*distancia, pygame.mouse.get_pos()[1]-math.cos(angle)*distancia) 
        pygame.draw.line(pantalla, color, posició_inicial, pos, width = 8)
# Creació porcs
def porcs():
    porc_radi = 30
    porc_posició = (pantalla_amplada - porc_radi - 150, pantalla_alçada - porc_radi - 100)
    pygame.draw.circle(pantalla, verd, porc_posició, porc_radi) 

#Caixes 
class caixa():
    def __init__(self, posició, alçada, amplada, movible, angle):
        self.alçada = alçada
        self.amplada = amplada
        self.posició = posició
        self.posició_inicial = (posició[0], posició[1])
        self.velocitat = pygame.math.Vector2(0,0)
        self.movible = movible
        llista_objectes_rectangulars.append(self)
        self.superficie_rectangle = pygame.Surface((self.amplada, self.alçada))
        self.rectangle = self.superficie_rectangle.get_rect()
        self.rectangle.center = (self.posició[0] + 0.5*self.amplada, self.posició[1] + 0.5*self.alçada)
        self.superficie_rectangle.set_colorkey(fons)
        self.angle = angle
        self.angle_inicial = angle
        self.superficie_rectangle.fill(marró)
        if self.amplada < self.alçada:    
            pygame.draw.rect(self.superficie_rectangle, marró_fosc , ((0,0), (self.amplada, self.alçada)), 10 - (100//self.amplada))
        else:
            pygame.draw.rect(self.superficie_rectangle, marró_fosc , ((0,0), (self.amplada, self.alçada)), 10 - (100//self.alçada))
        self.angle_rampa = 90 
        self.colisionat = False
        self.rectangle.center = (self.posició[0] + 0.5*self.amplada, self.posició[1] + 0.5*self.alçada)
        self.rectangle_nou = pygame.transform.rotate(self.superficie_rectangle, self.angle)
        self.rectangle = self.rectangle_nou.get_rect()
        self.rectangle.center = (self.posició[0] + 0.5*self.amplada, self.posició[1] + 0.5*self.alçada)
        self.mask = pygame.mask.from_surface(self.rectangle_nou)
        self.velocitat_angle = 0
    
    def update(self):
        if self.movible == True:
            self.posició_antiga = [self.posició[0], self.posició[1]]
            self.angle += self.velocitat_angle
            if self.angle >= 360:
                self.angle = 0
            if self.angle_rampa > 270:    
                self.velocitat[1] += gravetat*math.cos(math.radians(self.angle_rampa))
                self.velocitat[0] += gravetat*math.sin(math.radians(self.angle_rampa))
            elif self.angle_rampa > 180 and self.angle_rampa < 270:
                self.velocitat[1] -= gravetat*math.cos(math.radians(self.angle_rampa))
                self.velocitat[0] -= gravetat*math.sin(math.radians(self.angle_rampa))
            elif self.angle_rampa <= 180:
                self.velocitat[1] += gravetat
            if abs(self.velocitat[1]) < gravetat:
                self.velocitat[1] = 0
            if abs(self.velocitat[0]) < gravetat:
                self.velocitat[0] = 0
            self.posició[0] += self.velocitat[0]
            self.posició[1] += self.velocitat[1]
            self.angle_rampa = 90
            self.rectangle.center = (self.posició[0] + 0.5*self.amplada, self.posició[1] + 0.5*self.alçada)
        self.colisionat = False
        
    def dibuixar(self):
        if self.velocitat_angle != 0:    
            self.rectangle_nou = pygame.transform.rotate(self.superficie_rectangle, self.angle)
            self.rectangle = self.rectangle_nou.get_rect()
            self.mask = pygame.mask.from_surface(self.rectangle_nou)
        self.rectangle.center = (self.posició[0] + 0.5*self.amplada, self.posició[1] + 0.5*self.alçada)
        pantalla.blit(self.rectangle_nou, self.rectangle)
    
    def calcul_angle_rampa(self, pos):
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
            z = 0
        if z >= 360:
            z -= 360
        if z >= 180:
            z = z-180
        else:
            z = z + 180  
        return z
    
    def colisió(self, x):
        fself = -1
        fx = -1
        for i in llista_objectes_pantalla:
            if i in llista_objectes_rectangulars:
                if i.movible:
                    if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)) and i != self:
                        fself +=1
                    if x.mask.overlap(i.mask,(i.rectangle.x- x.rectangle.x, i.rectangle.y- x.rectangle.y)) and i!= x:
                        fx +=1
        mask_xoc = self.mask.overlap_mask(x.mask,(x.rectangle.x- self.rectangle.x, x.rectangle.y- self.rectangle.y))
        rectangle_xoc = mask_xoc.get_bounding_rects()
        posició_xoc = [rectangle_xoc[0].center[0] + self.rectangle.x, rectangle_xoc[0].center[1] +self.rectangle.y]
        self.angle_rampa = x.calcul_angle_rampa(posició_xoc)
        if x.movible == False:
            self.posició = [self.posició_antiga[0], self.posició_antiga[1]]
            nou_angle_velocitat =180 + 2*self.velocitat.angle_to((-1,0)) - 2*self.angle_rampa
            self.velocitat.rotate_ip(nou_angle_velocitat)
            self.velocitat[0] *=0.3 + 0.59*abs(math.sin(math.radians(self.angle_rampa)))
            self.velocitat[1] *=0.3 + 0.59*abs(math.cos(math.radians(self.angle_rampa)))
        else:
            x.angle_rampa = self.calcul_angle_rampa(posició_xoc)
            velocitat_inicial = self.velocitat.copy()
            diferencia_angle_self = abs(self.velocitat.angle_to((-1,0)) - self.angle_rampa)
            if diferencia_angle_self > 180:
                diferencia_angle_self = 360 - diferencia_angle_self
            diferencia_angle_x = abs(x.velocitat.angle_to((-1,0)) - x.angle_rampa)
            if diferencia_angle_x > 180:
                diferencia_angle_x = 360 - diferencia_angle_x    
            if diferencia_angle_self > 90 and self.velocitat.length() > 0 :    
                self.posició = [self.posició_antiga[0], self.posició_antiga[1]]
                nou_angle_velocitat = 180+2*self.velocitat.angle_to((-1,0)) - 2*self.angle_rampa 
                self.velocitat.rotate_ip(nou_angle_velocitat)
                self.velocitat[0] *=0.3 + 0.59*abs(math.sin(math.radians(x.angle_rampa)))
                self.velocitat[1] *=0.3 + 0.59*abs(math.cos(math.radians(x.angle_rampa)))
            elif diferencia_angle_x >= 90 and x.velocitat.length() >= 2:
                self.velocitat[0] += x.velocitat[0]*0.4*(0.5**fself)
                self.velocitat[1] += x.velocitat[1]*0.4*(0.5**fself)            
            if diferencia_angle_x > 90 and x.velocitat.length() > 0:
                x.posició = [x.posició_antiga[0], x.posició_antiga[1]]
                nou_angle_velocitat_2 = 180 + 2*x.velocitat.angle_to((-1,0)) - 2*x.angle_rampa 
                x.velocitat.rotate_ip(nou_angle_velocitat_2)
                x.velocitat[0] *=0.3 + 0.59*abs(math.sin(math.radians(x.angle_rampa)))
                x.velocitat[1] *=0.3 + 0.59*abs(math.cos(math.radians(x.angle_rampa)))
            elif diferencia_angle_self >= 90 and velocitat_inicial.length() >= 2 :
                x.velocitat[0] += velocitat_inicial[0]*0.4*(0.5**fx)
                x.velocitat[1] += velocitat_inicial[1]*0.4*(0.5**fx)

    def reinici(self):
        self.posició = [self.posició_inicial[0], self.posició_inicial[1]]
        self.velocitat *= 0
        self.angle = self.angle_inicial
        self.rectangle.center = (self.posició[0] + 0.5*self.amplada, self.posició[1] + 0.5*self.alçada)
        self.angle_rampa = 90

paret_dreta = caixa((pantalla_amplada, -500), pantalla_alçada + 500, 100, False, 0)
paret_esquerra = caixa((-100, -500), pantalla_alçada + 500, 100, False, 0)
terra = caixa([0, pantalla_alçada], 100, pantalla_amplada, False, 0)
caixa2 = caixa([pantalla_amplada - 293, 300], 75, 75, True, 0)
caixa3 = caixa([pantalla_amplada - 143, 300], 75, 75, True, 0)
caixa4 = caixa([pantalla_amplada - 240, -50], 100, 20, True, 0)
caixa5 = caixa([pantalla_amplada - 140, -50], 100, 20, True, 0)
caixa6 = caixa([pantalla_amplada - 305, -100], 20, 250, True, 0)
caixa7 = caixa([pantalla_amplada - 230, -300], 100, 100, True, 0)
caixa1 = caixa([pantalla_amplada - 330, 200], 20, 300, True, 0)
paret_inclinada = caixa([pantalla_amplada-60, pantalla_alçada-120], 200, 20, False, 135)

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
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    dificultat = selecció_nivell()
                    if dificultat:
                        print("Dificultat seleccionada:", dificultat)
                        return True

        pantalla.fill(fons)

        font = pygame.font.Font(None, 300)
        text = font.render("Angry Birds", True, taronja)
        pantalla.blit(text, (pantalla_amplada // 2 - text.get_width() // 2, pantalla_alçada // 2 - text.get_height() // 2))

        pygame.display.flip()

#Definim reinici al sortir del nivell
def reinici():
    global llista_objectes_pantalla
    global sprites
    for i in sprites:
        i.reinici()
    llista_objectes_pantalla = []
    llista_objectes_pantalla.extend(llista_objectes_rectangulars)
    sprites = []
    sprites.extend(llista_objectes_rectangulars)
    llista_ocells_llançats = [no_ocell]
# Game GameLoop
def GameLoop():
    zona_ocell = False
    mantenint_ocell = False
    partida = False
    nivell = [bombardero, vermellet, racista2, vermellet2, pequeñin, racista]
    while True:
        if not partida:
            reinici()
            mantenint_ocell = False
            if not menú():
                break
            partida = True
        else:
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

            # Netejar la pantalla
            pantalla.fill(fons)
            # Aparèixer porcs, ocells i linea
            if mantenint_ocell:
                linea(ocell_actual)
            porcs()
            if ocell_anterior.llançat:    
                ocell_anterior.estela()
            for i in  llista_objectes_pantalla:
                i.update()
            llista_objectes_pantalla.sort(key=lambda i: i.rectangle.center[1])
            for self in llista_objectes_pantalla:
                if self in llista_ocells:
                    if self.llançat:    
                        for i in llista_objectes_pantalla:
                            if i in llista_objectes_rodons:    
                                if i.llançat and i.colisionat==False and i!= self: 
                                    if self.rectangle.colliderect(i.rectangle):
                                        if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):
                                            self.colisió(i)
                            else:    
                                if self.rectangle.colliderect(i.rectangle): 
                                    if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):    
                                        self.colisió(i)
                    self.colisionat = True
                if self in llista_objectes_rectangulars:
                    if self.movible:    
                        for i in llista_objectes_pantalla:
                            if i != self and i.colisionat == False and i in llista_objectes_rectangulars: 
                                if self.rectangle.colliderect(i.rectangle):
                                    if self.mask.overlap(i.mask,(i.rectangle.x- self.rectangle.x, i.rectangle.y- self.rectangle.y)):
                                        self.colisió(i)
                        self.colisionat = True
            for i in  llista_objectes_pantalla:
                i.dibuixar()
            linea_ocells(nivell[0], nivell[1], nivell[2], nivell[3], nivell[4], nivell[5],)
        # Recarregar la pantalla
        pygame.display.flip()
    # Sortir del joc
    pygame.quit()

# Córrer el joc
GameLoop()
