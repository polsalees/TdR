import pygame
import math
def calcul_angle_cercle(self, pos):
    vector_angle = pygame.math.Vector2(pos[0]-self.rectangle.center[0], pos[1]-self.rectangle.center[1])
    s = vector_angle.angle_to((-1,0)) + 180
    if s >= 360:
        s -=360
    return s

def colisió_cercles(self,x, llista_ocells, llista_objectes_rectangulars, llista_objectes_rodons, llista_porcs, nombre_porcs, llista_objectes_pantalla):
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
            self.angle_rampa = calcul_angle_cercle(self,x.rectangle.center)
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
                self.velocitat *=0.5
            elif diferencia_angle_x > 90 and x.velocitat.length() >= 2:
                self.velocitat += x.velocitat*0.4
            if diferencia_angle_x > 90 and x.velocitat.length() > 0:
                nou_angle_velocitat_2 = 180 + 2*x.velocitat.angle_to((-1,0)) - 2*x.angle_rampa 
                x.velocitat.rotate_ip(nou_angle_velocitat_2)
                x.velocitat*=0.5 
            elif diferencia_angle_self > 90 and velocitat_inicial.length() >= 2:
                x.velocitat += velocitat_inicial*0.4
    if x in llista_objectes_rectangulars:
        x.colisionats.append(self)
        if self.velocitat.length()*self.massa/x.massa > 4 and x.movible and self in llista_ocells:
            self.velocitat *= 0.4
            if x.tipo == 5:
                self.velocitat*=-1
            x.destrucció(llista_objectes_pantalla, llista_porcs, llista_ocells)
        elif self in llista_porcs and self.velocitat.length()*400>self.massa and x.movible == False:
            nombre_porcs-=1
            self.destrucció()
        elif self in llista_porcs and self.velocitat.length()*300>self.massa and x.movible:
            nombre_porcs-=1
            self.destrucció()
        else:
            if self.velocitat.length()*self.massa/x.massa > 1.5 and x.movible and self in llista_ocells:
                x.mig_trencat(self.velocitat.length()*self.massa/x.massa, llista_objectes_pantalla, llista_porcs, llista_ocells)
            if x.caixa == False:
                self.velocitat *= 0.4
                if x.tipo == 5:
                    self.velocitat*=-1
            else:    
                if x.angle%90 == 0:
                    xesquina1, xesquina2, xesquina3, xesquina4 = x.rectangle.topleft, x.rectangle.topright, x.rectangle.bottomleft, x.rectangle.bottomright
                else:
                    if (x.angle//90)%2==1:
                        xesquina2, xesquina4, xesquina1, xesquina3 = pygame.math.Vector2(0.5*x.amplada,-0.5*x.alçada).rotate(-x.angle%90) + x.rectangle.center,  pygame.math.Vector2(0.5*x.amplada,0.5*x.alçada).rotate(-x.angle%90) + x.rectangle.center, pygame.math.Vector2(-0.5*x.amplada,-0.5*x.alçada).rotate(-x.angle%90) + x.rectangle.center,  pygame.math.Vector2(-0.5*x.amplada,0.5*x.alçada).rotate(-x.angle%90) + x.rectangle.center
                    else:
                        xesquina2, xesquina4, xesquina1, xesquina3 = pygame.math.Vector2(-0.5*x.amplada,-0.5*x.alçada).rotate(-x.angle%180) + x.rectangle.center,  pygame.math.Vector2(0.5*x.amplada,-0.5*x.alçada).rotate(-x.angle%180) + x.rectangle.center, pygame.math.Vector2(-0.5*x.amplada,0.5*x.alçada).rotate(-x.angle%180) + x.rectangle.center,  pygame.math.Vector2(0.5*x.amplada,0.5*x.alçada).rotate(-x.angle%180) + x.rectangle.center
                xesquines = [xesquina1,xesquina2,xesquina3,xesquina4]
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
                    self.angle_rampa = calcul_angle_cercle(self,posició_xoc)
                else:
                    self.angle_rampa = x.calcul_angle_rampa(posició_xoc)
                    if self.angle_rampa == "no":
                        self.angle_rampa = calcul_angle_cercle(self,posició_xoc)
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
                    if diferencia_angle_x > 90 and x.velocitat.length() > 0.1 and self in llista_porcs:
                        if x.velocitat.length()*x.massa/self.massa>4:
                            self.destrucció()
                            x.velocitat *= 0.4
                            nombre_porcs -=1
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
                        if xmeitat1 > xmeitat2:
                            x.rotar = True
                            if n != 0:    
                                if abs(xcentre4[2].length() - 0.5*x.amplada) < abs(xcentre4[2].length() - 0.5*x.alçada):
                                    xvelocitat_angle = -abs((x.velocitat[1]) * xmeitat1*0.5)/xtotal
                                else:
                                    xvelocitat_angle = -abs((x.velocitat[1]) * xmeitat1*0.5*x.alçada)/(xtotal*x.amplada)
                            else:
                                if abs(xcolisió_centre[2].length() - 0.5*x.amplada) < abs(xcolisió_centre[2].length() - 0.5*x.alçada):
                                    xvelocitat_angle = -abs((x.velocitat[1]) * xmeitat1*0.5)/xtotal
                                else:
                                    xvelocitat_angle =- abs((x.velocitat[1]) * xmeitat1*0.5*x.alçada)/(xtotal*x.amplada)
                            x.rotacions.append((xvelocitat_angle, round(posició_xoc[1])))
                        elif xmeitat1 < xmeitat2:
                            x.rotar = True
                            if n != 0:    
                                if abs(xcentre4[2].length() - 0.5*x.amplada) < abs(xcentre4[2].length() - 0.5*x.alçada):
                                    xvelocitat_angle = abs((x.velocitat[1]) * xmeitat2*0.5)/xtotal
                                else:
                                    xvelocitat_angle = abs((x.velocitat[1]) * xmeitat2*0.5*x.alçada)/(xtotal*x.amplada)
                            else:
                                if abs(xcolisió_centre[2].length() - 0.5*x.amplada) < abs(xcolisió_centre[2].length() - 0.5*x.alçada):
                                    xvelocitat_angle = abs((x.velocitat[1]) * xmeitat2*0.5)/xtotal
                                else:
                                    xvelocitat_angle = abs((x.velocitat[1]) * xmeitat2*0.5*x.alçada)/(xtotal*x.amplada) 
                            x.rotacions.append((xvelocitat_angle, round(posició_xoc[1])))
                    velocitat = self.velocitat.copy()
                    if diferencia_angle_self > 90 and self.velocitat.length() > 0 :    
                        nou_angle_velocitat = 180+2*self.velocitat.angle_to((-1,0)) - 2*self.angle_rampa 
                        self.velocitat.rotate_ip(nou_angle_velocitat)
                        self.velocitat *=0.5 
                    if diferencia_angle_self < 100 and diferencia_angle_x >= 90 and x.velocitat.length() >= 2:
                        self.velocitat += x.velocitat*0.4 *x.massa/self.massa
                    velocitat2 = x.velocitat.copy()           
                    if diferencia_angle_x > 90 and x.velocitat.length() > 0:
                        nou_angle_velocitat_2 = 180 + 2*x.velocitat.angle_to((-1,0)) - 2*x.angle_rampa 
                        velocitat2.rotate_ip(nou_angle_velocitat_2)
                        velocitat2 *=0.3
                        x.conjut_de_velocitats_1.append(velocitat2)
                    if diferencia_angle_x < 100 and diferencia_angle_self >= 90 and velocitat.length() >= 2 :
                        velocitat2*=0
                        velocitat2 += velocitat*0.4*self.massa/x.massa
                        x.conjut_de_velocitats_2.append(velocitat2) 
                    if x.rotar:
                        x.pivot = (round(x.pivot[0]), round(x.pivot[1]))
                        x.pivot_pantalla = (round(x.pivot_pantalla[0]), round(x.pivot_pantalla[1]))
    return nombre_porcs