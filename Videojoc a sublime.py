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
pantalla_amplada, pantalla_alçada = 1000, 600
pantalla = pygame.display.set_mode((pantalla_amplada, pantalla_alçada))
pygame.display.set_caption("Angry Birds")

# Eines per escriure
font = pygame.font.Font(None, 50)
text = font.render("Hello world!", True, negre)
pantalla.blit(text, (pantalla_amplada // 2 - text.get_width() // 2, pantalla_alçada // 2 - text.get_height() // 2))

# Creació ocells
class ocells(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ocell_radi = 20
        self.ocell_posició = [100, pantalla_alçada - self.ocell_radi - 100]
        self.velocitat = [0,0]
        self.potencia = 0
        self.angle = 0
        self.aire = False

    def update(self):     
        self.ocell_posició[0] += self.velocitat[0] 
        self.ocell_posició[1] += self.velocitat[1]
        if self.aire == True:
            self.velocitat[1] += 0.05
        pygame.draw.circle(pantalla, vermell, self.ocell_posició, self.ocell_radi)
        if self.ocell_posició[1]>1000:
            self.aire = False
            self.velocitat = [0,0]
            self.ocell_posició = [100, pantalla_alçada - self.ocell_radi - 100]
    def llançament(self):
        self.potencia = ((pygame.mouse.get_pos()[0] - 100)**2 + (pygame.mouse.get_pos()[1] - 480) ** 2) ** 0.5
        if self.potencia >= 100:
            self.potencia = 100
        self.angle = math.atan2(pygame.mouse.get_pos()[0] - 100, pygame.mouse.get_pos()[1] - 480)
        self.velocitat[0] = -math.sin(self.angle) * self.potencia * 0.1
        self.velocitat[1] = -math.cos(self.angle) * self.potencia * 0.1
        self.aire = True

# Variables linea
superficie_rectangle = pygame.Surface((200, 200))
superficie_rectangle.set_colorkey(fons)
superficie = superficie_rectangle.copy()
superficie.set_colorkey(fons)
rect = superficie.get_rect()
rect.center = (100, 480)

# Creació linea que indica direcció ocell
class linea(pygame.sprite.Sprite):
   
    def __init__(self):
        superficie_rectangle = pygame.Surface((200, 200))
        superficie_rectangle.set_colorkey(fons)
        rect = superficie.get_rect()
        rect.center = (100, pantalla_alçada - 480)
    
    def update(self):
        superficie_rectangle.fill(fons)
        amplada = ((pygame.mouse.get_pos()[0] - 100) **2 + (pygame.mouse.get_pos()[1] - 480) ** 2) ** 0.5 
        pygame.draw.rect(superficie_rectangle, blau, pygame.Rect(100 - amplada, 100, 1000, 5))
        pygame.draw.rect(superficie_rectangle, fons, pygame.Rect(100, 100, 100, 5))
        angle = math.degrees(math.atan2(pygame.mouse.get_pos()[0] - 100, pygame.mouse.get_pos()[1] - 480)) + 87.5
        rectangle_nou = pygame.transform.rotate(superficie_rectangle, angle)
        rect = rectangle_nou.get_rect()
        rect.center = (100, 480)
        pantalla.blit(rectangle_nou, rect)

# Creació porcs
def porcs():
    porc_radi = 30
    porc_posició = (pantalla_amplada - porc_radi - 100, pantalla_alçada - porc_radi - 10)
    pygame.draw.circle(pantalla, verd, porc_posició, porc_radi)

# Selecció de nivell
def selecció_nivell():
    nivell_seleccionat = None
    while not nivell_seleccionat:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    nivell_seleccionat = 1
                elif event.key == pygame.K_2:
                    nivell_seleccionat = 2
                elif event.key == pygame.K_3:
                    nivell_seleccionat = 3
                elif event.key == pygame.K_4:
                    nivell_seleccionat = 4
                elif event.key == pygame.K_5:
                    nivell_seleccionat = 5
                elif event.key == pygame.K_6:
                    nivell_seleccionat = 6
                elif event.key == pygame.K_7:
                    nivell_seleccionat = 7
                elif event.key == pygame.K_8:
                    nivell_seleccionat = 8
                elif event.key == pygame.K_9:
                    nivell_seleccionat = 9
        
        pantalla.fill(fons)
        
        font = pygame.font.Font(None, 100)
        text1 = font.render("Seleccionar nivell:", True, taronja)
        text2 = font.render("1", True, taronja)
        text3 = font.render("2", True, taronja)
        text4 = font.render("3", True, taronja)
        text5 = font.render("4", True, taronja)
        text6 = font.render("5", True, taronja)
        text7 = font.render("6", True, taronja)
        text8 = font.render("7", True, taronja)
        text9 = font.render("8", True, taronja)
        text10 = font.render("9", True, taronja)
        text11= font.render("10", True, taronja)
        text12 = font.render("11", True, taronja)
        text13 = font.render("12", True, taronja)

        pantalla.blit(text1, (pantalla_amplada // 2 - text1.get_width() // 2, pantalla_alçada // 5 - text1.get_height() // 2 ))
        pantalla.blit(text2, (pantalla_amplada // 5 - text2.get_width() // 2, pantalla_alçada * 2 // 5 - text2.get_height() // 2 ))
        pantalla.blit(text3, (pantalla_amplada * 2 // 5 - text3.get_width() // 2, pantalla_alçada * 2 // 5 - text3.get_height() // 2 ))
        pantalla.blit(text4, (pantalla_amplada * 3 // 5 - text4.get_width() // 2, pantalla_alçada * 2 // 5 - text4.get_height() // 2 ))
        pantalla.blit(text5, (pantalla_amplada * 4 // 5 - text5.get_width() // 2, pantalla_alçada * 2 // 5 - text5.get_height() // 2 ))
        pantalla.blit(text6, (pantalla_amplada // 5 - text6.get_width() // 2, pantalla_alçada * 3 // 5 - text6.get_height() // 2 ))
        pantalla.blit(text7, (pantalla_amplada * 2 // 5 - text7.get_width() // 2, pantalla_alçada * 3 // 5 - text7.get_height() // 2 ))
        pantalla.blit(text8, (pantalla_amplada * 3 // 5 - text8.get_width() // 2, pantalla_alçada * 3 // 5 - text8.get_height() // 2 ))
        pantalla.blit(text9, (pantalla_amplada * 4 // 5 - text9.get_width() // 2, pantalla_alçada * 3 // 5 - text9.get_height() // 2 ))
        pantalla.blit(text10, (pantalla_amplada // 5 - text10.get_width() // 2, pantalla_alçada * 4 // 5 - text10.get_height() // 2 ))
        pantalla.blit(text11, (pantalla_amplada * 2 // 5 - text11.get_width() // 2, pantalla_alçada * 4 // 5 - text11.get_height() // 2 ))
        pantalla.blit(text12, (pantalla_amplada * 3 // 5 - text12.get_width() // 2, pantalla_alçada * 4 // 5 - text12.get_height() // 2 ))
        pantalla.blit(text13, (pantalla_amplada * 4 // 5 - text13.get_width() // 2, pantalla_alçada * 4 // 5 - text13.get_height() // 2 ))

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

# Game GameLoop
def GameLoop():
    mantenint = False
    mantenint_ocell = False
    partida = False
    line = linea()
    vermellet = ocells()
    while True:
        if not partida:
            if not menú():
                break
            partida = True
        else:
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
                        vermellet.llançament()
            #Detectem si estem mantenint l'ocell
            if mantenint == True and pygame.mouse.get_pos()[1]>460 and pygame.mouse.get_pos()[1]<500 and pygame.mouse.get_pos()[0]>80 and pygame.mouse.get_pos()[0]<120:
                mantenint_ocell=True
        
            # Netejar la pantalla
            pantalla.fill(fons)
        
            # Aparèixer porcs, ocells i linea
            if mantenint_ocell:
                line.update()
            porcs()
            vermellet.update()

        # Recarregar la pantalla
        pygame.display.flip()

    # Sortir del joc
    pygame.quit()

# Córrer el joc
GameLoop()
