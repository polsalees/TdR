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
taronja = (255, 165, )
fons = (80, 80, 255)

# Preparar la pantalla
pantalla_amplada, pantalla_alçada = 1920, 1038
pantalla = pygame.display.set_mode((pantalla_amplada, pantalla_alçada))
pygame.display.set_caption("Angry Birds")

# Eines per escriure
font = pygame.font.Font(None, 50)
text = font.render("Hello world!", True, negre)
pantalla.blit(text, (pantalla_amplada // 2 - text.get_width() // 2, pantalla_alçada // 2 - text.get_height() // 2))

# LListes on es troben els objectes en pantalla i els que han estat en algun moment
llista_objectes_pantalla = []
sprites = []

#Creació funcions basiques
def calcular_angle():
    angle = math.degrees(math.atan2(pygame.mouse.get_pos()[0] - 200, pygame.mouse.get_pos()[1] - (pantalla_alçada - 240)))
    return angle

def distancia_ocell_ratoli():
    amplada = math.sqrt(((pygame.mouse.get_pos()[0] - 200) **2 + (pygame.mouse.get_pos()[1] - (pantalla_alçada - 240)) ** 2))
    return amplada

# Creació ocells
class ocells(pygame.sprite.Sprite):
    def __init__(self, radi, color):
        pygame.sprite.Sprite.__init__(self)
        self.radi = radi
        self.posició = [200, pantalla_alçada - 240]
        self.velocitat = [0,0]
        self.potencia = 0
        self.angle = 0
        self.aire = False
        self.color = color
        self.zona = False
        self.frenada = False
        self.llançat = False
        global llista_objectes_pantalla
        self.cooldown = 0
    
    def update(self):     
        self.posició[0] += self.velocitat[0] 
        self.posició[1] += self.velocitat[1]
        if self.aire == True:
            self.velocitat[1] += 0.05
        if self.posició[1] > (pantalla_alçada-self.radi):
            self.velocitat[1] *=-0.25 
            self.posició[1] = pantalla_alçada-self.radi
            if self.velocitat[1] < 0 and self.velocitat[1] > -0.05:
                self.aire = False
                self.velocitat[1] = 0
                self.frenada = True
        elif self.posició[0] > (pantalla_amplada-self.radi):
            self.velocitat[0] *= -0.25
            self.posició[0] = pantalla_amplada-self.radi
        elif self.posició[1] < self.radi:
            self.velocitat[1] = 0
            self.posició[1] = self.radi
        elif self.posició[0] < self.radi:
            self.velocitat[0] *= -0.25
            self.posició[0] = self.radi
        elif self.frenada == True:
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
        if self.llançat == True and self.velocitat == [0,0]:
            self.cooldown += 1
        pygame.draw.circle(pantalla, self.color, self.posició, self.radi)
        if self.cooldown >= 150:     
            llista_objectes_pantalla.remove(self)
   
    def llançament(self):
        self.potencia = distancia_ocell_ratoli() - self.radi
        if self.potencia >= 100:
            self.potencia = 100
        elif self.potencia <= 0:
            self.potencia = 0
        self.angle = math.radians(calcular_angle())
        self.velocitat[0] = -math.sin(self.angle) * self.potencia * 0.1
        self.velocitat[1] = -math.cos(self.angle) * self.potencia * 0.1
        if self.potencia != 0:
            self.aire = True
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
        self.posició = [200, pantalla_alçada - 240]
        self.zona = False
        self.cooldown = 0

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

#Creació ordre d'ocells
def següent_ocell(ocell1, ocell2, ocell3, ocell4, ocell5, ocell6):
    if ocell1.llançat == False:
        if llista_objectes_pantalla.count(ocell1) < 1:
            llista_objectes_pantalla.append(ocell1)
            sprites.append(ocell1)
        x = llista_objectes_pantalla.index(ocell1)
    elif ocell1.llançat == True:
        if ocell2.llançat == False:
            if llista_objectes_pantalla.count(ocell2) < 1:
                llista_objectes_pantalla.append(ocell2)
                sprites.append(ocell2)
            x = llista_objectes_pantalla.index(ocell2)
        elif ocell2.llançat == True:
            if ocell3.llançat == False:
                if llista_objectes_pantalla.count(ocell3) < 1:
                    llista_objectes_pantalla.append(ocell3)
                    sprites.append(ocell3)
                x = llista_objectes_pantalla.index(ocell3)
            elif ocell3.llançat == True:
                if ocell4.llançat == False:
                    if llista_objectes_pantalla.count(ocell4) < 1:
                         llista_objectes_pantalla.append(ocell4)
                         sprites.append(ocell4)
                    x = llista_objectes_pantalla.index(ocell4)
                elif ocell4.llançat == True:
                    if ocell5.llançat == False:
                        if llista_objectes_pantalla.count(ocell5) < 1:
                            llista_objectes_pantalla.append(ocell5)
                            sprites.append(ocell5)
                        x = llista_objectes_pantalla.index(ocell5) 
                    elif ocell5.llançat == True:
                        if ocell6.llançat == False:
                            if llista_objectes_pantalla.count(ocell6) < 1:
                                llista_objectes_pantalla.append(ocell6)
                                sprites.append(ocell6)
                            x = llista_objectes_pantalla.index(ocell6)
                        elif ocell6.llançat == True:
                            if llista_objectes_pantalla.count(no_ocell) < 1:
                                llista_objectes_pantalla.append(no_ocell)
                            x = llista_objectes_pantalla.index(no_ocell)
    return x

# Creació linea ocells
def linea_ocells(ocell1, ocell2, ocell3, ocell4, ocell5, ocell6):
    if ocell1.llançat == False:
        pygame.draw.circle(pantalla, ocell2.color, (180, pantalla_alçada - ocell2.radi), ocell2.radi)
        pygame.draw.circle(pantalla, ocell3.color, (130, pantalla_alçada - ocell3.radi), ocell3.radi)
        pygame.draw.circle(pantalla, ocell4.color, (80, pantalla_alçada - ocell4.radi), ocell4.radi)
        pygame.draw.circle(pantalla, ocell5.color, (30, pantalla_alçada - ocell5.radi), ocell5.radi)
        pygame.draw.circle(pantalla, ocell6.color, (-20, pantalla_alçada - ocell6.radi), ocell6.radi) 
    elif ocell1.llançat == True:
        if ocell2.llançat == False:
            pygame.draw.circle(pantalla, ocell3.color, (180, pantalla_alçada - ocell3.radi), ocell3.radi)
            pygame.draw.circle(pantalla, ocell4.color, (130, pantalla_alçada - ocell4.radi), ocell4.radi)
            pygame.draw.circle(pantalla, ocell5.color, (80, pantalla_alçada - ocell5.radi), ocell5.radi)
            pygame.draw.circle(pantalla, ocell6.color, (30, pantalla_alçada - ocell6.radi), ocell6.radi)
        elif ocell2.llançat == True:
            if ocell3.llançat == False:
                pygame.draw.circle(pantalla, ocell4.color, (180, pantalla_alçada - ocell4.radi), ocell4.radi)
                pygame.draw.circle(pantalla, ocell5.color, (130, pantalla_alçada - ocell5.radi), ocell5.radi)
                pygame.draw.circle(pantalla, ocell6.color, (80, pantalla_alçada - ocell6.radi), ocell6.radi)
            elif ocell3.llançat == True:
                if ocell4.llançat == False:
                    pygame.draw.circle(pantalla, ocell5.color, (180, pantalla_alçada - ocell5.radi), ocell5.radi)
                    pygame.draw.circle(pantalla, ocell6.color, (130, pantalla_alçada - ocell6.radi), ocell6.radi)
                elif ocell4.llançat == True:
                    if ocell5.llançat == False:
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
        self.rect.center = (200, pantalla_alçada - 240)
    def update(self):
        self.superficie_rectangle.fill(fons)
        self.amplada = distancia_ocell_ratoli() 
        pygame.draw.rect(self.superficie_rectangle, blau, pygame.Rect(self.costat/2 - 2.5, self.costat/2 - self.amplada, 5, 1000))
        pygame.draw.rect(self.superficie_rectangle, fons, pygame.Rect(self.costat/2 - 2.5, self.costat/2, 5, 1000))
        self.angle = calcular_angle() + 180 
        self.rectangle_nou = pygame.transform.rotate(self.superficie_rectangle, self.angle)
        self.rect = self.rectangle_nou.get_rect()
        self.rect.center = (200, pantalla_alçada - 240)
        pantalla.blit(self.rectangle_nou, self.rect)

# Creació porcs
def porcs():
    porc_radi = 30
    porc_posició = (pantalla_amplada - porc_radi - 150, pantalla_alçada - porc_radi - 100)
    pygame.draw.circle(pantalla, verd, porc_posició, porc_radi)

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
    sprites = []

# Game GameLoop
def GameLoop():
    zona_ocell = False
    mantenint = False
    mantenint_ocell = False
    partida = False
    nivell = [bombardero, vermellet, racista2, vermellet2, pequeñin, racista]
    while True:
        if not partida:
            reinici()
            if not menú():
                break
            partida = True
        else:
            següent_ocell(nivell[0], nivell[1], nivell[2], nivell[3], nivell[4], nivell[5])
            ocell_actual =  llista_objectes_pantalla[següent_ocell(nivell[0], nivell[1], nivell[2], nivell[3], nivell[4], nivell[5])]
            zona_ocell = ocell_actual.zona_llançament()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    partida = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        partida = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mantenint = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    mantenint = False
                    if mantenint_ocell == True:
                        mantenint_ocell = False
                        ocell_actual.llançament()
            
            #Detectem si estem mantenint l'ocell
            if mantenint == True and zona_ocell == True:
                mantenint_ocell=True

            # Creem una linea que començi desde un punt o altre depenent del ocell que llancem
            line = linea(ocell_actual)
            
            # Netejar la pantalla
            pantalla.fill(fons)
            # Aparèixer porcs, ocells i linea
            if mantenint_ocell:
                line.update()
            porcs()
            for i in  llista_objectes_pantalla:
                i.update()
            linea_ocells(nivell[0], nivell[1], nivell[2], nivell[3], nivell[4], nivell[5])
        # Recarregar la pantalla
        pygame.display.flip()

    # Sortir del joc
    pygame.quit()

# Córrer el joc
GameLoop()
