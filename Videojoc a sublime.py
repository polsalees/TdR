import pygame
import math

# Iniciar programa
pygame.init()

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
fons = (80, 80, 255)

# Definim la gravetat
gravetat = 0.05

# Preparar la pantalla
pantalla_amplada, pantalla_alçada = 1920, 1038
pantalla = pygame.display.set_mode((pantalla_amplada, pantalla_alçada))
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
class ocells(pygame.sprite.Sprite):
    def __init__(self, radi, color):
        global gravetat
        pygame.sprite.Sprite.__init__(self)
        self.radi = radi
        self.posició = [posició_inicial[0], posició_inicial[1]]
        self.velocitat = [0,0]
        self.potencia = 0
        self.angle = 0
        self.angle_cercle = 0
        self.aire = False
        self.color = color
        self.zona = False
        self.frenada = False
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
    
    def calcul_posició_primer_xoc (self):
        if self.tocat_objecte == False:
            self.posició_primer_xoc[0] += self.posició[0]
            self.posició_primer_xoc[1] += self.posició[1]
            self.tocat_objecte = True
    
    def calcul_angle_cercle(self, x, y):
        s = 0 
        if (self.posició[0]-x) != 0:    
            s = -1*math.degrees(math.atan((self.posició[1]-y)/ (self.posició[0]-x)))
        if s == 0:
            if (self.posició[1]-y) and self.posició[0] - x > 0:
                s -=180
            if (self.posició[0]-x) == 0:
                s +=90
        if s <= 0:
            s +=180
        if self.posició[1]-y > 0:
            s +=180
        return s

    def calcul_angle_velocitat(self):
        if self.velocitat[0] != 0:
            x = -1*math.degrees(math.atan(self.velocitat[1]/self.velocitat[0]))
        else:
            if self.velocitat[1] != 0:
                x = 90
            else:
                x = 0
        if x == 0:
            if self.velocitat[0] >= 0:
                x -=180
        if x <= 0:
            x +=180
        if self.velocitat[1] > 0:
            x +=180
        return x
    
    def calcul_xoc(self, puntx, punty, coordenada, x):   
        if math.sqrt((self.posició[0] - puntx) **2 + (self.posició[1] - punty) ** 2) <= self.radi:
            self.angle_velocitat = self.calcul_angle_velocitat()
            self.angle_cercle = self.calcul_angle_cercle(puntx, punty)
            if (self.angle_velocitat // 90) != (self.angle_cercle // 90) and self.magnitud_velocitat > 0:   
                while math.sqrt((self.posició[0] - puntx) **2 + (self.posició[1] - punty) ** 2) <= self.radi and self.magnitud_velocitat > 0:    
                    self.posició[0] += self.magnitud_velocitat * math.cos(math.radians(self.angle_cercle)) * 0.1
                    self.posició[1] += -self.magnitud_velocitat * math.sin(math.radians(self.angle_cercle)) * 0.1
                if self.angle_cercle <= 180:
                    nou_angle_velocitat = 180 -self.angle_velocitat + 2*self.angle_cercle
                else:    
                    nou_angle_velocitat = -180 - self.angle_velocitat + 2*self.angle_cercle
                if coordenada == "x":    
                    self.velocitat[0] = self.magnitud_velocitat * math.cos(math.radians(nou_angle_velocitat)) 
                    self.velocitat[1] = -self.magnitud_velocitat * math.sin(math.radians(nou_angle_velocitat))*0.4
                elif coordenada == "y":
                    self.velocitat[0] = self.magnitud_velocitat * math.cos(math.radians(nou_angle_velocitat)) * 0.4
                    self.velocitat[1] = -self.magnitud_velocitat * math.sin(math.radians(nou_angle_velocitat)) 
            elif x.magnitud_velocitat > 1:
                self.velocitat[0] += x.velocitat[0]*0.4 
                self.velocitat[1] += x.velocitat[1]*0.4
            if x.movible == True:
                angle_direcció_rectangle = self.angle_cercle + 180
                if math.sqrt(x.magnitud_velocitat**2) <= gravetat:
                    x.magnitud_velocitat = 0
                if angle_direcció_rectangle >= 360:
                    angle_direcció_rectangle -= 360
                if x.velocitat[0] != 0:
                    angle_velocitat = -1*math.degrees(math.atan(x.velocitat[1]/x.velocitat[0]))
                else:
                    if x.velocitat[1] != 0:
                        angle_velocitat = 90
                    else:
                        angle_velocitat = 0
                if angle_velocitat == 0:
                    if x.velocitat[0] >= 0:
                        angle_velocitat -=180
                if angle_velocitat <= 0:
                    angle_velocitat +=180
                if x.velocitat[1] > 0:
                    angle_velocitat +=180
                if (angle_velocitat // 90) != (angle_direcció_rectangle // 90) and x.magnitud_velocitat > 0:    
                    while math.sqrt((self.posició[0] - puntx) **2 + (self.posició[1] - punty) ** 2) <= self.radi and x.magnitud_velocitat > 0:    
                        puntx += x.magnitud_velocitat * math.cos(math.radians(angle_direcció_rectangle)) * 0.1
                        punty += -x.magnitud_velocitat * math.sin(math.radians(angle_direcció_rectangle)) * 0.1
                        x.posició[0] += x.magnitud_velocitat * math.cos(math.radians(angle_direcció_rectangle)) * 0.1
                        x.posició[1] += -x.magnitud_velocitat * math.sin(math.radians(angle_direcció_rectangle)) * 0.1
                    if angle_direcció_rectangle <= 180:
                        nou_angle_velocitat_rectangle = 180 -angle_velocitat + 2*angle_direcció_rectangle
                    else:    
                        nou_angle_velocitat_rectangle = -180 - angle_velocitat + 2*angle_direcció_rectangle
                    if coordenada == "x":    
                        x.velocitat[0] = x.magnitud_velocitat * math.cos(math.radians(nou_angle_velocitat_rectangle)) 
                        x.velocitat[1] = -x.magnitud_velocitat * math.sin(math.radians(nou_angle_velocitat_rectangle))*0.4
                    elif coordenada == "y":
                        x.velocitat[0] = x.magnitud_velocitat * math.cos(math.radians(nou_angle_velocitat_rectangle))*0.4
                        x.velocitat[1] = -x.magnitud_velocitat * math.sin(math.radians(nou_angle_velocitat_rectangle))
                elif self.magnitud_velocitat > 1:
                    if coordenada == "x":    
                        x.velocitat[0] += -self.velocitat[0]*0.6*0.4
                        x.velocitat[1] += -self.velocitat[1]*0.6
                    if coordenada == "y":    
                        x.velocitat[0] += -self.velocitat[0]*0.6 
                        x.velocitat[1] += -self.velocitat[1]*0.6*0.4
    def colisió(self,x):
        if x in llista_objectes_rodons:    
            if (self.radi + x.radi) > math.sqrt(((self.posició[0] - x.posició[0]) **2 + (self.posició[1] - x.posició[1]) ** 2)):
                self.calcul_posició_primer_xoc()
                nou_angle_velocitat = 0
                if x in llista_ocells:     
                    x.calcul_posició_primer_xoc()
                self.angle_cercle = self.calcul_angle_cercle(x.posició[0], x.posició[1])
                self.angle_velocitat = self.calcul_angle_velocitat()
                self.magnitud_velocitat = math.sqrt(((self.velocitat[0]) **2 + (self.velocitat[1]) ** 2))
                x.magnitud_velocitat = math.sqrt(((x.velocitat[0]) **2 + (x.velocitat[1]) ** 2))
                x.angle_velocitat = x.calcul_angle_velocitat()
                x.angle_cercle = self.angle_cercle + 180
                if x.angle_cercle >= 360:
                    x.angle_cercle -= 360
                if self.magnitud_velocitat != 0 and x.magnitud_velocitat != 0 and self.angle != 180:
                    if self.angle_velocitat // 90 != self.angle_cercle//90:
                        if x.angle_velocitat // 90 != x.angle_cercle//90:
                            while (self.radi + x.radi) >= math.sqrt(((self.posició[0] - x.posició[0]) **2 + (self.posició[1] - x.posició[1]) ** 2)):
                                x.posició[0] += x.magnitud_velocitat * math.cos(math.radians(x.angle_cercle)) * 0.1
                                x.posició[1] += -x.magnitud_velocitat * math.sin(math.radians(x.angle_cercle)) * 0.1
                                self.posició[0] += self.magnitud_velocitat * math.cos(math.radians(self.angle_cercle)) * 0.1
                                self.posició[1] += -self.magnitud_velocitat * math.sin(math.radians(self.angle_cercle)) * 0.1
                        else:
                            while (self.radi + x.radi) >= math.sqrt(((self.posició[0] - x.posició[0]) **2 + (self.posició[1] - x.posició[1]) ** 2)):
                                self.posició[0] += self.magnitud_velocitat * math.cos(math.radians(self.angle_cercle)) * 0.1
                                self.posició[1] += -self.magnitud_velocitat * math.sin(math.radians(self.angle_cercle)) * 0.1
                    else:
                         while (self.radi + x.radi) >= math.sqrt(((self.posició[0] - x.posició[0]) **2 + (self.posició[1] - x.posició[1]) ** 2)):
                            x.posició[0] += x.magnitud_velocitat * math.cos(math.radians(x.angle_cercle)) * 0.1
                            x.posició[1] += -x.magnitud_velocitat * math.sin(math.radians(x.angle_cercle)) * 0.1
                if self.magnitud_velocitat == 0 and x.magnitud_velocitat !=0:
                    while (self.radi + x.radi) >= math.sqrt(((self.posició[0] - x.posició[0]) **2 + (self.posició[1] - x.posició[1]) ** 2)):
                            x.posició[0] += x.magnitud_velocitat * math.cos(math.radians(x.angle_cercle)) * 0.1
                            x.posició[1] += -x.magnitud_velocitat * math.sin(math.radians(x.angle_cercle)) * 0.1
                if x.magnitud_velocitat == 0 and self.magnitud_velocitat != 0:
                    while (self.radi + x.radi) >= math.sqrt(((self.posició[0] - x.posició[0]) **2 + (self.posició[1] - x.posició[1]) ** 2)):
                            self.posició[0] += self.magnitud_velocitat * math.cos(math.radians(self.angle_cercle)) * 0.1
                            self.posició[1] += -self.magnitud_velocitat * math.sin(math.radians(self.angle_cercle)) * 0.1
                if (self.angle_velocitat // 90) != (self.angle_cercle // 90) or self.magnitud_velocitat==0:    
                    if self.angle_cercle <= 180:
                        nou_angle_velocitat = 180 - self.angle_velocitat + 2*self.angle_cercle
                    if self.angle_cercle > 180:
                        nou_angle_velocitat = -180 - self.angle_velocitat + 2*self.angle_cercle  
                    self.velocitat[0] = self.magnitud_velocitat * math.cos(math.radians(nou_angle_velocitat)) *0.4
                    self.velocitat[1] = -self.magnitud_velocitat * math.sin(math.radians(nou_angle_velocitat)) *0.4
                else:
                    self.velocitat[0] += x.velocitat[0]*0.4 
                    self.velocitat[1] += x.velocitat[1]*0.4
                if (x.angle_velocitat // 90) != (x.angle_cercle // 90) or x.magnitud_velocitat==0:        
                    if x.angle_cercle <= 180:
                        nou_angle_velocitat_2 = 180 - x.angle_velocitat + 2*x.angle_cercle
                    if x.angle_cercle > 180:
                        nou_angle_velocitat_2 = -180 - x.angle_velocitat + 2*x.angle_cercle   
                    x.velocitat[0] = x.magnitud_velocitat * math.cos(math.radians(nou_angle_velocitat_2)) *0.4
                    x.velocitat[1] = -x.magnitud_velocitat * math.sin(math.radians(nou_angle_velocitat_2)) *0.4 
                else:
                    x.velocitat[0] += -self.velocitat[0]
                    x.velocitat[1] += -self.velocitat[1]
        if x in llista_objectes_rectangulars:
            if self.posició[0] > (x.posició[0]-self.radi) and self.posició[0] < (x.posició[0] + x.amplada + self.radi) and self.posició[1] > (x.posició[1]-self.radi) and self.posició[1] < (x.posició[1] + x.alçada + self.radi):
                self.calcul_posició_primer_xoc()
                x.magnitud_velocitat = math.sqrt(x.velocitat[0]**2 + x.velocitat[1]**2)
                self.magnitud_velocitat = math.sqrt(self.velocitat[0]**2 + self.velocitat[1]**2)    
                if self.magnitud_velocitat > 8 and x.movible:
                    llista_objectes_pantalla.remove(x)
                    self.velocitat = [self.velocitat[0]*0.4, self.velocitat[1]*0.4] 
                else:
                    if x.magnitud_velocitat > 8 and x.movible:
                        llista_objectes_pantalla.remove(x)
                    if (self.posició[0] - x.posició[0]) < 0:     
                        if self.posició[1] > (x.posició[1] + x.alçada):
                            self.calcul_xoc(x.posició[0], x.posició[1] + x.alçada, "x", x)
                        elif self.posició[1] < x.posició[1]:
                            self.calcul_xoc(x.posició[0], x.posició[1], "x", x)
                        else:    
                            if self.velocitat[0] > 0:
                                self.posició[0] = x.posició[0]-self.radi                                  
                                self.velocitat[0] *= -0.4
                            elif x.magnitud_velocitat > 1:
                                self.velocitat[0] += x.velocitat[0]*0.4
                            if x.movible == True: 
                                if x.velocitat[0] < 0:
                                    x.posició[0] = self.posició[0]+self.radi
                                    x.velocitat[0] *= -0.4
                                elif self.magnitud_velocitat > 1:
                                    x.velocitat[0] += -self.velocitat[0]*0.6
                    if (self.posició[0] - (x.posició[0] + x.amplada)) > 0:   
                        if self.posició[1] > (x.posició[1] + x.alçada):
                            self.calcul_xoc(x.posició[0] + x.amplada, x.posició[1] + x.alçada, "x", x)
                        elif self.posició[1] < x.posició[1]:
                            self.calcul_xoc(x.posició[0] + x.amplada, x.posició[1], "x", x)
                        else:    
                            if self.velocitat[0] < 0:
                                self.posició[0] = x.posició[0] + x.amplada+self.radi     
                                self.velocitat[0] *= -0.4
                            elif x.magnitud_velocitat > 1:
                                self.velocitat[0] += x.velocitat[0]*0.4
                            if x.movible == True :
                                if x.velocitat[0] > 0:    
                                    x.posició[0] = self.posició[0] - x.amplada-self.radi
                                    x.velocitat[0] *= -0.4
                                elif self.magnitud_velocitat > 1:
                                    x.velocitat[0] += -self.velocitat[0]*0.6
                    if (self.posició[1] - x.posició[1]) < 0:     
                        if self.posició[0] > (x.posició[0] + x.amplada):
                            self.calcul_xoc(x.posició[0] + x.amplada, x.posició[1], "y", x)
                        elif self.posició[0] < x.posició[0]:
                            self.calcul_xoc(x.posició[0], x.posició[1], "y", x)
                        else:    
                            if self.velocitat[1] > 0:      
                                self.posició[1] = x.posició[1] -self.radi
                                self.velocitat[1] *= -0.4
                            elif x.magnitud_velocitat > 1:
                                self.velocitat[1] += x.velocitat[1]*0.4
                            if x.movible == True:
                                if x.velocitat[1] < 0:     
                                    x.posició[1] = self.posició[1] + self.radi
                                    x.velocitat[1] *= -0.4
                                elif self.magnitud_velocitat > 1:
                                    x.velocitat[1] += -self.velocitat[1]*0.6
                    if (self.posició[1] - (x.posició[1]+x.alçada)) > 0:     
                        if self.posició[0] > (x.posició[0] + x.amplada):
                            self.calcul_xoc(x.posició[0] + x.amplada, x.posició[1] + x.alçada, "y", x)
                        elif self.posició[0] < x.posició[0]:
                            self.calcul_xoc(x.posició[0], x.posició[1] + x.alçada, "y", x)
                        else:    
                            if self.velocitat[1] < 0:    
                                self.posició[1] = x.posició[1] + x.alçada + self.radi
                                self.velocitat[1] *= -0.4
                            elif x.magnitud_velocitat > 1:
                                self.velocitat[1] += x.velocitat[1]*0.4
                            if x.movible == True:
                                if x.velocitat[1] > 0:     
                                    x.posició[1] = self.posició[1] - x.alçada - self.radi
                                    x.velocitat[1] *= -0.4
                                elif self.magnitud_velocitat > 1:
                                    x.velocitat[1] += -self.velocitat[1]*0.6
                             
    
    def calcul_linea_direció(self):
        n = 0 
        self.linea_direció_radi = 5
        self.linea_direció_posició = [posició_inicial[0], posició_inicial[1]]
        self.linea_direció_tocat_objecte = False
        self.potencia = distancia_ocell_ratoli() - self.radi
        self.angle = math.radians(calcular_angle())
        if self.potencia >= 100:
            self.potencia = 100
        if self.potencia <= 0 or self.angle > -0.1 or self.angle < -3:
            self.potencia = 0
        self.linea_direció_velocitat[0] = -math.sin(self.angle) * self.potencia * 0.1
        self.linea_direció_velocitat[1] = -math.cos(self.angle) * self.potencia * 0.1
        self.linea_direció_velocitat[1]  += gravetat * 0.2 *(self.linea_direció_moviment%30)
        self.linea_direció_posició[0] += self.linea_direció_velocitat[0] * 0.2 *(self.linea_direció_moviment%30)
        self.linea_direció_posició[1] += self.linea_direció_velocitat[1] * 0.2 *(self.linea_direció_moviment%30)
        pygame.draw.circle(pantalla, blanc, self.linea_direció_posició, self.linea_direció_radi)
        if self.potencia !=0:    
            while not self.linea_direció_tocat_objecte and not self.linea_direció_radi <=1:
                n -= 1       
                self.linea_direció_radi -= 0.15
                self.linea_direció_velocitat[1]  += gravetat * 3
                self.linea_direció_posició[0] += self.linea_direció_velocitat[0] * 3
                self.linea_direció_posició[1] += self.linea_direció_velocitat[1] * 3
                for i in llista_objectes_pantalla:
                    if i != self:
                        if i in llista_objectes_rodons:    
                            if (i.radi + self.linea_direció_radi) > math.sqrt(((i.posició[0] - self.linea_direció_posició[0]) **2 + (i.posició[1] - self.linea_direció_posició[1]) ** 2)):
                                self.linea_direció_tocat_objecte = True 
                        if i in llista_objectes_rectangulars:
                            if self.linea_direció_posició[0] > (i.posició[0]-self.linea_direció_radi) and self.linea_direció_posició[0] < (i.posició[0] + i.amplada + self.linea_direció_radi) and self.linea_direció_posició[1] > (i.posició[1]-self.linea_direció_radi) and self.linea_direció_posició[1] < (i.posició[1] + i.alçada + self.linea_direció_radi):
                                    self.linea_direció_tocat_objecte = True
                if n % 2  == 0 and self.linea_direció_tocat_objecte == False:
                    pygame.draw.circle(pantalla, blanc, self.linea_direció_posició, self.linea_direció_radi)
            self.linea_direció_moviment +=0.5
    
    def estela(self): 
        n = 0
        self.estela_radi = 2
        self.estela_posició = [posició_inicial[0],posició_inicial[1]]
        self.estela_tocat_ocell = False
        self.estela_velocitat[0] = -math.sin(self.angle) * self.potencia * 0.1
        self.estela_velocitat[1] = -math.cos(self.angle) * self.potencia * 0.1   
        if self.tocat_objecte == False:    
            while self.estela_tocat_ocell == False :
                n += 1  
                self.estela_velocitat[1]  += gravetat
                self.estela_posició[0] += self.estela_velocitat[0]
                self.estela_posició[1] += self.estela_velocitat[1]
                if (self.radi + 2) > math.sqrt(((self.posició[0] - self.estela_posició[0]) **2 + (self.posició[1] - self.estela_posició[1]) ** 2)):
                    self.estela_tocat_ocell = True 
                if (n % 5) == 0:     
                    pygame.draw.circle(pantalla, blanc, self.estela_posició, self.estela_radi)
                    self.estela_radi += 1
                    if self.estela_radi > 3:
                        self.estela_radi = 2
        else:
            while self.estela_posició[0] < self.posició_primer_xoc[0]:
                n += 1  
                self.estela_velocitat[1]  += gravetat
                self.estela_posició[0] += self.estela_velocitat[0]
                self.estela_posició[1] += self.estela_velocitat[1]
                if (n % 5) == 0:     
                    pygame.draw.circle(pantalla, blanc, self.estela_posició, self.estela_radi)
                    self.estela_radi += 1
                    if self.estela_radi > 3:
                        self.estela_radi = 2
    def update(self):     
        if self.linea_direció:
            self.calcul_linea_direció()    
        if self.llançat and self.tocat_objecte == False:
            self.estela()
        if self.posició[1] < (pantalla_alçada-self.radi) and self.llançat or self.velocitat[1] < 0:
            self.aire = True
        if self.aire:  
            if self.angle_cercle >= 0 and self.angle_cercle < 90:    
                self.velocitat[1] += gravetat*math.cos(math.radians(self.angle_cercle))
                self.velocitat[0] += gravetat*math.sin(math.radians(self.angle_cercle))
            elif self.angle_cercle > 90 and self.angle_cercle < 180:
                self.velocitat[1] -= gravetat*math.cos(math.radians(self.angle_cercle))
                self.velocitat[0] -= gravetat*math.sin(math.radians(self.angle_cercle))
            elif self.angle_cercle >= 180:
                self.velocitat[1] += gravetat
        if self.velocitat[1] < gravetat and self.velocitat[1] > 0 and self.tocat_objecte:
            self.velocitat[1] = 0
        if self.velocitat[1] > gravetat and self.velocitat[1] < 0 and self.tocat_objecte:
            self.velocitat[1] = 0
        self.posició[0] += self.velocitat[0]
        self.posició[1] += self.velocitat[1]
        if self.velocitat[1] == 0 and self.velocitat[0] != 0:
            self.frenada = True
        else:
            self.frenada = False
        if self.frenada:
            if self.velocitat[0] > 0:
                self.velocitat[0] -= 0.01
                if self.velocitat[0] <= 0.01:
                    self.velocitat[0] = 0
                    self.frenada = False
            elif self.velocitat[0] < 0:
                self.velocitat[0] += 0.01
                if self.velocitat[0] >= -0.01:
                    self.velocitat[0] = 0
                    self.frenada = False
        if self.llançat and self.velocitat[0] == 0:
            if self.velocitat[1] == 0 or self.velocitat[1] == gravetat:    
                self.cooldown += 1
        else:
            self.cooldown = 0
        self.angle_cercle = 0
        if self.cooldown >= 500:     
            llista_objectes_pantalla.remove(self)

    def dibuixar(self):
        pygame.draw.circle(pantalla, self.color, self.posició, self.radi)

    def llançament(self):
        self.potencia = distancia_ocell_ratoli() - self.radi
        self.angle = math.radians(calcular_angle())
        if self.potencia >= 100:
            self.potencia = 100
        if self.potencia <= 0 or self.angle > -0.1 or self.angle < -3:
            self.potencia = 0
        self.velocitat[0] = -math.sin(self.angle) * self.potencia * 0.1
        self.velocitat[1] = -math.cos(self.angle) * self.potencia * 0.1
        if self.potencia != 0:
            self.llançat = True
    
    def zona_llançament(self):
        self.distancia = distancia_ocell_ratoli() - self.radi
        if self.distancia <= 0:
            self.zona = True
        if self.distancia >= 0:
            self.zona = False
        return self.zona

    def reinici(self):
        self.aire = False
        self.velocitat = [0,0]
        self.frenada = False
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
    if ocell1.llançat == False:
        if llista_objectes_pantalla.count(ocell1) < 1:
            llista_objectes_pantalla.append(ocell1)
            sprites.append(ocell1)
            llista_ocells_llançats.append(ocell1)
        x = llista_ocells_llançats.index(ocell1)
    if ocell1.llançat: 
        if ocell1.tocat_objecte == False:
            x = llista_ocells_llançats.index(no_ocell)
        if ocell1.tocat_objecte:
            if ocell2.llançat == False:
                if llista_objectes_pantalla.count(ocell2) < 1:
                    llista_objectes_pantalla.append(ocell2)
                    sprites.append(ocell2)
                    llista_ocells_llançats.append(ocell2)
                x = llista_ocells_llançats.index(ocell2)
            if ocell2.llançat:
                if ocell2.tocat_objecte == False:
                    x = llista_ocells_llançats.index(no_ocell)
                if ocell2.tocat_objecte:
                    if ocell3.llançat == False:
                        if llista_objectes_pantalla.count(ocell3) < 1:
                            llista_objectes_pantalla.append(ocell3)
                            sprites.append(ocell3)
                            llista_ocells_llançats.append(ocell3)
                        x = llista_ocells_llançats.index(ocell3)
                    if ocell3.llançat:
                        if ocell3.tocat_objecte == False:
                            x = llista_ocells_llançats.index(no_ocell)
                        if ocell3.tocat_objecte:
                            if ocell4.llançat == False:
                                if llista_objectes_pantalla.count(ocell4) < 1:
                                     llista_objectes_pantalla.append(ocell4)
                                     sprites.append(ocell4)
                                     llista_ocells_llançats.append(ocell4)
                                x = llista_ocells_llançats.index(ocell4)
                            if ocell4.llançat:
                                if ocell4.tocat_objecte == False:
                                    x = llista_ocells_llançats.index(no_ocell)
                                if ocell4.tocat_objecte:
                                    if ocell5.llançat == False:
                                        if llista_objectes_pantalla.count(ocell5) < 1:
                                            llista_objectes_pantalla.append(ocell5)
                                            sprites.append(ocell5)
                                            llista_ocells_llançats.append(ocell5)
                                        x = llista_ocells_llançats.index(ocell5) 
                                    if ocell5.llançat:
                                        if ocell5.tocat_objecte == False:
                                            x = llista_ocells_llançats.index(no_ocell)
                                        if ocell5.tocat_objecte:
                                            if ocell6.llançat == False:
                                                if llista_objectes_pantalla.count(ocell6) < 1:
                                                    llista_objectes_pantalla.append(ocell6)
                                                    sprites.append(ocell6)
                                                    llista_ocells_llançats.append(ocell6)
                                                x = llista_ocells_llançats.index(ocell6)
                                            if ocell6.llançat:
                                                x = llista_ocells_llançats.index(no_ocell)
    return x

# Creació linea ocells
def linea_ocells(ocell1, ocell2, ocell3, ocell4, ocell5, ocell6):
    if ocell1.llançat == False or ocell1.tocat_objecte == False:
        pygame.draw.circle(pantalla, ocell2.color, (180, pantalla_alçada - ocell2.radi), ocell2.radi)
        pygame.draw.circle(pantalla, ocell3.color, (130, pantalla_alçada - ocell3.radi), ocell3.radi)
        pygame.draw.circle(pantalla, ocell4.color, (80, pantalla_alçada - ocell4.radi), ocell4.radi)
        pygame.draw.circle(pantalla, ocell5.color, (30, pantalla_alçada - ocell5.radi), ocell5.radi)
        pygame.draw.circle(pantalla, ocell6.color, (-20, pantalla_alçada - ocell6.radi), ocell6.radi) 
    else:
        if ocell2.llançat == False or ocell2.tocat_objecte == False:
            pygame.draw.circle(pantalla, ocell3.color, (180, pantalla_alçada - ocell3.radi), ocell3.radi)
            pygame.draw.circle(pantalla, ocell4.color, (130, pantalla_alçada - ocell4.radi), ocell4.radi)
            pygame.draw.circle(pantalla, ocell5.color, (80, pantalla_alçada - ocell5.radi), ocell5.radi)
            pygame.draw.circle(pantalla, ocell6.color, (30, pantalla_alçada - ocell6.radi), ocell6.radi)
        else:
            if ocell3.llançat == False or ocell3.tocat_objecte == False:
                pygame.draw.circle(pantalla, ocell4.color, (180, pantalla_alçada - ocell4.radi), ocell4.radi)
                pygame.draw.circle(pantalla, ocell5.color, (130, pantalla_alçada - ocell5.radi), ocell5.radi)
                pygame.draw.circle(pantalla, ocell6.color, (80, pantalla_alçada - ocell6.radi), ocell6.radi)
            else:
                if ocell4.llançat == False or ocell4.tocat_objecte == False:
                    pygame.draw.circle(pantalla, ocell5.color, (180, pantalla_alçada - ocell5.radi), ocell5.radi)
                    pygame.draw.circle(pantalla, ocell6.color, (130, pantalla_alçada - ocell6.radi), ocell6.radi)
                else:
                    if ocell5.llançat == False or ocell5.tocat_objecte == False:
                        pygame.draw.circle(pantalla, ocell6.color, (180, pantalla_alçada - ocell6.radi), ocell6.radi)

# Creació linea que indica direcció ocell
class linea(pygame.sprite.Sprite):
    def __init__(self, x):
        self.costat = 200 + 2*x.radi
        self.superficie_rectangle = pygame.Surface((self.costat, self.costat))
        self.superficie_rectangle.set_colorkey(fons)
        self.superficie = self.superficie_rectangle.copy()
        self.superficie.set_colorkey(fons)
        self.rect = self.superficie.get_rect()
        self.rect.center = (posició_inicial[0], posició_inicial[1])
    def update(self):
        self.superficie_rectangle.fill(fons)
        self.amplada = distancia_ocell_ratoli() 
        pygame.draw.rect(self.superficie_rectangle, blau, pygame.Rect(self.costat/2 - 2.5, self.costat/2 - self.amplada, 5, 1000))
        pygame.draw.rect(self.superficie_rectangle, fons, pygame.Rect(self.costat/2 - 2.5, self.costat/2, 5, 1000))
        self.angle = calcular_angle() + 180 
        self.rectangle_nou = pygame.transform.rotate(self.superficie_rectangle, self.angle)
        self.rect = self.rectangle_nou.get_rect()
        self.rect.center = (posició_inicial[0], posició_inicial[1])
        pantalla.blit(self.rectangle_nou, self.rect)

# Creació porcs
def porcs():
    porc_radi = 30
    porc_posició = (pantalla_amplada - porc_radi - 150, pantalla_alçada - porc_radi - 100)
    pygame.draw.circle(pantalla, verd, porc_posició, porc_radi) 

#Caixes 
class caixa(pygame.sprite.Sprite):
    def __init__(self, posició_x, posició_y, alçada, amplada, movible):
        pygame.sprite.Sprite.__init__(self)
        self.alçada = alçada
        self.amplada = amplada
        self.posició = [posició_x, posició_y]
        self.posició_inicial = [posició_x, posició_y]
        self.velocitat = [0,0]
        self.movible = movible
        llista_objectes_rectangulars.append(self)
        self.frenada = False
    
    def update(self):
        if self.movible == True:
            self.velocitat[1] += gravetat
            if self.velocitat[1] < gravetat and self.velocitat[1] > 0:
                        self.velocitat[1] = 0
            if self.velocitat[1] > -gravetat and self.velocitat[1] < 0:
                        self.velocitat[1] = 0
            if self.velocitat[1] == 0 and self.velocitat[0] != 0:
                self.frenada = True
            else:
                self.frenada = False 
            if self.frenada:
                if self.velocitat[0] > 0:
                    self.velocitat[0] -= 0.005
                    if self.velocitat[0] <= 0.005:
                        self.velocitat[0] = 0
                        self.frenada = False
                elif self.velocitat[0] < 0:
                    self.velocitat[0] += 0.005
                    if self.velocitat[0] >= -0.005:
                        self.velocitat[0] = 0
                        self.frenada = False
            self.posició[0] += self.velocitat[0]
            self.posició[1] += self.velocitat[1]
        
    def dibuixar(self):
        pygame.draw.rect(pantalla, marró , (self.posició, (self.amplada, self.alçada)))

    def dintre(self, puntX, puntY):
        if puntX >= self.posició[0] and puntX <= (self.posició[0] + self.amplada) and puntY >= self.posició[1] and puntY <= (self.posició[1] + self.alçada):
            return True
        else:
            return False

    def colisió(self, x):
        if x in llista_objectes_rectangulars:
            if (x.dintre(self.posició[0] +self.amplada, self.posició[1]) == True or x.dintre(self.posició[0] + self.amplada, self.posició[1] + self.alçada) == True or x.dintre(self.posició[0], self.posició[1]) == True or x.dintre(self.posició[0], self.posició[1] + self.alçada) == True) and (x.movible or self.movible):
                x.magnitud_velocitat = math.sqrt(x.velocitat[0]**2 + x.velocitat[1]**2)
                self.magnitud_velocitat = math.sqrt(self.velocitat[0]**2 + self.velocitat[1]**2)
                if x.movible == False:
                    if (self.posició[0] - x.posició[0]) < 0 and not self.velocitat[0] <= 0:     
                        self.posició[0] = x.posició[0]-self.amplada
                        self.velocitat[0] *= -0.4
                    if ((self.posició[0] + self.amplada) - (x.posició[0] + x.amplada)) > 0  and not self.velocitat[0] >= 0:      
                        self.posició[0] = x.posició[0] + x.amplada
                        self.velocitat[0] *= -0.4
                    if (self.posició[1] - x.posició[1]) < 0 and not self.velocitat[1] <= 0:        
                        self.posició[1] = x.posició[1] - self.alçada
                        self.velocitat[1] *= -0.4
                    if ((self.posició[1] + self.alçada) - (x.posició[1]+x.alçada)) > 0 and not self.velocitat[1] >= 0:     
                        self.posició[1] = x.posició[1] + x.alçada
                        self.velocitat[1] *= -0.4
                
                elif self.movible == False:
                    if (x.posició[0] - self.posició[0]) < 0 and not x.velocitat[0] <= 0:     
                        x.posició[0] = self.posició[0]-x.amplada
                        x.velocitat[0] *= -0.4
                    if ((x.posició[0] + x.amplada) - (self.posició[0] + self.amplada)) > 0  and not x.velocitat[0] >= 0:      
                        x.posició[0] = self.posició[0] + self.amplada
                        x.velocitat[0] *= -0.4
                    if (x.posició[1] - self.posició[1]) < 0 and not x.velocitat[1] <= 0:        
                        x.posició[1] = self.posició[1] - x.alçada
                        x.velocitat[1] *= -0.4
                    if ((x.posició[1] + x.alçada) - (self.posició[1]+self.alçada)) > 0 and not x.velocitat[1] >= 0:     
                        x.posició[1] = self.posició[1] + self.alçada
                        x.velocitat[1] *= -0.4

                else:
                    if x.dintre(self.posició[0] + self.amplada, self.posició[1]) == True:
                        valor = ((self.posició[0] + self.amplada) - x.posició[0])
                        if valor <= (x.posició[1] + x.alçada - self.posició[1]):
                            if self.velocitat[0] > 0 and x.velocitat[0] < 0:    
                                self.posició[0] = x.posició[0]-self.amplada
                                self.velocitat[0] *= -0.4
                                x.velocitat[0] *= -0.4
                            elif self.velocitat[0] <= 0 and x.velocitat[0] < 0:    
                                x.posició[0] = self.posició[0] + self.amplada
                                x.velocitat[0] *= -0.4
                                if x.magnitud_velocitat > 0.5:    
                                    self.velocitat[0] += -x.velocitat[0]
                            elif self.velocitat[0] > 0 and x.velocitat[0] >= 0:
                                self.posició[0] = x.posició[0]-self.amplada
                                self.velocitat[0] *= -0.4
                                if self.magnitud_velocitat > 0.5:    
                                    x.velocitat[0] += -self.velocitat[0]
                        if valor >= (x.posició[1] + x.alçada - self.posició[1]):
                            if self.velocitat[1] < 0 and x.velocitat[1] > 0: 
                                self.posició[1] = x.posició[1] + x.alçada   
                                self.velocitat[1] *= -0.4
                                x.velocitat[1] *= -0.4
                            elif self.velocitat[1] >= 0 and x.velocitat[1] > 0:  
                                x.posició[1] = self.posició[1] - x.alçada  
                                x.velocitat[1] *= -0.4
                                if x.magnitud_velocitat > 0.5:    
                                    self.velocitat[1] += -x.velocitat[1]
                            elif self.velocitat[1] < 0 and x.velocitat[1] <= 0:
                                self.posició[1] = x.posició[1] + x.alçada
                                self.velocitat[1] *= -0.4
                                if self.magnitud_velocitat > 0.5:    
                                    x.velocitat[1] += -self.velocitat[1]
                    elif x.dintre(self.posició[0], self.posició[1]) == True:
                        valor = x.posició[0] + x.amplada - self.posició[0]
                        if valor <= x.posició[1] + x.alçada - self.posició[1]:
                            if self.velocitat[0] < 0 and x.velocitat[0] > 0:    
                                self.posició[0] = x.posició[0] + x.amplada
                                self.velocitat[0] *= -0.4
                                x.velocitat[0] *= -0.4
                            elif self.velocitat[0] >= 0 and x.velocitat[0] > 0:    
                                x.posició[0] = self.posició[0] - x.amplada
                                x.velocitat[0] *= -0.4
                                if x.magnitud_velocitat > 0.5:    
                                    self.velocitat[0] += -x.velocitat[0]
                            elif self.velocitat[0] < 0 and x.velocitat[0] <= 0:
                                self.posició[0] = x.posició[0] + x.amplada
                                self.velocitat[0] *= -0.4
                                if self.magnitud_velocitat > 0.5:    
                                    x.velocitat[0] += -self.velocitat[0]
                        if valor >= x.posició[1] + x.alçada - self.posició[1]:
                            if self.velocitat[1] < 0 and x.velocitat[1] > 0: 
                                self.posició[1] = x.posició[1] + x.alçada   
                                self.velocitat[1] *= -0.4
                                x.velocitat[1] *= -0.4
                            elif self.velocitat[1] >= 0 and x.velocitat[1] > 0:  
                                x.posició[1] = self.posició[1] - x.alçada  
                                x.velocitat[1] *= -0.4
                                if x.magnitud_velocitat > 0.5:    
                                    self.velocitat[1] += -x.velocitat[1]
                            elif self.velocitat[1] < 0 and x.velocitat[1] <= 0:
                                self.posició[1] = x.posició[1] + x.alçada
                                self.velocitat[1] *= -0.4
                                if self.magnitud_velocitat > 0.5:    
                                    x.velocitat[1] += -self.velocitat[1]
                    elif x.dintre(self.posició[0], self.posició[1] + self.alçada) == True:
                        valor = x.posició[0] + x.amplada - self.posició[0]
                        if valor <= self.posició[1] + self.alçada - x.posició[1]:
                            if self.velocitat[0] < 0 and x.velocitat[0] > 0:    
                                self.posició[0] = x.posició[0] + x.amplada
                                self.velocitat[0] *= -0.4
                                x.velocitat[0] *= -0.4
                            elif self.velocitat[0] >= 0 and x.velocitat[0] > 0:    
                                x.posició[0] = self.posició[0] - x.amplada
                                x.velocitat[0] *= -0.4
                                if x.magnitud_velocitat > 0.5:    
                                    self.velocitat[0] += -x.velocitat[0]
                            elif self.velocitat[0] < 0 and x.velocitat[0] <= 0:
                                self.posició[0] = x.posició[0] + x.amplada
                                self.velocitat[0] *= -0.4
                                if self.magnitud_velocitat > 0.5:    
                                    x.velocitat[0] += -self.velocitat[0]
                        if valor >= self.posició[1] + self.alçada - x.posició[1]:
                            if self.velocitat[1] > 0 and x.velocitat[1] < 0:    
                                self.posició[1] = x.posició[1] -self.alçada
                                self.velocitat[1] *= -0.4
                                x.velocitat[1] *= -0.4
                            elif self.velocitat[1] <= 0 and x.velocitat[1] < 0:    
                                x.posició[1] = self.posició[1] + self.alçada
                                x.velocitat[1] *= -0.4
                                if x.magnitud_velocitat > 0.5:    
                                    self.velocitat[1] += -x.velocitat[1]
                            elif self.velocitat[1] > 0 and x.velocitat[1] >= 0:
                                self.posició[1] = x.posició[1] -self.alçada
                                self.velocitat[1] *= -0.4
                                if self.magnitud_velocitat > 0.5:    
                                    x.velocitat[1] += -self.velocitat[1]
                    elif x.dintre(self.posició[0] +self.amplada, self.posició[1] + self.alçada) == True:
                        valor = (self.posició[0] + self.amplada) - x.posició[0]
                        if valor <= self.posició[1] + self.alçada - x.posició[1]:
                            if self.velocitat[0] > 0 and x.velocitat[0] < 0:    
                                self.posició[0] = x.posició[0]-self.amplada
                                self.velocitat[0] *= -0.4
                                x.velocitat[0] *= -0.4
                            elif self.velocitat[0] <= 0 and x.velocitat[0] < 0:    
                                x.posició[0] = self.posició[0] + self.amplada
                                x.velocitat[0] *= -0.4
                                if x.magnitud_velocitat > 0.5:    
                                    self.velocitat[0] += -x.velocitat[0]
                            elif self.velocitat[0] > 0 and x.velocitat[0] >= 0:
                                self.posició[0] = x.posició[0]-self.amplada
                                self.velocitat[0] *= -0.4
                                if self.magnitud_velocitat > 0.5:    
                                    x.velocitat[0] += -self.velocitat[0]
                        if valor >= self.posició[1] + self.alçada - x.posició[1]:
                            if self.velocitat[1] > 0 and x.velocitat[1] < 0:    
                                self.posició[1] = x.posició[1] -self.alçada
                                self.velocitat[1] *= -0.4
                                x.velocitat[1] *= -0.4
                            elif self.velocitat[1] <= 0 and x.velocitat[1] < 0:    
                                x.posició[1] = self.posició[1] + self.alçada
                                x.velocitat[1] *= -0.4
                                if x.magnitud_velocitat > 0.5:
                                    self.velocitat[1] += -x.velocitat[1]
                            elif self.velocitat[1] > 0 and x.velocitat[1] >= 0:
                                self.posició[1] = x.posició[1] -self.alçada
                                self.velocitat[1] *= -0.4
                                if self.magnitud_velocitat > 0.5:    
                                    x.velocitat[1] += -self.velocitat[1]
            
    def reinici(self):
        self.posició = [self.posició_inicial[0], self.posició_inicial[1]]
        self.velocitat = [0,0]
        self.frenada = False

paret_dreta = caixa(pantalla_amplada, -500, pantalla_alçada + 500, 100, False)
paret_esquerra = caixa(-100, -500, pantalla_alçada + 500, 100, False)
terra = caixa(0, pantalla_alçada, 100, pantalla_amplada, False)
caixa2 = caixa(pantalla_amplada - 293, 300, 75, 75, True)
caixa3 = caixa(pantalla_amplada - 143, 300, 75, 75, True)
caixa4 = caixa(pantalla_amplada - 240, -50, 100, 20, True)
caixa5 = caixa(pantalla_amplada - 140, -50, 100, 20, True)
caixa6 = caixa(pantalla_amplada - 305, -100, 20, 250, True)
caixa7 = caixa(pantalla_amplada - 230, -300, 100, 100, True)
caixa1 = caixa(pantalla_amplada - 330, 200, 20, 300, True)

# Selecció de nivell
def selecció_nivell():
    nivell_seleccionat = 1
    selecció_nivell_acabada = False
    while not selecció_nivell_acabada:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and nivell_seleccionat < 12:
                    nivell_seleccionat += 1
                elif event.key == pygame.K_LEFT and nivell_seleccionat > 1:
                    nivell_seleccionat -= 1
                elif event.key == pygame.K_SPACE:
                    selecció_nivell_acabada = True
        
        pantalla.fill(fons)
        
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

        for i, text in enumerate(textos):
            pos = posicions[i]
            num_text = font_gran.render(str(i+1), True, taronja)
            num_x = pos[0] - num_text.get_width() // 2
            num_y = pos[1] - num_text.get_height() // 2
            pantalla.blit(num_text, (num_x, num_y))

        pygame.display.flip()

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

            # Creem una linea que començi desde un punt o altre depenent del ocell que llancem
            line = linea(ocell_actual)
            
            # Netejar la pantalla
            pantalla.fill(fons)
            # Aparèixer porcs, ocells i linea
            if mantenint_ocell:
                line.update()
            porcs()
            if ocell_anterior.llançat:    
                ocell_anterior.estela()
            for i in  llista_objectes_pantalla:
                i.update()
            llista_objectes_pantalla.sort(key=lambda i: i.posició[1])
            for self in llista_objectes_pantalla:
                if self in llista_ocells:
                    for i in llista_objectes_pantalla:
                        if i != self and i.posició != posició_inicial and self.posició != posició_inicial: 
                            self.colisió(i)
                if self in llista_objectes_rectangulars:
                    for i in llista_objectes_pantalla:
                        if i != self: 
                            self.colisió(i)
            for i in  llista_objectes_pantalla:
                i.dibuixar()
            linea_ocells(nivell[0], nivell[1], nivell[2], nivell[3], nivell[4], nivell[5])
        # Recarregar la pantalla
        pygame.display.flip()

    # Sortir del joc
    pygame.quit()

# Córrer el joc
GameLoop()
