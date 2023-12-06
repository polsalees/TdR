import pygame
import math
from codi_astres import distancia_ocell_ratoli
marró = (128, 64, 0)
marró2 = (118, 54, 0)
fons = pygame.image.load("Grafics/fons.jpg").convert_alpha()

def linea_ocells(ordre_ocells, diferencia, llista_ocells_llançats,pantalla, posició_inicial,pantalla_alçada):
    n = 1
    for i in ordre_ocells:
        if i not in llista_ocells_llançats:    
            if i.skin:
                if i.invisible == False:    
                    pantalla.blit(i.ocell_nou,(posició_inicial[0] - n*50-i.radi*1.1 + diferencia.x, pantalla_alçada - i.radi*2-5+diferencia.y))
                    rectangle2 = i.ocell_nou.get_rect(topleft =(posició_inicial[0] - n*50-i.radi*1.1 + diferencia.x, pantalla_alçada - i.radi*2-5+diferencia.y+i.diferencia_skin.y -0.45*i.radi))
                    rectangle = i.imatge_skin.get_rect(center=rectangle2.center)
                    rectangle.center += pygame.math.Vector2(0,0.1*i.radi)
                    pantalla.blit(i.imatge_skin, rectangle)
            else:
                pantalla.blit(i.ocell_nou,(posició_inicial[0] - n*50-i.radi*1.1 + diferencia.x, pantalla_alçada - i.radi*2-5+diferencia.y))
            n+=1
#Tirachines
def linea(ocell, x, diferencia, pantalla, posició_inicial, rectangle_base, punt_t1, punt_t2, punt_t3, punt_t4, punt_t5):
    pygame.draw.line(pantalla, marró2, punt_t1+diferencia, punt_t3+diferencia, width = 18)
    if x == True:
        pos = pygame.mouse.get_pos()
        angle = math.atan2(pos[0]-(posició_inicial[0]), pos[1]-(posició_inicial[1]))
        if distancia_ocell_ratoli(ocell) < (100+ocell.radi):
            pos = list(pos)
        else:
            distancia = distancia_ocell_ratoli(ocell) - 100 - ocell.radi
            pos = [pygame.mouse.get_pos()[0]-math.sin(angle)*distancia, pygame.mouse.get_pos()[1]-math.cos(angle)*distancia]
        rectangle = pygame.Rect(pos[0]-ocell.radi, pos[1]-ocell.radi, 2*ocell.radi, 2*ocell.radi)
        rectangle_base_2 = rectangle_base.copy() 
        if rectangle_base_2.colliderect(rectangle):
            if rectangle.center[0]-rectangle_base_2[0]<0:    
                if (rectangle.right-rectangle_base_2.left)/ocell.radi <=1:    
                    pos[1] = punt_t1[1]-ocell.radi*math.cos(math.acos((rectangle.right-rectangle_base_2.left)/ocell.radi)) 
                else:
                    pos[1] = punt_t1[1]-ocell.radi
            else:    
                if (rectangle_base_2.right- rectangle.left)/ocell.radi <= 1: 
                    pos[1] = punt_t1[1]-ocell.radi*math.cos(math.acos((rectangle_base_2.right- rectangle.left)/ocell.radi)) 
                else:
                    pos[1] = punt_t1[1]-ocell.radi
        pygame.draw.line(pantalla, (160,160,160), punt_t5+ diferencia, pos+ diferencia, width = 8)
        pygame.draw.line(pantalla, (160,160,160), punt_t4+diferencia, pos+ diferencia, width = 8)
        pygame.draw.line(pantalla, marró, punt_t1+diferencia, punt_t2+diferencia, width = 20)
        angle = math.degrees(angle)
        if angle<= 180:    
            angle = 180-angle
        else:
            angle = 360-angle + 180
        ocell.angle = -angle -90
        ocell.ocell_nou = pygame.transform.rotate(ocell.superficie_ocell, ocell.angle)
        ocell.rectangle_2 = ocell.ocell_nou.get_rect(center = pos)
    else:
        pygame.draw.line(pantalla, (160,160,160),punt_t5+diferencia, posició_inicial+diferencia, width = 8)
        pygame.draw.line(pantalla, (160,160,160),punt_t4+diferencia, posició_inicial+diferencia, width = 8)
        if ocell.angle != 0:
            ocell.angle = 0
            ocell.ocell_nou = pygame.transform.rotate(ocell.superficie_ocell, ocell.angle)
            ocell.rectangle_2 = ocell.ocell_nou.get_rect(center = posició_inicial)    
            ocell.rectangle_2.center = posició_inicial

class camera():
    def __init__(self, pantalla_amplada, pantalla_alçada, pantalla):
        self.pantalla = pantalla
        self.pantalla_amplada = pantalla_amplada
        self.pantalla_alçada = pantalla_alçada
        self.rectangle_camara_orig = (self.pantalla_amplada*0.2, self.pantalla_alçada*0.2)
        self.rectangle_camara = pygame.Rect(self.pantalla_amplada*0.2, self.pantalla_alçada*0.2, self.pantalla_amplada*0.6, self.pantalla_alçada*0.6)
        self.diferencia = pygame.math.Vector2(0,0)
        self.diferencia_2 = pygame.math.Vector2(0,0)
        self.tornar_ocell = True
        self.principi_nivell = True
        self.posició_inicial = [150, pantalla_alçada-150]
        self.rectangle_base = pygame.Rect(self.posició_inicial[0]-10, self.posició_inicial[1]+55, 20, pantalla_alçada-self.posició_inicial[1]-55)
        self.punt_t1 = (self.posició_inicial[0], self.posició_inicial[1]+55)
        self.punt_t2 = (self.posició_inicial[0]+50,self.posició_inicial[1]-50)
        self.punt_t3 = (self.posició_inicial[0]-60,self.posició_inicial[1]-50)
        self.punt_t4 = (self.posició_inicial[0]+50,self.posició_inicial[1]-45)
        self.punt_t5 = (self.posició_inicial[0]-60,self.posició_inicial[1]-45)
        relació = fons.get_width()/fons.get_height()
        fons1 = pygame.transform.scale(fons,(fons.get_width()*3, fons.get_height()*3))
        self.fons  = pygame.Surface((2.2*pantalla_amplada, 2.2*pantalla_alçada))
        x = 0
        y = 0
        self.superficie2= pygame.Surface((2*pantalla_amplada, 2*pantalla_alçada))
        for i in range(8):
            self.fons.blit(fons1,(x,y))
            x+=fons.get_width()*3
            if x>pantalla_amplada*2.2+fons.get_width():
                x = 0
                y += fons.get_height()*3
    def cam_1(self,personatge,factor_de_potencia):
        if personatge.tocat_objecte==False:    
            if personatge.rectangle.top < self.rectangle_camara.top:
                self.rectangle_camara.top = personatge.rectangle.top 
            if personatge.rectangle.right > self.rectangle_camara.right:
                self.rectangle_camara.right = personatge.rectangle.right 
            if personatge.rectangle.bottom > self.rectangle_camara.bottom:
                self.rectangle_camara.bottom = personatge.rectangle.bottom
            if self.rectangle_camara.bottom > self.pantalla_alçada*0.85:
                self.rectangle_camara.bottom = self.pantalla_alçada*0.85
            self.diferencia.x =self.rectangle_camara_orig[0]-self.rectangle_camara.left
            self.diferencia.y =self.rectangle_camara_orig[1]-self.rectangle_camara.top
            self.diferencia=round(self.diferencia)
        else:
            if factor_de_potencia!= 0.125:    
                self.camara_punt((personatge.posició_primer_xoc[0]-self.pantalla_amplada*0.3, personatge.posició_primer_xoc[1]-self.pantalla_alçada*0.3))
            else:
                self.camara_punt((personatge.posició_primer_xoc[0]-self.pantalla_amplada*0.3, self.rectangle_camara_orig[1]))
    def camara_punt(self,punt):
        self.rectangle_camara_orig_2 = self.rectangle_camara.topleft 
        self.diferencia_2.x =punt[0]-self.rectangle_camara.left
        self.diferencia_2.y =punt[1]-self.rectangle_camara.top
        self.diferencia_2*=0.1
        self.rectangle_camara.left = self.rectangle_camara_orig_2[0] + self.diferencia_2.x
        self.rectangle_camara.top = self.rectangle_camara_orig_2[1] + self.diferencia_2.y
        if self.rectangle_camara.bottom > self.pantalla_alçada*0.85:
            self.rectangle_camara.bottom = self.pantalla_alçada*0.85
        if self.rectangle_camara.left < -self.pantalla_amplada*0.05:
            self.rectangle_camara.left = -self.pantalla_amplada*0.05
        if self.rectangle_camara.right > self.pantalla_amplada*1.85:
            self.rectangle_camara.right = self.pantalla_amplada*1.85
        if self.rectangle_camara.top < -self.pantalla_alçada*1.05:
            self.rectangle_camara.top = -self.pantalla_alçada*1.05
        self.diferencia.x =self.rectangle_camara_orig[0]-self.rectangle_camara.left
        self.diferencia.y =self.rectangle_camara_orig[1]-self.rectangle_camara.top
        self.diferencia=round(self.diferencia)
    def camara_ratoli(self, mantenint, posició_mantenint, rectangle_mantenint):
        if mantenint:
            self.tornar_ocell = False
            diferencia_ratoli = pygame.math.Vector2()    
            diferencia_ratoli.x =pygame.mouse.get_pos()[0]-posició_mantenint[0]
            diferencia_ratoli.y =pygame.mouse.get_pos()[1]-posició_mantenint[1]
            self.rectangle_camara.left = rectangle_mantenint.left - diferencia_ratoli.x*2
            self.rectangle_camara.top = rectangle_mantenint.top - diferencia_ratoli.y*2
            if self.rectangle_camara.bottom > self.pantalla_alçada*0.85:
                self.rectangle_camara.bottom = self.pantalla_alçada*0.85
            if self.rectangle_camara.left < -self.pantalla_amplada*0.05:
                self.rectangle_camara.left = -self.pantalla_amplada*0.05
            if self.rectangle_camara.right > self.pantalla_amplada*1.85:
                self.rectangle_camara.right = self.pantalla_amplada*1.85
            if self.rectangle_camara.top < -self.pantalla_alçada*1.05:
                self.rectangle_camara.top = -self.pantalla_alçada*1.05
            self.diferencia.x =self.rectangle_camara_orig[0]-self.rectangle_camara.left
            self.diferencia.y =self.rectangle_camara_orig[1]-self.rectangle_camara.top
            self.diferencia=round(self.diferencia)
    def update(self, llista_objectes_pantalla, personatge, ocells_nivell,ocell_actual, mantenint_ocell,ocell_anterior, mantenint,posició_mantenint,rectangle_mantenint, llista_ocells_llançats, factor_de_potencia,llista_ocells):
        if mantenint_ocell == False and (ocell_actual.radi != 0 or ocell_anterior.tocat_objecte== False):    
            if self.principi_nivell:
                self.camara_punt((self.pantalla_amplada , self.rectangle_camara_orig[1]))
            elif (personatge in llista_objectes_pantalla and personatge.temps_desde_tocar_objectes <= 200):
                self.cam_1(personatge, factor_de_potencia)
                self.tornar_ocell = True
            else:
                if self.tornar_ocell or mantenint_ocell:   
                    self.camara_punt(self.rectangle_camara_orig)
                self.camara_ratoli(mantenint,posició_mantenint,rectangle_mantenint)
        else:
            self.diferencia *=0
        self.pantalla.fill((0,0,0))
        if mantenint_ocell == False and (ocell_actual.radi != 0 or  ocell_anterior.tocat_objecte==False):
            self.pantalla.blit(self.fons, (-0.2*self.pantalla_amplada,-self.pantalla_alçada*1.2)+self.diferencia)
            if ocell_anterior.llançat:    
                ocell_anterior.estela(self.diferencia, self.pantalla)  
            linea_ocells(ocells_nivell, self.diferencia, llista_ocells_llançats, self.pantalla,self.posició_inicial, self.pantalla_alçada)
            linea(ocell_actual,mantenint_ocell, self.diferencia, self.pantalla,self.posició_inicial, self.rectangle_base, self.punt_t1, self.punt_t2, self.punt_t3, self.punt_t4, self.punt_t5)
            for i in  llista_objectes_pantalla:
                if i in llista_ocells:    
                    i.dibuixar(self.diferencia, factor_de_potencia, self.pantalla)
                else:
                    i.dibuixar(self.diferencia, self.pantalla)
            pygame.draw.line(self.pantalla, marró, self.punt_t1+self.diferencia, self.punt_t2+self.diferencia, width = 20)
            rectangle_base_2 = self.rectangle_base.copy() 
            rectangle_base_2.topleft += self.diferencia
            pygame.draw.rect(self.pantalla, marró, rectangle_base_2)
        else:    
            self.superficie2.blit(self.fons, (-0.2*self.pantalla_amplada,-self.pantalla_alçada*0.2))
            self.superficie2.blit(self.fons, (-0.2*self.pantalla_amplada,-self.pantalla_alçada*0.2)+pygame.math.Vector2(0, self.pantalla_alçada))            
            self.superficie2.blit(self.fons, (-0.2*self.pantalla_amplada,-self.pantalla_alçada*0.2)+pygame.math.Vector2(self.pantalla_amplada, self.pantalla_alçada))            
            self.superficie2.blit(self.fons, (-0.2*self.pantalla_amplada,-self.pantalla_alçada*0.2)+pygame.math.Vector2(self.pantalla_amplada, 0))            
            linea_ocells(ocells_nivell, pygame.math.Vector2(0,self.pantalla_alçada), llista_ocells_llançats, self.superficie2,self.posició_inicial, self.pantalla_alçada)
            linea(ocell_actual,mantenint_ocell, pygame.math.Vector2(0,self.pantalla_alçada), self.superficie2,self.posició_inicial, self.rectangle_base, self.punt_t1, self.punt_t2, self.punt_t3, self.punt_t4, self.punt_t5)
            if ocell_anterior.llançat:    
                ocell_anterior.estela(pygame.math.Vector2(0,self.pantalla_alçada), self.superficie2)  
            for i in  llista_objectes_pantalla:
                if i in llista_ocells:  
                    i.dibuixar(pygame.math.Vector2(0,self.pantalla_alçada), factor_de_potencia, self.superficie2)
                else:    
                    i.dibuixar(pygame.math.Vector2(0,self.pantalla_alçada), self.superficie2)
            pygame.draw.line(self.superficie2, marró, self.punt_t1+pygame.math.Vector2(0,self.pantalla_alçada), self.punt_t2+pygame.math.Vector2(0,self.pantalla_alçada), width = 20)
            rectangle_base_2 = self.rectangle_base.copy() 
            rectangle_base_2.topleft += pygame.math.Vector2(0,self.pantalla_alçada)
            pygame.draw.rect(self.superficie2, marró, rectangle_base_2)
            pantalla = pygame.transform.scale(self.superficie2, (self.pantalla_amplada,self.pantalla_alçada))
            self.pantalla.blit(pantalla, (0,0)) 
