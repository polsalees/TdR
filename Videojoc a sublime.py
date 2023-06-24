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
fons = (80, 80, 255)

# Preparar la pantalla
pantalla_amplada, pantalla_alçada = 1920, 1038
pantalla = pygame.display.set_mode((pantalla_amplada, pantalla_alçada))
pygame.display.set_caption("Angry Birds")

# Eines per escriure
font = pygame.font.Font(None, 50)
text = font.render("Hello world!", True, negre)
pantalla.blit(text, (pantalla_amplada // 2 - text.get_width() // 2, pantalla_alçada // 2 - text.get_height() // 2))

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
   
    def update(self):     
        self.posició[0] += self.velocitat[0] 
        self.posició[1] += self.velocitat[1]
        if self.aire == True:
            self.velocitat[1] += 0.05
        if self.posició[1] > (pantalla_alçada-self.radi):
            self.velocitat[1] *=-0.25 
            self.posició[1] = pantalla_alçada-self.radi
            if self.velocitat[1] < 0 and self.velocitat[1] > -0.5:
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
                self.velocitat[0] -= 0.01
                if self.velocitat[0] <= 0.01:
                    self.velocitat[0] = 0
                    self.frenada = False
            elif self.velocitat[0] < 0:
                self.velocitat[0] += 0.01
                if self.velocitat[0] >= -0.01:
                    self.velocitat[0] = 0
                    self.frenada = False  
        pygame.draw.circle(pantalla, self.color, self.posició, self.radi)
    def llançament(self):
        if self.llançat == False:
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

# Ocells creats
vermellet = ocells(20, vermell)
bombardero = ocells(30, negre)
pequeñin = ocells(10, cian)
racista = ocells(20, groc)
no_ocell = ocells(0, fons)
llista_ocell = []

#Creació ordre d'ocells
def ordre_ocell():
    if vermellet.llançat == False:
        if llista_ocell.count(vermellet) < 1:
            llista_ocell.append(vermellet)
        x = 0
    elif vermellet.llançat == True:
        if bombardero.llançat == False:
            if llista_ocell.count(bombardero) < 1:
                llista_ocell.append(bombardero)
            x = 1
        elif bombardero.llançat == True:
            if pequeñin.llançat == False:
                if llista_ocell.count(pequeñin) < 1:
                    llista_ocell.append(pequeñin)
                x = 2
            elif pequeñin.llançat == True:
                if racista.llançat == False:
                    if llista_ocell.count(racista) < 1:
                         llista_ocell.append(racista)
                    x = 3
                elif racista.llançat == True:
                    if llista_ocell.count(no_ocell) < 1:
                        llista_ocell.append(no_ocell)
                    x = 4
    return x
# Variables linea
superficie_rectangle = pygame.Surface((200, 200))
superficie_rectangle.set_colorkey(fons)
superficie = superficie_rectangle.copy()
superficie.set_colorkey(fons)
rect = superficie.get_rect()
rect.center = (200, pantalla_alçada - 240)

# Creació linea que indica direcció ocell
class linea(pygame.sprite.Sprite):
    def update(self):
        superficie_rectangle.fill(fons)
        amplada = distancia_ocell_ratoli() 
        pygame.draw.rect(superficie_rectangle, blau, pygame.Rect(100 - amplada, 100, 1000, 5))
        pygame.draw.rect(superficie_rectangle, fons, pygame.Rect(100, 100, 100, 5))
        angle = calcular_angle() + 87.5
        rectangle_nou = pygame.transform.rotate(superficie_rectangle, angle)
        rect = rectangle_nou.get_rect()
        rect.center = (200, pantalla_alçada - 240)
        pantalla.blit(rectangle_nou, rect)

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
    global llista_ocell
    for i in llista_ocell:
                i.reinici()
    llista_ocell = []
# Game GameLoop
def GameLoop():
    zona_ocell = False
    mantenint = False
    mantenint_ocell = False
    partida = False
    line = linea()
    while True:
        if not partida:
            reinici()
            if not menú():
                break
            partida = True
        else:
            zona_ocell = llista_ocell[ordre_ocell()].zona_llançament()
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
                        llista_ocell[ordre_ocell()].llançament()
            
            #Detectem si estem mantenint l'ocell
            if mantenint == True and zona_ocell == True:
                mantenint_ocell=True
        
            # Netejar la pantalla
            pantalla.fill(fons)
        
            # Aparèixer porcs, ocells i linea
            if mantenint_ocell:
                line.update()
            porcs()
            for i in llista_ocell:
                i.update()
        # Recarregar la pantalla
        pygame.display.flip()

    # Sortir del joc
    pygame.quit()

# Córrer el joc
GameLoop()