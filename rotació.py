import pygame
import math
def rotacions(self,x, posició_xoc_s, ns, nx, rectangle_xoc, centre1,centre2,centre3,centre4, esquina1, esquina2, esquina3, esquina4, suma_velocitat_per_rotació, xesquines_xoc, rotar, antic_centre):    
    esquines = [esquina1, esquina2, esquina3, esquina4]
    centres = [centre1,centre2,centre3,centre4]
    posició_xoc_s_2 = posició_xoc_s - pygame.math.Vector2(antic_centre)
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
        if colisió_centre==0:
            colisió = True
        if nx == 2 and vector_colisió.length() < rectangle_xoc[0].width*0.5:
            vector_colisió *= 0
        if colisió == False:    
            if self.rotar:
                if vector_colisió.length()>=2:
                    if abs(colisió_centre[2].angle_to((-1,0)) - vector_colisió.angle_to((-1,0))) <  abs(vector_negatiu.angle_to((-1,0)) - vector_colisió.angle_to((-1,0))):
                        self.velocitat_angle += vector_colisió.length()*(abs(suma_velocitat_per_rotació.length()*math.sin(math.radians(colisió_centre[2].angle_to((-1,0)) - suma_velocitat_per_rotació.angle_to((-1,0))))*x.massa/self.massa))/(0.5*self.amplada)
                    else:
                        self.velocitat_angle -= vector_colisió.length()*(abs(suma_velocitat_per_rotació.length()*math.sin(math.radians(colisió_centre[2].angle_to((-1,0)) - suma_velocitat_per_rotació.angle_to((-1,0))))*x.massa/self.massa))/(0.5*self.amplada)
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
                    self.velocitat_angle += vector_colisió.length()*(abs(suma_velocitat_per_rotació.length()*math.sin(math.radians(colisió_centre[2].angle_to((-1,0)) - suma_velocitat_per_rotació.angle_to((-1,0))))*x.massa/self.massa))/(0.5*self.amplada)
                else:
                    self.velocitat_angle -= vector_colisió.length()*(abs(suma_velocitat_per_rotació.length()*math.sin(math.radians(colisió_centre[2].angle_to((-1,0)) - suma_velocitat_per_rotació.angle_to((-1,0))))*x.massa/self.massa))/(0.5*self.amplada)
    if rotar == False or self.velocitat.length()>=3 or self.velocitat_angle>=1:
        self.pivot_pantalla = self.rectangle.center
        self.pivot = (0.5*self.amplada, self.alçada*0.5)
    else:
        self.pivot_pantalla = posició_xoc_s_2 + self.rectangle.center
        self.pivot =(posició_xoc_s_2.rotate(self.angle) + antic_centre) - pygame.math.Vector2(antic_centre[0]-0.5*self.amplada, antic_centre[1]-0.5*self.alçada)
    if round(x.angle)%90 != round(self.angle)%90 or (nx!=0 and ns ==0) or (nx == 1 and ns == 1 and ((rectangle_xoc[0].width < self.amplada/2))):    
        if (self.angle%90 == 0 and colisió_centre == centre3) or (self.angle%90!=0 and (colisió_centre == centre3 or colisió_centre == centre4)) or posició_xoc_s == esquina4 or (posició_xoc_s == esquina3 and self.angle%90 > 45) or (posició_xoc_s == esquina2 and self.angle%90 < 45):
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
                if meitat1 > meitat2:
                    if meitat2 == 0:
                        meitat2 =1
                    meitat1_orig = meitat1
                    meitat1 += abs(self.velocitat[1])*meitat1/meitat2
                    meitat2 -= abs(self.velocitat[1])*meitat1_orig/meitat2
                elif meitat2 < meitat1:
                    if meitat1 == 0:
                        meitat1 =1
                    meitat2_orig = meitat2
                    meitat2 += abs(self.velocitat[1])*meitat2/meitat1
                    meitat1 -= abs(self.velocitat[1])*meitat2_orig/meitat1
                meitat1_orig = meitat1
                total = meitat2 + meitat3 + meitat1
                if abs(meitat1)> total*1.5:
                    meitat1 = total*1.5
                    meitat2 = -total*0.5
                elif abs(meitat2)> total*1.5:
                    meitat2 = total*1.5
                    meitat1 = -total*0.5
                if self.suma_pes!=[]:  
                    for i in self.suma_pes:
                        for s in i[0]:      
                            s = list(s)
                            s[0] += self.rectangle.left
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
                if meitat1 > meitat2:
                    if meitat2 == 0:
                        meitat2 =1
                    meitat1_orig = meitat1
                    meitat1 += abs(self.velocitat[1])*meitat1/meitat2
                    meitat2 -= abs(self.velocitat[1])*meitat1_orig/meitat2
                elif meitat2 < meitat1:
                    if meitat1 == 0:
                        meitat1 =1
                    meitat2_orig = meitat2
                    meitat2 += abs(self.velocitat[1])*meitat2/meitat1
                    meitat1 -= abs(self.velocitat[1])*meitat2_orig/meitat1
                meitat1_orig = meitat1
                meitat1 += (self.velocitat[0]- self.velocitat_angle_ax)*(meitat2+meitat1) 
                meitat2 -= (self.velocitat[0]- self.velocitat_angle_ax)*(meitat1_orig + meitat2)
                total = meitat2 + meitat3 + meitat1
                if abs(meitat1)> total*1.5:
                    meitat1 = total*1.5
                    meitat2 = -total*0.5
                elif abs(meitat2)> total*1.5:
                    meitat2 = total*1.5
                    meitat1 = -total*0.5
                meitat5-=2
                meitat4 +=1
                if meitat4 > meitat5:
                    if meitat5 == 0:
                        meitat5 =1
                    meitat4_orig = meitat4
                    meitat4 += abs(self.velocitat[1])*meitat4/meitat5
                    meitat5 -= abs(self.velocitat[1])*meitat4_orig/meitat5
                elif meitat5 < meitat4:
                    if meitat4 == 0:
                        meitat4 =1
                    meitat5_orig = meitat5
                    meitat5 += abs(self.velocitat[1])*meitat5/meitat4
                    meitat4 -= abs(self.velocitat[1])*meitat5_orig/meitat4
                meitat4_orig = meitat4
                meitat4 += (self.velocitat[0]- self.velocitat_angle_ax)*(meitat4+meitat5) 
                meitat5 -= (self.velocitat[0]- self.velocitat_angle_ax)*(meitat4_orig + meitat5)
                if abs(meitat4)> total*1.5:
                    meitat4 = total*1.5
                    meitat5 = -total*0.5
                elif abs(meitat5)> total*1.5:
                    meitat5 = total*1.5
                    meitat4 = -total*0.5
                total = meitat2 + meitat3 + meitat1
                if self.suma_pes!=[]:  
                    for i in self.suma_pes:
                        for s in i[0]: 
                            s[0] += self.rectangle.left     
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
            if meitat1 > meitat2:
                self.rotar = True
                self.n = 0
                if posició_xoc_s in esquines:    
                    if abs(centre4[2].length() - 0.5*self.amplada) < abs(centre4[2].length() - 0.5*self.alçada):
                        svelocitat_angle = -abs(meitat1*0.5)/(total*self.amplada/100)
                    else:
                        svelocitat_angle = -abs(meitat1*0.5*self.alçada)/((total)*self.amplada)
                else:
                    if abs(colisió_centre[2].length() - 0.5*self.amplada) < abs(colisió_centre[2].length() - 0.5*self.alçada):
                        svelocitat_angle = -abs(meitat1*0.5)/(total*self.amplada/70)
                    else:
                        svelocitat_angle = -abs(meitat1*0.5*self.alçada)/((total)*self.amplada)
                self.rotacions.append((svelocitat_angle*2, round(posició_xoc_s[1])))
                if len(self.rotacions)>1:
                    if min(self.rotacions, key = lambda i: i[0])[0] * max(self.rotacions, key = lambda i: i[0])[0] <0:
                        self.velocitat_angle = 0
                        self.rotar = False
                        if self.angle%90 == 0: 
                            self.centre_no_rotar = [centre3[0], centre3[1], centre1[0], centre1[1]]
                        elif posició_xoc_s in esquines:
                            if self.angle%90 <= 45:
                                self.centre_no_rotar = [centre4[0], centre4[1], centre2[0], centre2[1]]
                            else:
                                self.centre_no_rotar = [centre3[0], centre3[1], centre1[0], centre1[1]]
                        else:
                            colisió_centre_2 = (pygame.math.Vector2(colisió_centre[0],colisió_centre[1]) - antic_centre).rotate(180) + antic_centre
                            self.centre_no_rotar = [colisió_centre[0], colisió_centre[1], colisió_centre_2[0], colisió_centre_2[1]]
                        self.suma_pes.clear()    
            elif meitat1 < meitat2:
                self.rotar = True
                self.n = 0
                if posició_xoc_s in esquines:    
                    if abs(centre3[2].length() - 0.5*self.amplada) < abs(centre3[2].length() - 0.5*self.alçada):
                        svelocitat_angle = abs(meitat2*0.5)/(total*self.amplada/70)
                    else:
                        svelocitat_angle = abs(meitat2*0.5*self.alçada)/((total)*self.amplada)
                else:
                    if abs(colisió_centre[2].length() - 0.5*self.amplada) < abs(colisió_centre[2].length() - 0.5*self.alçada):
                        svelocitat_angle = abs(meitat2*0.5)/(total*self.amplada/70)
                    else:
                        svelocitat_angle = abs(meitat2*0.5*self.alçada)/((total)*self.amplada)
                self.rotacions.append((svelocitat_angle*2, round(posició_xoc_s[1])))
                if len(self.rotacions)>1:
                    if min(self.rotacions, key = lambda i: i[0])[0] * max(self.rotacions, key = lambda i: i[0])[0] <0:
                        self.velocitat_angle = 0
                        self.rotar = False
                        if self.angle%90 == 0: 
                            self.centre_no_rotar = [centre3[0], centre3[1], centre1[0], centre1[1]]
                        elif posició_xoc_s in esquines:
                            if self.angle%90 <= 45:
                                self.centre_no_rotar = [centre4[0], centre4[1], centre2[0], centre2[1]]
                            else:
                                self.centre_no_rotar = [centre3[0], centre3[1], centre1[0], centre1[1]]
                        else:
                            colisió_centre_2 = (pygame.math.Vector2(colisió_centre[0],colisió_centre[1]) - antic_centre).rotate(180) + antic_centre
                            self.centre_no_rotar = [colisió_centre[0], colisió_centre[1], colisió_centre_2[0], colisió_centre_2[1]]
                        self.suma_pes.clear()    
    elif self.rotar:
        self.angle = round(self.angle)
        self.velocitat_angle = 0
        self.rotar = False
        if posició_xoc_s in esquines or colisió == True:
            if self.angle%90 == 0: 
                self.centre_no_rotar = [centre3[0], centre3[1], centre1[0], centre1[1]]
            elif self.angle%90 <= 45:
                self.centre_no_rotar = [centre4[0], centre4[1], centre2[0], centre2[1]]
            else:
                self.centre_no_rotar = [centre3[0], centre3[1], centre1[0], centre1[1]]
        else:
            colisió_centre_2 = (pygame.math.Vector2(colisió_centre[0],colisió_centre[1]) - antic_centre).rotate(180) + antic_centre
            self.centre_no_rotar = [colisió_centre[0], colisió_centre[1], colisió_centre_2.x, colisió_centre_2.y] 
        self.rotacions.append((-1,0))
        self.rotacions.append((1,0))
        self.suma_pes.clear()
    if self.rotar:
        self.pivot = (round(self.pivot[0]), round(self.pivot[1]))
        self.pivot_pantalla = (round(self.pivot_pantalla[0]), round(self.pivot_pantalla[1]))