import pygame
import math
from colisió_ocells import colisió_cercles
from colisió_ocells import calcul_angle_cercle
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
gris=(50,50,50)
gravetat = 0.05
#Cargem les imatges
art = pygame.image.load("Grafics/art.png").convert_alpha()
art2 = pygame.image.load("Grafics/art2.png").convert_alpha()
art3 = pygame.image.load("Grafics/art3.png").convert_alpha()
def calcular_angle(self):
    angle = math.degrees(math.atan2(pygame.mouse.get_pos()[0] - (self.posició_inicial[0]), pygame.mouse.get_pos()[1] - (self.posició_inicial[1])))
    return angle

def distancia_ocell_ratoli(self):
    amplada = math.sqrt(((pygame.mouse.get_pos()[0] - (self.posició_inicial[0])) **2 + (pygame.mouse.get_pos()[1] - (self.posició_inicial[1])) ** 2))
    return amplada
class ocell():
    def __init__(self, radi, color, llista_ocells, llista_objectes_rodons, posició_inicial, pantalla):
        global gravetat
        self.skin = False
        self.pantalla = pantalla
        self.temps_desde_tocar_objectes = 0
        self.animació = False
        self.radi = radi
        self.velocitat = pygame.math.Vector2(0,0)
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
        llista_objectes_rodons.append(self) 
        self.colisionat = False
        self.superficie_ocell = pygame.Surface((2.2*self.radi, 2.2*self.radi), pygame.SRCALPHA)
        self.rectangle = self.superficie_ocell.get_rect()
        self.rectangle.center = (posició_inicial[0], posició_inicial[1])
        if self.color != negre:    
            self.color2 = self.color - pygame.math.Vector3(100,100,100)
            color2 = []
            for i in self.color2:
                if i > 255:
                    i = 255
                if i < 0:
                    i = 0
                color2.append(i)
            self.color2 = color2
        else:
            self.color2 = gris
        pygame.draw.circle(self.superficie_ocell, self.color2, (self.radi*1.1, self.radi*1.1), self.radi)
        self.mask = pygame.mask.from_surface(self.superficie_ocell)
        if self.color!=vermell:    
            pygame.draw.circle(self.superficie_ocell, self.color, (self.radi*1.1, self.radi*0.75), self.radi*0.7)
            pygame.draw.circle(self.superficie_ocell, self.color, (self.radi*1.4, self.radi*0.95), self.radi*0.7)
            pygame.draw.circle(self.superficie_ocell, self.color, (self.radi*0.7, self.radi*0.95), self.radi*0.7)
            pygame.draw.circle(self.superficie_ocell, self.color, (self.radi*1.1, self.radi*1), self.radi*0.8)
            pygame.draw.circle(self.superficie_ocell, self.color, (self.radi*1.3, self.radi*0.8), self.radi*0.7)
            pygame.draw.circle(self.superficie_ocell, self.color2, (self.radi*1.85, self.radi*0.9), self.radi/3)
            pygame.draw.circle(self.superficie_ocell, self.color2, (self.radi*1.15, self.radi*0.9), self.radi/3)
            pygame.draw.line(self.superficie_ocell, self.color, (self.radi,self.radi/3), (0, 0), width=round(self.radi/2))
            pygame.draw.circle(self.superficie_ocell, blanc, (self.radi*1.85, self.radi*0.9), self.radi/4)
            pygame.draw.circle(self.superficie_ocell, negre, (self.radi*1.85, self.radi*0.9), self.radi/6)
            pygame.draw.circle(self.superficie_ocell, blanc, (self.radi*1.15, self.radi*0.9), self.radi/4)
            pygame.draw.circle(self.superficie_ocell, negre, (self.radi*1.15, self.radi*0.9), self.radi/6)
            pygame.draw.polygon(self.superficie_ocell, taronja, ((self.radi*1.5,self.radi*1.2), (self.radi*1.5,self.radi*1.7), (self.radi*2.2,self.radi*1.45)))
            pygame.draw.line(self.superficie_ocell, negre, (self.radi*1.5,self.radi*1.45), (self.radi*2.2,self.radi*1.45), width=round(self.radi/20))
            if self.color != negre:
                pygame.draw.line(self.superficie_ocell, negre, (self.radi*0.8,self.radi*0.4), (1.8*self.radi, 0.4*self.radi), width=round(self.radi/5))
            else:
                pygame.draw.line(self.superficie_ocell, blanc, (self.radi*0.8,self.radi*0.4), (1.8*self.radi, 0.4*self.radi), width=round(self.radi/5))
            self.superficie_ocell_orig = self.superficie_ocell.copy()
            self.superficie_ocell_2 = pygame.Surface((2.2*self.radi, 2.2*self.radi), pygame.SRCALPHA)
            pygame.draw.circle(self.superficie_ocell_2, self.color2, (self.radi*1.1, self.radi*1.1), self.radi)
            pygame.draw.circle(self.superficie_ocell_2, self.color, (self.radi*1.1, self.radi*0.75), self.radi*0.7)
            pygame.draw.circle(self.superficie_ocell_2, self.color, (self.radi*1.4, self.radi*0.95), self.radi*0.7)
            pygame.draw.circle(self.superficie_ocell_2, self.color, (self.radi*0.7, self.radi*0.95), self.radi*0.7)
            pygame.draw.circle(self.superficie_ocell_2, self.color, (self.radi*1.1, self.radi*1), self.radi*0.8)
            pygame.draw.circle(self.superficie_ocell_2, self.color, (self.radi*1.3, self.radi*0.8), self.radi*0.7)
            pygame.draw.circle(self.superficie_ocell_2, self.color2, (self.radi*1.85, self.radi*0.9), self.radi/3)
            pygame.draw.circle(self.superficie_ocell_2, self.color2, (self.radi*1.15, self.radi*0.9), self.radi/3)
            pygame.draw.line(self.superficie_ocell_2, self.color, (self.radi,self.radi/3), (0, 0), width=round(self.radi/2))
            pygame.draw.circle(self.superficie_ocell_2, blanc, (self.radi*1.85, self.radi*0.9), self.radi/4)
            pygame.draw.circle(self.superficie_ocell_2, negre, (self.radi*1.85, self.radi*0.9), self.radi/6)
            pygame.draw.circle(self.superficie_ocell_2, blanc, (self.radi*1.15, self.radi*0.9), self.radi/4)
            pygame.draw.circle(self.superficie_ocell_2, negre, (self.radi*1.15, self.radi*0.9), self.radi/6)
            pygame.draw.polygon(self.superficie_ocell_2, taronja, ((self.radi*1.5,self.radi*1.2), (self.radi*1.5,self.radi*1.45), (self.radi*2.2,self.radi*1.2)))
            pygame.draw.polygon(self.superficie_ocell_2, taronja, ((self.radi*1.5,self.radi*1.45), (self.radi*1.5,self.radi*1.7), (self.radi*2.2,self.radi*1.8)))
            if self.color != negre:
                pygame.draw.line(self.superficie_ocell_2, negre, (self.radi*0.8,self.radi*0.1), (1.5*self.radi, 0.4*self.radi), width=round(self.radi/5))
                pygame.draw.line(self.superficie_ocell_2, negre, (self.radi*1.5,self.radi*0.4), (1.8*self.radi, 0.1*self.radi), width=round(self.radi/5))
            else:
                pygame.draw.line(self.superficie_ocell_2, blanc, (self.radi*0.8,self.radi*0.1), (1.5*self.radi, 0.4*self.radi), width=round(self.radi/5))
                pygame.draw.line(self.superficie_ocell_2, blanc, (self.radi*1.5,self.radi*0.4), (1.8*self.radi, 0.1*self.radi), width=round(self.radi/5))
            self.superficie_ocell_3 = self.superficie_ocell_2.copy()
        else:    
            self.superficie_ocell = art
            self.superficie_ocell = pygame.transform.scale(self.superficie_ocell,(self.radi*2,self.radi*2))
            self.superficie_ocell_2 = art2
            self.superficie_ocell_2 = pygame.transform.scale(self.superficie_ocell_2,(self.radi*8/3,self.radi*2))
            self.superficie_ocell_3 = art3
            self.superficie_ocell_3 = pygame.transform.scale(self.superficie_ocell_3,(self.radi*2,self.radi*2))
            self.superficie_ocell_orig = self.superficie_ocell.copy()
        self.c = 0
        self.posició_real = posició_inicial
        self.massa = self.radi**2 *3.14
        self.activat = False
        self.n = 0
        self.llista_estela = []
        self.llista_copia = []
        self.ocell_nou = self.superficie_ocell.copy()
        self.rectangle_2 = self.rectangle.copy()
        self.rectangle_2.center = posició_inicial
        self.angle = 0
        self.posició_inicial = posició_inicial
        self.pantalla_rect = pantalla.get_rect()
    
    def calcul_posició_primer_xoc (self):
        if self.tocat_objecte == False:
            self.posició_primer_xoc = self.rectangle.center 
            self.superficie_ocell = self.superficie_ocell_3
            self.tocat_objecte = True
            self.llista_copia.clear()
    
    def colisió(self,x, llista_ocells, llista_objectes_rectangulars, llista_objectes_rodons, llista_porcs,nombre_porcs,llista_objectes_pantalla):
        nombre_porcs = colisió_cercles(self,x, llista_ocells, llista_objectes_rectangulars, llista_objectes_rodons, llista_porcs, nombre_porcs,llista_objectes_pantalla)
        return nombre_porcs
    def calcul_linea_direció(self, diferencia, factor_de_potencia):
        self.linea_direció_radi = 5
        self.linea_direció_posició = [self.posició_inicial[0], self.posició_inicial[1]] + diferencia
        self.potencia = distancia_ocell_ratoli(self) - self.radi
        angle = math.radians(calcular_angle(self))
        if self.potencia >= 100:
            self.potencia = 100
        if self.potencia <= 0 or angle > -0.1 or angle < -3:
            self.potencia = 0
        if self.potencia !=0:
            self.linea_direció_velocitat[0] = -math.sin(angle) * self.potencia * factor_de_potencia
            self.linea_direció_velocitat[1] = -math.cos(angle) * self.potencia * factor_de_potencia
            self.linea_direció_velocitat[1]  += gravetat * 0.2 *(self.linea_direció_moviment%30)
            self.linea_direció_posició[0] += self.linea_direció_velocitat[0] * 0.2 *(self.linea_direció_moviment%30)
            self.linea_direció_posició[1] += self.linea_direció_velocitat[1] * 0.2 *(self.linea_direció_moviment%30)
            pygame.draw.circle(self.pantalla, blanc, self.linea_direció_posició, self.linea_direció_radi)    
            while self.linea_direció_radi >1:   
                self.linea_direció_radi -= 0.2
                self.linea_direció_velocitat[1]  += gravetat * 6
                self.linea_direció_posició[0] += self.linea_direció_velocitat[0] * 6
                self.linea_direció_posició[1] += self.linea_direció_velocitat[1] * 6
                pygame.draw.circle(self.pantalla, blanc, self.linea_direció_posició, self.linea_direció_radi)
            self.linea_direció_moviment +=0.5
    def posar_skin(self, imatge):
        if self.skin == False:
            self.imatge_skin = pygame.transform.scale(imatge,(self.radi*2, self.radi*2+(9/5)*self.radi))
            self.skin_offset = pygame.math.Vector2(0,-0.45*self.radi)
            self.diferencia_skin = pygame.math.Vector2(0,-1.25*self.radi)
            self.skin = True
            self.rectangle_skin = self.imatge_skin.get_rect()
        else:
            self.skin = False
    def estela(self,diferencia): 
        for i in self.llista_estela:
            pygame.draw.circle(self.pantalla, blanc, i[0]+diferencia ,i[1])
    
    def update(self, nombre_ocells, llista_objectes_pantalla):
        if self.c == 1:
            self.posició_real = self.rectangle.center
            self.c = 0
        if self.llançat and self.tocat_objecte == False:
            self.n+=1
            if self.n%5 == 0:
                if self.llista_copia == []:    
                    self.llista_estela.append((self.rectangle.center,2))
                else:
                    for i in self.llista_copia:
                        i.llista_estela.append((self.rectangle.center,2))
        if self.aire:  
            self.posició_real += self.velocitat
            self.posició_real[1] += 0.5*gravetat
            self.velocitat[1] += gravetat
            if abs(self.velocitat[1]) < gravetat:
                self.velocitat[1] = 0
            if abs(self.velocitat[0]) < gravetat:
                self.velocitat[0] = 0
            self.rectangle.center = self.posició_real
            if self.tocat_objecte == False or self.velocitat.length()>2.5:
                self.angle = self.velocitat.angle_to((-1,0)) +180
            else:
                self.angle -= self.velocitat[0]
            self.ocell_nou = pygame.transform.rotate(self.superficie_ocell, self.angle)
            self.rectangle_2 = self.ocell_nou.get_rect(center = self.posició_real)
            if self.tocat_objecte:
                self.temps_desde_tocar_objectes += 1
        if self.llançat:
            if self.velocitat.length()<gravetat:    
                self.cooldown += 1
        else:
            self.cooldown = 0
        if self.cooldown >= 30:    
            nombre_ocells-=1 
            llista_objectes_pantalla.remove(self)
        self.colisionat = False
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
        return nombre_ocells

    def dibuixar(self, diferencia, factor_de_potencia):
        if self.linea_direció:
            self.calcul_linea_direció(diferencia, factor_de_potencia)
        rectangle = self.rectangle_2.copy()   
        rectangle.topleft += diferencia  
        if rectangle.colliderect(self.pantalla_rect):  
            self.pantalla.blit(self.ocell_nou, rectangle)
            if self.skin:
                imatge_skin_rotada = pygame.transform.rotate(self.imatge_skin, self.angle)
                if self.llançat and self.tocat_objecte == False:
                    self.rectangle_skin = imatge_skin_rotada.get_rect(center =self.rectangle_2.center + diferencia + self.skin_offset.rotate(-self.angle)+pygame.math.Vector2((8/3-2)*self.radi,0).rotate(-self.angle))
                else:
                    self.rectangle_skin = imatge_skin_rotada.get_rect(center =self.rectangle_2.center + diferencia + self.skin_offset.rotate(-self.angle))
                self.pantalla.blit(imatge_skin_rotada, self.rectangle_skin)
            if self.animació:
                for i in self.objecte_animació:
                    pygame.draw.circle(self.pantalla,self.color_animació,i[1]+diferencia,i[0])

    def llançament(self, factor_de_potencia):
        self.rectangle.center = self.posició_inicial
        self.potencia = distancia_ocell_ratoli(self) - self.radi
        angle = math.radians(calcular_angle(self))
        if self.potencia >= 100:
            self.potencia = 100
        if self.potencia <= 0 or angle > -0.1 or angle < -3:
            self.potencia = 0
        if self.potencia != 0:
            self.superficie_ocell = self.superficie_ocell_2
            self.velocitat[0] = -math.sin(angle) * self.potencia * factor_de_potencia
            self.velocitat[1] = -math.cos(angle) * self.potencia * factor_de_potencia
            self.llançat = True
            self.aire = True
    
    def zona_llançament(self,diferencia):
        rectangle = self.rectangle.copy()
        rectangle.topleft+=diferencia
        self.zona = rectangle.collidepoint(pygame.mouse.get_pos())
        return self.zona
    def habilitat(self, llista_ocells, llista_objectes_rodons, llista_objectes_pantalla, llista_porcs, llista_objectes_rectangulars, sprites, nombre_ocells):
        if self.activat == False and self.color != vermell:
            self.llista_estela.append((self.rectangle.center, 10))
            self.n = 0    
            if self.color == groc:
                self.activar_animació(blanc,1) 
                self.velocitat[0] *= 2.5
            elif self.color == cian:
                self.activar_animació(blanc,1) 
                self.copia1 = self.copy(llista_ocells, llista_objectes_rodons)
                self.copia2 = self.copy(llista_ocells, llista_objectes_rodons) 
                self.copia1.llançat = True
                self.copia2.llançat = True
                self.copia1.aire = True
                self.copia2.aire = True
                self.copia1.tocat_objecte = False
                self.copia2.tocat_objecte = False
                self.copia1.posició_real = self.rectangle.center
                self.copia2.posició_real = self.rectangle.center
                if self.skin:
                    self.copia1.posar_skin(self.imatge_skin)
                    self.copia2.posar_skin(self.imatge_skin)
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
                nombre_ocells+=2
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
                                potencia = 400 - distancia_explosió.length() + self.radi
                                if potencia >0:
                                    angle = calcul_angle_cercle(self,i.rectangle.center) +180
                                    if angle <= 180:    
                                        angle = 180- angle
                                    else:
                                        angle = 360-angle + 180
                                    if self.color == blanc:
                                        angle +=180
                                        potencia *=2
                                    else:
                                        potencia +=30
                                    potencia /= 5
                                    i.velocitat += pygame.math.Vector2.from_polar((potencia*50/i.massa, angle))
                        elif i in llista_ocells:    
                            if i.llançat:    
                                distancia_explosió = pygame.math.Vector2(self.rectangle.center) - i.rectangle.center
                                potencia = 400 - distancia_explosió.length() + self.radi
                                if potencia >0:
                                    angle = calcul_angle_cercle(self,i.rectangle.center)
                                    if angle <= 180:    
                                        angle = 180- angle
                                    else:
                                        angle = 360-angle +180
                                    if self.color == blanc:
                                        angle +=180
                                        potencia *=2
                                    else:    
                                        potencia +=30
                                    potencia /= 2.5
                                    i.velocitat += pygame.math.Vector2.from_polar((potencia*50/i.massa, angle))
                        if i in llista_objectes_rectangulars:    
                            if i.caixa and i.movible:    
                                distancia_explosió = pygame.math.Vector2(self.rectangle.center) - i.rectangle.center
                                potencia = 400 - distancia_explosió.length() + self.radi
                                if potencia >0:
                                    angle = calcul_angle_cercle(self,i.rectangle.center) + 180
                                    if angle <= 180:    
                                        angle = 180- angle
                                    else:
                                        angle = 360-angle + 180
                                    if self.color == blanc:
                                        angle +=180
                                        potencia *=2
                                    else:    
                                        potencia +=30
                                    potencia /= 2.5
                                    i.mig_trencat(potencia*50/i.massa/100, llista_objectes_pantalla, llista_porcs, llista_ocells)
                                    i.velocitat += pygame.math.Vector2.from_polar((potencia*100/(i.massa*0.7), angle))

            self.activat = True
        return nombre_ocells
    def copy(self, llista_ocells, llista_objectes_rodons):
        x = ocell(self.radi, self.color, llista_ocells, llista_objectes_rodons, self.posició_inicial, self.pantalla)
        return x
    def reinici(self):
        self.skin = False
        self.temps_desde_tocar_objectes = 0
        self.activat = False
        self.aire = False
        self.velocitat *= 0
        self.llançat = False
        self.llista_estela.clear()
        self.n = 0
        self.rectangle.center = [self.posició_inicial[0], self.posició_inicial[1]]
        self.posició_real = [self.posició_inicial[0], self.posició_inicial[1]]
        self.zona = False
        self.cooldown = 0
        self.tocat_objecte = False
        self.linea_direció = False
        self.posició_primer_xoc = [0,0] 
        self.animació = False
        self.llista_copia.clear()
        self.angle = 0
        self.superficie_ocell = self.superficie_ocell_orig
        self.rectangle_2 = self.rectangle.copy()
        self.ocell_nou = self.superficie_ocell.copy()
    
    def activar_animació(self, color,radi2):
        radi = self.radi /radi2
        self.color_animació = color
        self.animació=True
        self.objecte_animació = [[radi,self.rectangle.center],[radi,self.rectangle.center],[radi,self.rectangle.center],[radi,self.rectangle.center]]