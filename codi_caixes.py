import pygame
import math
import random
from colisió_ocells import calcul_angle_cercle 
from rotació import rotacions

negre = (0, 0, 0)
blanc = (255, 255, 255)
vermell = (255, 0, 0)
vermell2 = (200, 0, 0)
verd = (0, 255, 0)
verd_fosc = (227,227,208)
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

class caixa():
    def __init__(self, posició, alçada, amplada, movible, angle, tipo, llista_objectes_rectangulars,pantalla):
        self.alçada = alçada
        self.amplada = amplada
        self.pantalla = pantalla
        self.tipo = tipo 
        if self.tipo == 5:
            self.tipo = 2
        self.massa = self.alçada*self.amplada*(self.tipo**1.5/2**1.5)
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
        if self.tipo == 1:
            self.color_borde = blau_fosc
            self.color = cian
        elif self.tipo == 2:
            self.color_borde = marró_fosc  
            self.color = marró
        elif self.tipo == 3:
            self.color_borde = gris 
            self.color   = pedra
        self.superficie_rectangle.fill(self.color)
        if self.amplada < self.alçada:    
            pygame.draw.rect(self.superficie_rectangle, self.color_borde , ((0,0), (self.amplada, self.alçada)), 10 - (100//self.amplada))
        else:
            pygame.draw.rect(self.superficie_rectangle, self.color_borde , ((0,0), (self.amplada, self.alçada)), 10 - (100//self.alçada))
        self.tipo = tipo 
        if self.tipo == 5:
            pygame.draw.rect(self.superficie_rectangle, vermell, ((self.amplada*0.2, self.alçada*0.25), (self.amplada/15, self.alçada/2)))
            pygame.draw.rect(self.superficie_rectangle, vermell, ((self.amplada*0.08, self.alçada*0.25), (self.amplada/3.5, self.alçada/15)))
            pygame.draw.polygon(self.superficie_rectangle, vermell, ( (self.amplada*0.4, self.alçada*0.75),(self.amplada*0.4, self.alçada*0.25), (self.amplada*0.48, self.alçada*0.25), (self.amplada*0.56, self.alçada*0.60), (self.amplada*0.56, self.alçada*0.25), (self.amplada*0.62, self.alçada*0.25), (self.amplada*0.62, self.alçada*0.75), (self.amplada*0.54, self.alçada*0.75), (self.amplada*0.46, self.alçada*0.40), (self.amplada*0.46, self.alçada*0.75)))
            pygame.draw.rect(self.superficie_rectangle, vermell, ((self.amplada*0.77, self.alçada*0.25), (self.amplada/15, self.alçada/2)))
            pygame.draw.rect(self.superficie_rectangle, vermell, ((self.amplada*0.65, self.alçada*0.25), (self.amplada/3.5, self.alçada/15)))
        self.colisionat = False
        if self.movible == False:
            self.color = verd_fosc
            self.color_borde = verd_fosc
            self.superficie_rectangle.fill(verd_fosc)
            for i in range(int(amplada/30)):
                random_x = random.randint(-20, int(amplada)+20)
                random_y = random.randint(-20, int(alçada)+20)
                random_amplada = random.randint(5, 50)/2
                pygame.draw.circle(self.superficie_rectangle, gris,(random_x,random_y,), random_amplada)
        self.rectangle_nou = pygame.transform.rotate(self.superficie_rectangle, self.angle)
        self.rectangle = self.rectangle_nou.get_rect()
        self.rectangle.center = posició
        self.posició_real = posició
        self.mask = pygame.mask.from_surface(self.rectangle_nou)
        self.velocitat_angle = 0
        self.conjut_de_velocitats_1 = []
        self.conjut_de_velocitats_2 = []
        self.vector_centre1 = pygame.math.Vector2(-0.5*amplada+0.5*alçada, 0)
        self.vector_centre2 = pygame.math.Vector2(0.5*amplada-0.5*alçada, 0)
        self.colisionats = []
        self.rotar = True
        self.n = 0
        self.suma_pes = []
        self.rotacions = []
        self.caixa = True
        self.vida = 4
        self.z = 0
        self.pantalla_rect = pantalla.get_rect()
        if self.movible == False:
            if self.tipo == 1:
                self.velocitat_angle = 1
            elif self.tipo == 3:
                self.velocitat_angle = -1
        self.n2 = 0

    def update(self, llista_objectes_pantalla):
        self.n2 +=1
        if self.movible == True and self.caixa:
            if self.z == 1:
                self.z = 0
                self.posició_real = self.rectangle.center
                if self.conjut_de_velocitats_1 != []:
                    self.velocitat*=0    
                    for i in self.conjut_de_velocitats_1:
                        self.velocitat += i
                    self.velocitat /= len(self.conjut_de_velocitats_1)
                    self.conjut_de_velocitats_1.clear()
                if self.conjut_de_velocitats_2 != []:    
                    for i in self.conjut_de_velocitats_2:
                        self.velocitat += i
                    self.conjut_de_velocitats_2.clear()
                if self.rotacions != []:
                    if min(self.rotacions, key = lambda i: i[0])[0] * max(self.rotacions, key = lambda i: i[0])[0] >=0:
                        self.velocitat_angle += max(self.rotacions, key = lambda i: i[1])[0]
                    else:
                        self.velocitat_angle = 0
                    if self.n2%3==0:    
                        self.rotacions.clear()
                if self.velocitat_angle == 0:    
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
                    self.rectangle_orig = self.rectangle.center
                    self.centre_no_rotar_orig = [self.centre_no_rotar[0], self.centre_no_rotar[1],self.centre_no_rotar[2],self.centre_no_rotar[3]]
            if self.angle >= 360:
                self.angle -= 360
            elif self.angle < 0:
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
                self.centre_no_rotar[0] = self.rectangle.center[0] - self.rectangle_orig[0] + self.centre_no_rotar_orig[0]
                self.centre_no_rotar[2] = self.rectangle.center[0] - self.rectangle_orig[0] + self.centre_no_rotar_orig[2]
                self.centre_no_rotar[1] = self.rectangle.center[1] - self.rectangle_orig[1] + self.centre_no_rotar_orig[1]
                self.centre_no_rotar[3] = self.rectangle.center[1] - self.rectangle_orig[1] + self.centre_no_rotar_orig[3]
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
            self.velocitat_angle_ax = self.velocitat_angle
        self.colisionat = False
        if self.caixa == False:
            n=pygame.math.Vector2(1,1)
            for i in self.animació:
                i[0] -= 0.5
                i[1] +=n
                n.rotate_ip(90)
            if self.animació[0][0] <=1:
                llista_objectes_pantalla.remove(self)
        if self.movible == False:
            self.z = 0
            if self.tipo == 3 or self.tipo == 1:    
                self.angle+=self.velocitat_angle
                if self.angle >= 360:
                    self.angle -= 360
                elif self.angle < 0:
                    self.angle += 360
                self.rectangle_nou = pygame.transform.rotate(self.superficie_rectangle, self.angle)
                self.rectangle = self.rectangle_nou.get_rect(center = self.posició_real)
                self.mask = pygame.mask.from_surface(self.rectangle_nou)

    def dibuixar(self, diferencia):
        rectangle = self.rectangle.copy()
        rectangle.topleft+=diferencia  
        if rectangle.colliderect(self.pantalla_rect):    
            if self.caixa: 
                self.pantalla.blit(self.rectangle_nou, rectangle)
            else:
                for i in self.animació:
                    pygame.draw.circle(self.pantalla,self.color_animació,i[1]+diferencia,i[0])
    def calcul_angle_rampa(self, pos):
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
        if abs(y2) < 45 or abs(y2) > 315:
             z = self.angle
        elif abs(y1) < 45 or abs(y1)> 315:
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
    
    def colisió(self, x, llista_objectes_pantalla, llista_objectes_rectangulars):
        self.colisionats.append(x)
        x.colisionats.append(self)
        xesquines_xoc = []
        esquines_xoc = []
        rotar = True
        if self.angle%90 == 0:
            esquina1, esquina2, esquina3, esquina4 = self.rectangle.topleft, self.rectangle.topright, self.rectangle.bottomleft, self.rectangle.bottomright
        else:
            if (self.angle//90)%2==1:
                esquina2, esquina4, esquina1, esquina3 = pygame.math.Vector2(0.5*self.amplada,-0.5*self.alçada).rotate(-self.angle%90) + self.rectangle.center,  pygame.math.Vector2(0.5*self.amplada,0.5*self.alçada).rotate(-self.angle%90) + self.rectangle.center, pygame.math.Vector2(-0.5*self.amplada,-0.5*self.alçada).rotate(-self.angle%90) + self.rectangle.center,  pygame.math.Vector2(-0.5*self.amplada,0.5*self.alçada).rotate(-self.angle%90) + self.rectangle.center
            else:
                esquina2, esquina4, esquina1, esquina3 = pygame.math.Vector2(-0.5*self.amplada,-0.5*self.alçada).rotate(-self.angle%180) + self.rectangle.center,  pygame.math.Vector2(0.5*self.amplada,-0.5*self.alçada).rotate(-self.angle%180) + self.rectangle.center, pygame.math.Vector2(-0.5*self.amplada,0.5*self.alçada).rotate(-self.angle%180) + self.rectangle.center,  pygame.math.Vector2(0.5*self.amplada,0.5*self.alçada).rotate(-self.angle%180) + self.rectangle.center
        esquines = [esquina1,esquina2,esquina3,esquina4]
        if x.angle%90 == 0:
            xesquina1, xesquina2, xesquina3, xesquina4 = x.rectangle.topleft, x.rectangle.topright, x.rectangle.bottomleft, x.rectangle.bottomright
        else:
            if (x.angle//90)%2==1:
                xesquina2, xesquina4, xesquina1, xesquina3 = pygame.math.Vector2(0.5*x.amplada,-0.5*x.alçada).rotate(-x.angle%90) + x.rectangle.center,  pygame.math.Vector2(0.5*x.amplada,0.5*x.alçada).rotate(-x.angle%90) + x.rectangle.center, pygame.math.Vector2(-0.5*x.amplada,-0.5*x.alçada).rotate(-x.angle%90) + x.rectangle.center,  pygame.math.Vector2(-0.5*x.amplada,0.5*x.alçada).rotate(-x.angle%90) + x.rectangle.center
            else:
                xesquina2, xesquina4, xesquina1, xesquina3 = pygame.math.Vector2(-0.5*x.amplada,-0.5*x.alçada).rotate(-x.angle%180) + x.rectangle.center,  pygame.math.Vector2(0.5*x.amplada,-0.5*x.alçada).rotate(-x.angle%180) + x.rectangle.center, pygame.math.Vector2(-0.5*x.amplada,0.5*x.alçada).rotate(-x.angle%180) + x.rectangle.center,  pygame.math.Vector2(0.5*x.amplada,0.5*x.alçada).rotate(-x.angle%180) + x.rectangle.center
        xesquines = [xesquina1,xesquina2,xesquina3,xesquina4]
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
            rampa_x = self
            rampa_s = x
            mask_xoc = self.mask.overlap_mask(x.mask,(x.rectangle.x- self.rectangle.x, x.rectangle.y- self.rectangle.y))        
            rectangle_xoc = mask_xoc.get_bounding_rects()
            posició_xoc = mask_xoc.centroid() + pygame.math.Vector2(self.rectangle.topleft)
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
                        self.rotacions.append((-1,0))
                        self.rotacions.append((1,0))
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
                        x.rotacions.append((-1,0))
                        x.rotacions.append((1,0))
                posició_xoc_s = posició_xoc
                posició_xoc_x = posició_xoc
        elif ns == 1:
            mask_xoc = self.mask.overlap_mask(x.mask,(x.rectangle.x- self.rectangle.x, x.rectangle.y- self.rectangle.y))        
            rectangle_xoc = mask_xoc.get_bounding_rects()
            posició_xoc_x = mask_xoc.centroid() + pygame.math.Vector2(self.rectangle.topleft)
            posició_xoc = posició_xoc_x
        elif nx == 1:
            mask_xoc = self.mask.overlap_mask(x.mask,(x.rectangle.x- self.rectangle.x, x.rectangle.y- self.rectangle.y))        
            rectangle_xoc = mask_xoc.get_bounding_rects()
            posició_xoc_s = mask_xoc.centroid() + pygame.math.Vector2(self.rectangle.topleft)
            posició_xoc = posició_xoc_s
        elif n == 0:
            rampa_s = x
            rampa_x = self
            mask_xoc = self.mask.overlap_mask(x.mask,(x.rectangle.x- self.rectangle.x, x.rectangle.y- self.rectangle.y))        
            rectangle_xoc = mask_xoc.get_bounding_rects()
            posició_xoc_s = rectangle_xoc[0].center + pygame.math.Vector2(self.rectangle.topleft)
            posició_xoc_x = posició_xoc_s
            posició_xoc = posició_xoc_s
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
            esperar = False
            antic_centre = self.rectangle.center
            while self.mask.overlap(x.mask,(x.rectangle.x-self.rectangle.x, x.rectangle.y-self.rectangle.y)):
                self.rectangle.center+=z
            nou_centre = self.rectangle.center
            self.rectangle.center = antic_centre
            for i in llista_objectes_pantalla:
                if i in llista_objectes_rectangulars and i != self:
                    if i not in self.colisionats and i.caixa: 
                        if self.rectangle.colliderect(i.rectangle):    
                            if self.mask.overlap(i.mask,(i.rectangle.x-self.rectangle.x, i.rectangle.y-self.rectangle.y)):
                                self.rectangle.center = nou_centre
                                if not self.mask.overlap(i.mask,(i.rectangle.x-self.rectangle.x, i.rectangle.y-self.rectangle.y)):
                                    esperar = True
                                self.rectangle.center = antic_centre
            if esperar == False:
                self.rectangle.center = nou_centre
            if ns!=2:    
                rotacions(self,x, posició_xoc_s, ns, nx, rectangle_xoc, centre1,centre2,centre3,centre4, esquina1, esquina2, esquina3, esquina4, pygame.math.Vector2(0,0), xesquines_xoc, rotar, antic_centre)
            else:
                self.pivot = (0.5*self.amplada, 0.5*self.alçada)
                self.pivot_pantalla = self.rectangle.center
            if esperar == False:
                if self.rotar == False:    
                    self.centre_no_rotar[0] += nou_centre[0] - antic_centre[0]
                    self.centre_no_rotar[1] += nou_centre[1] - antic_centre[1]
                    self.centre_no_rotar[2] += nou_centre[0] - antic_centre[0]
                    self.centre_no_rotar[3] += nou_centre[1] - antic_centre[1]
            nou_angle_velocitat =180 + 2*self.velocitat.angle_to((-1,0)) - 2*self.angle_rampa
            velocitat.rotate_ip(nou_angle_velocitat)
            velocitat *=0.5
            self.conjut_de_velocitats_1.append(velocitat)
        elif n!= 0:
            for i in x.suma_pes:
                if i[1] == self:
                    x.suma_pes.remove(i)
            xsuma_pes = []
            for i in self.mask.outline(10):
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
            if self.velocitat.length() < gravetat*2:
                self.velocitat*=0
            if x.velocitat.length() < gravetat*2:
                x.velocitat*=0
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
            if x.angle_rampa <= 180:    
                angle_x = 180-x.angle_rampa
            else:
                angle_x = 360-x.angle_rampa + 180
            zx = pygame.math.Vector2.from_polar((1, angle_x))   
            if (diferencia_angle_self > 90 and self.velocitat.length() > 0) or ((diferencia_angle_x <= 90 or x.velocitat.length() == 0) and ((zx[1]>=0 and z[1]>=0) or z[1]<0)):
                if self.velocitat.length() >1.3:    
                    suma_velocitat_per_rotació_x = self.velocitat 
                while self.mask.overlap(x.mask,(x.rectangle.x-self.rectangle.x, x.rectangle.y-self.rectangle.y)):
                    self.rectangle.center+=z
                nou_centre = self.rectangle.center
                self.rectangle.center = antic_centre 
                for i in llista_objectes_pantalla:
                    if i in llista_objectes_rectangulars and i != self:
                        if i not in self.colisionats and i.caixa: 
                            if self.rectangle.colliderect(i.rectangle):    
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
                while self.mask.overlap(x.mask,(x.rectangle.x-self.rectangle.x, x.rectangle.y-self.rectangle.y)):
                    x.rectangle.center+=zx
                nou_centre = x.rectangle.center
                x.rectangle.center = antic_centre_x 
                for i in llista_objectes_pantalla:
                    if i in llista_objectes_rectangulars and i != x:
                        if i not in x.colisionats and i.movible and i.caixa: 
                            if x.rectangle.colliderect(i.rectangle):    
                                if x.mask.overlap(i.mask,(i.rectangle.x-x.rectangle.x, i.rectangle.y-x.rectangle.y)):
                                    x.rectangle.center = nou_centre
                                    if not x.mask.overlap(i.mask,(i.rectangle.x-x.rectangle.x, i.rectangle.y-x.rectangle.y)):
                                        esperarx = True
                                    x.rectangle.center = antic_centre_x
                if esperarx == False:
                    x.rectangle.center = nou_centre
            if diferencia_angle_x > 90 and x.velocitat.length() > 1.3:
                suma_velocitat_per_rotació = x.velocitat
            if ns !=2:    
                rotacions(self,x, posició_xoc_s, ns, nx, rectangle_xoc, centre1,centre2,centre3,centre4, esquina1, esquina2, esquina3, esquina4, suma_velocitat_per_rotació, xesquines_xoc, rotar, antic_centre)
            else:
                self.pivot = (0.5*self.amplada, 0.5*self.alçada)
                self.pivot_pantalla = self.rectangle.center
            if nx!=2:
                rotacions(x, self, posició_xoc_x, nx, ns, rectangle_xoc, xcentre1,xcentre2,xcentre3,xcentre4, xesquina1, xesquina2, xesquina3, xesquina4, suma_velocitat_per_rotació_x, esquines_xoc, rotar, antic_centre_x)  
            else:
                x.pivot = (0.5*x.amplada, 0.5*x.alçada)
                x.pivot_pantalla = x.rectangle.center
            if (diferencia_angle_self > 90 and self.velocitat.length() > 0) or ((diferencia_angle_x <= 90 or x.velocitat.length() == 0)):
                if esperar == False:
                    if self.rotar == False:    
                        self.centre_no_rotar[0] += nou_centre[0] - antic_centre[0]
                        self.centre_no_rotar[1] += nou_centre[1] - antic_centre[1]
                        self.centre_no_rotar[2] += nou_centre[0] - antic_centre[0]
                        self.centre_no_rotar[3] += nou_centre[1] - antic_centre[1]
            else:
                if esperarx == False:
                    if x.rotar == False:    
                        x.centre_no_rotar[0] += nou_centre[0] - antic_centre_x[0] 
                        x.centre_no_rotar[1] += nou_centre[1] - antic_centre_x[1]
                        x.centre_no_rotar[2] += nou_centre[0] - antic_centre_x[0]
                        x.centre_no_rotar[3] += nou_centre[1] - antic_centre_x[1]
            if diferencia_angle_self > 90 and self.velocitat.length() > 0 :    
                nou_angle_velocitat = 180+2*self.velocitat.angle_to((-1,0)) - 2*self.angle_rampa 
                velocitat.rotate_ip(nou_angle_velocitat)
                velocitat *=0.5
                self.conjut_de_velocitats_1.append(velocitat)
            if diferencia_angle_self < 100 and diferencia_angle_x >= 90 and x.velocitat.length() >= 2:
                velocitat*=0
                velocitat += x.velocitat*0.4*x.massa/self.massa
                self.conjut_de_velocitats_2.append(velocitat)
            velocitat2 = x.velocitat.copy()            
            if diferencia_angle_x > 90 and x.velocitat.length() > 0:
                nou_angle_velocitat_2 = 180 + 2*x.velocitat.angle_to((-1,0)) - 2*x.angle_rampa 
                velocitat2.rotate_ip(nou_angle_velocitat_2)
                velocitat2 *=0.5
                x.conjut_de_velocitats_1.append(velocitat2)
            if diferencia_angle_x < 100 and diferencia_angle_self >= 90 and self.velocitat.length() >= 2:
                velocitat2*=0
                velocitat2 += self.velocitat*0.4*self.massa/x.massa
                x.conjut_de_velocitats_2.append(velocitat2)
            self.velocitat_angle = round(self.velocitat_angle,3)
            x.velocitat_angle = round(x.velocitat_angle,3)
            if x.rotar:
                x.pivot = (round(x.pivot[0]), round(x.pivot[1]))
                x.pivot_pantalla = (round(x.pivot_pantalla[0]), round(x.pivot_pantalla[1]))
            if self.rotar:
                self.pivot = (round(self.pivot[0]), round(self.pivot[1]))
                self.pivot_pantalla = (round(self.pivot_pantalla[0]), round(self.pivot_pantalla[1]))
    def destrucció(self, llista_objectes_pantalla, llista_porcs, llista_ocells):
        self.velocitat *= 0
        self.velocitat_angle = 0
        self.colisionats.clear()
        self.conjut_de_velocitats_1.clear()
        self.conjut_de_velocitats_2.clear()
        self.suma_pes.clear()
        self.rotacions.clear()
        if self.tipo == 5:    
            self.color_animació = gris
            for i in llista_objectes_pantalla:
                if i != self:
                    if i in llista_porcs:    
                        if i.porc:    
                            distancia_explosió = pygame.math.Vector2(self.rectangle.center) - i.rectangle.center
                            potencia = 300 - distancia_explosió.length()
                            if potencia >0:
                                potencia += 50
                                if potencia >= 300:
                                    potencia = 300
                                angle = calcul_angle_cercle(self,i.rectangle.center) +180
                                if angle <= 180:    
                                    angle = 180- angle
                                else:
                                    angle = 360-angle + 180
                                i.velocitat += pygame.math.Vector2.from_polar((potencia*50/i.massa, angle))
                    elif i in llista_ocells:    
                        if i.llançat:    
                            distancia_explosió = pygame.math.Vector2(self.rectangle.center) - i.rectangle.center
                            potencia = 300 - distancia_explosió.length()
                            if potencia >0:
                                potencia += 50
                                if potencia >= 300:
                                    potencia = 300
                                angle = calcul_angle_cercle(self,i.rectangle.center)
                                if angle <= 180:    
                                    angle = 180- angle
                                else:
                                    angle = 360-angle +180
                                i.velocitat += pygame.math.Vector2.from_polar((potencia*50/i.massa, angle))
                    else:    
                        if i.caixa and i.movible:    
                            distancia_explosió = pygame.math.Vector2(self.rectangle.center) - i.rectangle.center
                            potencia = 300 - distancia_explosió.length()
                            if potencia >0:
                                if potencia >= 300:
                                    potencia = 300
                                angle = calcul_angle_cercle(self,i.rectangle.center) + 180
                                if angle <= 180:    
                                    angle = 180- angle
                                else:
                                    angle = 360-angle + 180
                                i.velocitat += pygame.math.Vector2.from_polar((potencia*50/i.massa, angle))
                                i.mig_trencat(potencia/75, llista_objectes_pantalla, llista_porcs, llista_ocells)
        else:
            self.color_animació = blanc
        self.caixa = False
        radi = self.massa/100
        if radi > self.amplada/2:
            radi = self.amplada/2
        self.animació = [[radi,self.rectangle.center],[radi,self.rectangle.center],[radi,self.rectangle.center],[radi,self.rectangle.center]]
    def mig_trencat(self, força, llista_objectes_pantalla, llista_porcs, llista_ocells):
        self.vida -= round(força)
        if self.vida <= 0:
            self.destrucció(llista_objectes_pantalla, llista_porcs, llista_ocells)
        elif self.vida <=2:
            self.superficie_rectangle.fill(vermell2)
            if self.amplada < self.alçada:    
                pygame.draw.rect(self.superficie_rectangle, self.color_borde , ((0,0), (self.amplada, self.alçada)), 10 - (100//self.amplada))
            else:
                pygame.draw.rect(self.superficie_rectangle, self.color_borde , ((0,0), (self.amplada, self.alçada)), 10 - (100//self.alçada))
            if self.tipo == 5:
                pygame.draw.rect(self.superficie_rectangle, vermell, ((self.amplada*0.2, self.alçada*0.25), (self.amplada/15, self.alçada/2)))
                pygame.draw.rect(self.superficie_rectangle, vermell, ((self.amplada*0.08, self.alçada*0.25), (self.amplada/3.5, self.alçada/15)))
                pygame.draw.polygon(self.superficie_rectangle, vermell, ( (self.amplada*0.4, self.alçada*0.75),(self.amplada*0.4, self.alçada*0.25), (self.amplada*0.48, self.alçada*0.25), (self.amplada*0.56, self.alçada*0.60), (self.amplada*0.56, self.alçada*0.25), (self.amplada*0.62, self.alçada*0.25), (self.amplada*0.62, self.alçada*0.75), (self.amplada*0.54, self.alçada*0.75), (self.amplada*0.46, self.alçada*0.40), (self.amplada*0.46, self.alçada*0.75)))
                pygame.draw.rect(self.superficie_rectangle, vermell, ((self.amplada*0.77, self.alçada*0.25), (self.amplada/15, self.alçada/2)))
                pygame.draw.rect(self.superficie_rectangle, vermell, ((self.amplada*0.65, self.alçada*0.25), (self.amplada/3.5, self.alçada/15)))
    def copy(self, posició, llista_objectes_rectangulars):
        x = caixa(posició,self.alçada, self.amplada,self.movible,self.angle_inicial, self.tipo, llista_objectes_rectangulars, self.pantalla)
        return x
    def reinici(self):
        self.vida = 4
        self.superficie_rectangle.fill(self.color)
        if self.amplada < self.alçada:    
            pygame.draw.rect(self.superficie_rectangle, self.color_borde , ((0,0), (self.amplada, self.alçada)), 10 - (100//self.amplada))
        else:
            pygame.draw.rect(self.superficie_rectangle, self.color_borde , ((0,0), (self.amplada, self.alçada)), 10 - (100//self.alçada))
        if self.tipo == 5:
            pygame.draw.rect(self.superficie_rectangle, vermell, ((self.amplada*0.2, self.alçada*0.25), (self.amplada/15, self.alçada/2)))
            pygame.draw.rect(self.superficie_rectangle, vermell, ((self.amplada*0.08, self.alçada*0.25), (self.amplada/3.5, self.alçada/15)))
            pygame.draw.polygon(self.superficie_rectangle, vermell, ( (self.amplada*0.4, self.alçada*0.75),(self.amplada*0.4, self.alçada*0.25), (self.amplada*0.48, self.alçada*0.25), (self.amplada*0.56, self.alçada*0.60), (self.amplada*0.56, self.alçada*0.25), (self.amplada*0.62, self.alçada*0.25), (self.amplada*0.62, self.alçada*0.75), (self.amplada*0.54, self.alçada*0.75), (self.amplada*0.46, self.alçada*0.40), (self.amplada*0.46, self.alçada*0.75)))
            pygame.draw.rect(self.superficie_rectangle, vermell, ((self.amplada*0.77, self.alçada*0.25), (self.amplada/15, self.alçada/2)))
            pygame.draw.rect(self.superficie_rectangle, vermell, ((self.amplada*0.65, self.alçada*0.25), (self.amplada/3.5, self.alçada/15)))
        self.velocitat *= 0
        self.angle = self.angle_inicial
        self.rectangle_nou = pygame.transform.rotate(self.superficie_rectangle, self.angle)
        self.rectangle = self.rectangle_nou.get_rect()
        self.rectangle.center = self.posició_inicial 
        self.posició_real = self.posició_inicial
        self.mask = pygame.mask.from_surface(self.rectangle_nou)
        self.x = self.mask.outline(5)
        self.velocitat_angle = 0
        self.colisionats.clear()
        self.conjut_de_velocitats_1.clear()
        self.conjut_de_velocitats_2.clear()
        self.suma_pes.clear()
        self.rotacions.clear()
        self.caixa = True
        self.rotar = True
        self.n = 0
        if self.movible == False:
            if self.tipo == 1:
                self.velocitat_angle = 1
            elif self.tipo == 3:
                self.velocitat_angle = -1
