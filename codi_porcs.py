import pygame
import math
from colisió_ocells import colisió_cercles
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
fons = (80, 80, 255)
gris=(50,50,50)
pedra = (139,140,122)
gravetat = 0.05

class porc():
    def __init__(self, radi, posició, llista_porcs, llista_objectes_rodons, pantalla):    
        global gravetat
        self.radi = radi
        self.velocitat = pygame.math.Vector2(0,0)
        self.angle_rampa = 0
        global llista_objectes_pantalla
        llista_porcs.append(self) 
        llista_objectes_rodons.append(self)
        self.colisionat = False
        self.superficie_porc = pygame.Surface((3*self.radi, 3*self.radi), pygame.SRCALPHA)
        self.rectangle = self.superficie_porc.get_rect()
        self.rectangle.center = posició
        pygame.draw.circle(self.superficie_porc, verd, (self.radi*1.5, self.radi*1.5), self.radi)
        self.mask = pygame.mask.from_surface(self.superficie_porc)
        self.c = 0
        self.posició_real = posició
        self.massa = self.radi**2 *3.14
        self.posició_inicial = posició
        self.rectangle.center = posició
        self.porc = True
        self.n = 0
        self.angle = 0
        pygame.draw.circle(self.superficie_porc, verd, (self.radi*1.75, self.radi/3 ), self.radi/4)
        pygame.draw.circle(self.superficie_porc, verd, (self.radi*2.3, self.radi/1.60), self.radi/4)
        pygame.draw.circle(self.superficie_porc, verd_fosc, (self.radi*1.5, self.radi*1.65), self.radi/2.5)
        pygame.draw.circle(self.superficie_porc, blanc, (self.radi*2.1, self.radi*1.3), self.radi/4)
        pygame.draw.circle(self.superficie_porc, negre, (self.radi*2.1, self.radi*1.3), self.radi/6)
        pygame.draw.circle(self.superficie_porc, blanc, (self.radi*0.9, self.radi*1.3), self.radi/4)
        pygame.draw.circle(self.superficie_porc, negre, (self.radi*0.9, self.radi*1.3), self.radi/6)
        pygame.draw.line(self.superficie_porc, negre, (self.radi*1.3,self.radi*2.2), (1.7*self.radi, 2.2*self.radi), width=round(self.radi/5))
        pygame.draw.line(self.superficie_porc, negre, (self.radi*1.35,self.radi*1.8), (1.35*self.radi, 1.4*self.radi), width=round(self.radi/6))
        pygame.draw.line(self.superficie_porc, negre, (self.radi*1.65,self.radi*1.8), (1.65*self.radi, 1.4*self.radi), width=round(self.radi/6))
        self.porc_nou = self.superficie_porc.copy()
        self.rectangle_2 = self.rectangle.copy()
        self.pantalla = pantalla
        self.pantalla_rect = pantalla.get_rect()
    
    def update(self, llista_objectes_pantalla):
        if self.porc:
            if self.c == 1:
                self.posició_real = self.rectangle.center
                self.c = 0    
            self.colisionat = False
            self.posició_real += self.velocitat
            self.posició_real[1] += 0.5*gravetat
            self.velocitat[1] += gravetat 
            if abs(self.velocitat[1]) < gravetat:
                self.velocitat[1] = 0
            if abs(self.velocitat[0]) < gravetat:
                self.velocitat[0] = 0
            self.rectangle.center = self.posició_real
            self.angle -= self.velocitat[0]
            self.porc_nou = pygame.transform.rotate(self.superficie_porc, self.angle)
            self.rectangle_2 = self.porc_nou.get_rect(center = self.posició_real)
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
    def dibuixar(self,diferencia):
        rectangle = self.rectangle_2.copy()
        rectangle.topleft += diferencia   
        if rectangle.colliderect(self.pantalla_rect):    
            if self.porc:    
                self.pantalla.blit(self.porc_nou, rectangle)
            else:    
                for i in self.animació:
                    pygame.draw.circle(self.pantalla,verd,i[1]+diferencia,i[0])
    def reinici(self):
        self.velocitat *= 0
        self.rectangle.center = self.posició_inicial
        self.posició_real = self.posició_inicial
        self.porc = True
        self.n = 0
        self.angle = 0
        self.rectangle_2 = self.rectangle.copy()
        self.ocell_nou = self.superficie_porc.copy()

    def colisió(self,x,llista_ocells, llista_objectes_rectangulars, llista_objectes_rodons, llista_porcs,nombre_porcs, llista_objectes_pantalla):
        nombre_porcs = colisió_cercles(self,x, llista_ocells, llista_objectes_rectangulars, llista_objectes_rodons, llista_porcs, nombre_porcs, llista_objectes_pantalla)
        return nombre_porcs
    def destrucció(self):
        self.velocitat *= 0
        self.angle_rampa = 90
        radi = self.radi/2
        self.porc  = False
        self.animació = [[radi,self.rectangle.center],[radi,self.rectangle.center],[radi,self.rectangle.center],[radi,self.rectangle.center]]
    def copy(self, posició, llista_porcs, llista_objectes_rodons):
        x = porc(self.radi, posició, llista_porcs, llista_objectes_rodons, self.pantalla)
        return x