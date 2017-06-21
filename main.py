import pygame, time
import random

pygame.init()
SZEROKOŚĆ = 800
WYSOKOŚĆ = 600
ROZMIAR = [SZEROKOŚĆ, WYSOKOŚĆ]

# kolory
JASNONIEBIESKI = pygame.color.THECOLORS['lightblue']
BIAŁY = pygame.color.THECOLORS['white']
CIEMNOCZERWONY = pygame.color.THECOLORS['darkred']
CIEMNOZIELONY = pygame.color.THECOLORS['darkgreen']
CZARNY = pygame.color.THECOLORS['black']
SZARY = pygame.color.THECOLORS['gray']

# zmienne globalne
ekran = pygame.display.set_mode(ROZMIAR)
pygame.display.set_caption('zabij obcego')
okno_otwarte = True
start = True
gra_aktywna = False
zegar = pygame.time.Clock()
tree1 = pygame.image.load('tree.png')
plik_obcy = pygame.image.load('obcy.png')
BONUS = pygame.image.load('bonus.png')
muzyka=pygame.mixer.Sound('alien_music.wav')

down1 = pygame.image.load('a1.png')
down2 = pygame.image.load('a2.png')
down3 = pygame.image.load('a3.png')
down4 = pygame.image.load('a4.png')

up1 = pygame.image.load('d1.png')
up2 = pygame.image.load('d2.png')
up3 = pygame.image.load('d3.png')
up4 = pygame.image.load('d4.png')

left1 = pygame.image.load('b1.png')
left2 = pygame.image.load('b2.png')
left3 = pygame.image.load('b3.png')
left4 = pygame.image.load('b4.png')

right1 = pygame.image.load('c1.png')
right2 = pygame.image.load('c2.png')
right3 = pygame.image.load('c3.png')
right4 = pygame.image.load('c4.png')

plik = 'życie.png'
obraz = pygame.image.load(plik)
mini_obraz = pygame.transform.scale(obraz, (obraz.get_rect().width // 3,
                                            obraz.get_rect().height // 3))

mini_bonus = pygame.transform.scale(BONUS, (BONUS.get_rect().width // 3,
                                            BONUS.get_rect().height // 3))


# klasy
class Gracz(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = down1
        self.rect = self.image.get_rect()
        self.ruch_x = 0
        self.ruch_y = 0
        self.licznik = 0
        self.prędkość = 2

        self.lvl = 1
        self.życie = self.lvl * 5
        self.trafione = 0

    def lewo(self):
        self.ruch_x = -self.prędkość

    def prawo(self):
        self.ruch_x = self.prędkość

    def góra(self):
        self.ruch_y = -self.prędkość

    def dół(self):
        self.ruch_y = self.prędkość

    def stopx(self):
        self.ruch_x = 0
        self.image = down1

    def stopy(self):
        self.ruch_y = 0
        self.image = down1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):

        self.rect.x += self.ruch_x
        self.rect.y += self.ruch_y

        if self.ruch_x > 0 and self.ruch_y == 0:
            self.__move(right1, right2, right3, right4)
        if self.ruch_x < 0 and self.ruch_y == 0:
            self.__move(left1, left2, left3, left4)
        if self.ruch_y > 0:
            self.__move(down2, down3, down4, down1)
        if self.ruch_y < 0:
            self.__move(up1, up2, up3, up4)

    def __move(self, obraz1, obraz2, obraz3, obraz4):
        if self.licznik < 5:
            self.image = obraz1
        elif self.licznik < 10:
            self.image = obraz2
        elif self.licznik < 15:
            self.image = obraz3
        elif self.licznik < 20:
            self.image = obraz4

        if self.licznik >= 20:
            self.licznik = 0
        else:
            self.licznik += 1

    def obsługa_zdarzeń(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.dół()
            if event.key == pygame.K_w:
                self.góra()
            if event.key == pygame.K_d:
                self.prawo()
            if event.key == pygame.K_a:
                self.lewo()
            if event.key == pygame.K_SPACE:
                self.image = down1



        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s and self.ruch_y > 0:
                self.stopy()
            if event.key == pygame.K_w and self.ruch_y < 0:
                self.stopy()
            if event.key == pygame.K_d and self.ruch_x > 0:
                self.stopx()
            if event.key == pygame.K_a and self.ruch_x < 0:
                self.stopx()
            if event.key == pygame.K_SPACE:
                self.atak()

    def atak(self):
        for i in grupa_obcych:
            if pygame.sprite.spritecollide(self, grupa_obcych, True):
                gracz.trafione += 1
        for j in grupa_bonusów:
            j.właściwość=random.randint(0,30)
            if pygame.sprite.spritecollide(self, grupa_bonusów, True):
                if j.właściwość < 10:
                    pass

                elif (j.właściwość > 10) and (j.właściwość < 20):
                    for b in grupa_obcych:
                        b.ruch = 0

                elif (j.właściwość > 20) and (j.właściwość < 30):
                    self.prędkość += 10
                else:
                    pass



class Potwór(pygame.sprite.Sprite):
    def __init__(self, plik_obrazu, życie=1, ruch=1):
        super().__init__()
        self.image = pygame.image.load('obcy.png')
        self.rect = self.image.get_rect()
        self.życie = życie
        self.ruch = ruch

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.x += self.ruch
        if self.życie == 0:
            self.kill()

    def sprawdź_krawędzie_boczne(self):
        if self.rect.left > SZEROKOŚĆ:
            return True
        else:
            return False


class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.właściwość = 0
        self.image = mini_bonus
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        random.randint(0, 500)
        # self.rect.x = random.randint(10, 700)
        # self.rect.y = random.randint(120, 500)


class Tekst:
    def __init__(self, tekst, kolor_tekstu, położenie, rozmiar=42):
        self.tekst = tekst
        self.kolor_tekstu = kolor_tekstu
        self.położenie = położenie
        self.font = pygame.font.SysFont(None, rozmiar)
        self.ustaw(położenie)

    def ustaw(self, położenie):
        self.image = self.font.render(str(self.tekst), 1, self.kolor_tekstu)
        self.rect = self.image.get_rect()
        self.rect.center = położenie

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Przycisk:
    def __init__(self, tekst, szerokość, wysokość, kolor_tła, kolor_tekstu):
        self.tekst = tekst
        self.szerokość = szerokość
        self.wysokość = wysokość
        self.kolor_tła = kolor_tła
        self.kolor_tekstu = kolor_tekstu
        self.font = pygame.font.SysFont(None, 60)
        self.rect = pygame.Rect(0, 0, self.szerokość, self.wysokość)
        self.rect.center = [SZEROKOŚĆ // 2, WYSOKOŚĆ // 2]
        self.ustaw()

    def ustaw(self):
        self.image = self.font.render(self.tekst,
                                      1, self.kolor_tekstu, self.kolor_tła)
        self.rect_image = self.image.get_rect()
        self.rect_image.center = self.rect.center

    def draw(self, surface):
        surface.fill(self.kolor_tła, self.rect)
        surface.blit(self.image, self.rect_image)


def stwórz_obcych(lvl=1):
    grupa_obcych = pygame.sprite.Group()
    # obcy = Potwór(plik_obcy)
    liczba_potworów = lvl
    for i in range(liczba_potworów):
        obcy = Potwór(plik_obcy, lvl * 10, lvl // 2)
        obcy.rect.x = random.randint(10, 700)
        obcy.rect.y = random.randint(120, 500)
        for j in grupa_obcych:
            if obcy.rect.x == j.rect.x or obcy.rect.y == j.rect.y:
                obcy.rect.x = random.randint(10, 700)
                obcy.rect.y = random.randint(120, 500)

        grupa_obcych.add(obcy)

    return grupa_obcych


def stwórz_bonus(lvl):
    grupa_bonusów = pygame.sprite.Group()
    for i in range(lvl):
        bonus = Bonus()
        bonus.rect.x = random.randint(10, 700)
        bonus.rect.y = random.randint(120, 500)
        grupa_bonusów.add(bonus)
    return grupa_bonusów


def reset_planszy(gracz, ekran):
    global grupa_obcych
    global grupa_bonusów
    pygame.mixer.Sound.stop(muzyka)
    pygame.mixer.Sound.play(muzyka)

    time.sleep(0.5)
    ekran.fill(BIAŁY)
    pygame.display.flip()
    time.sleep(0.5)
    grupa_obcych.empty()
    grupa_bonusów.empty()
    gracz.trafione = 0
    grupa_obcych = stwórz_obcych(gracz.lvl)
    grupa_bonusów = stwórz_bonus(1)
    gracz.prędkość=2

    gracz.rect.x = SZEROKOŚĆ - 100
    gracz.rect.y = WYSOKOŚĆ // 2 - gracz.image.get_rect().height
    gracz.draw(ekran)

    obiekt_punkty.tekst = gracz.lvl
    grupa_obcych.draw(ekran)
    grupa_bonusów.draw(ekran)
    pygame.display.flip()
    time.sleep(0.5)


# konkretyzacja obiektów
gracz = Gracz()
gracz.rect.center = ekran.get_rect().center
grupa_obcych = stwórz_obcych(10)
grupa_bonusów = stwórz_bonus(1)

obiekt_punkty = Tekst(gracz.lvl, CIEMNOZIELONY, [SZEROKOŚĆ // 2, 20])
obiekt_poziom = Tekst("aby zabić potwora podejdź do niego i wciśnij spację", CZARNY, [SZEROKOŚĆ // 2, WYSOKOŚĆ // 2],
                      56)
obiekt_instrukcja = Tekst("aby zabić potwora lub podnieść bonus podejdź do niego i wciśnij spację", CZARNY, [SZEROKOŚĆ // 2, 60], 30)

przycisk = Przycisk("START ", 300, 100, SZARY, CZARNY)
pygame.mixer.Sound.play(muzyka)

# pętla gry
while okno_otwarte:
    # pętla zdarzeń

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            okno_otwarte = False
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if przycisk.rect.collidepoint(pygame.mouse.get_pos()):
                    gra_aktywna = True
                    pygame.mouse.set_visible(False)
            else:
                gracz.obsługa_zdarzeń(event)
    if gra_aktywna:
        if start:
            reset_planszy(gracz, ekran)
            start = False

        for ob in grupa_obcych:
            if ob.sprawdź_krawędzie_boczne():
                for o in grupa_obcych:
                    o.kill()
                    gracz.życie -= 1

                    break
                break
        grupa_obcych.draw(ekran)
        grupa_obcych.update()
        grupa_bonusów.draw(ekran)
        grupa_bonusów.update()
        obiekt_punkty.ustaw([SZEROKOŚĆ // 2, 20])
        obiekt_punkty.draw(ekran)
        gracz.update()
        gracz.draw(ekran)

        # rysowanie żyć
        if gracz.życie:
            for i in range(gracz.życie):
                ekran.blit(mini_obraz, [40 * i, 15])

        if not gracz.życie:
            okno_otwarte = False

        if len(grupa_obcych) == 0:
            if gracz.życie > 0:
                gracz.lvl += 1
                if gracz.życie <= 20:
                    gracz.życie += 1
            pygame.mixer.Sound.stop(muzyka)
            reset_planszy(gracz, ekran)

        pygame.display.flip()
        ekran.fill(BIAŁY)
        zegar.tick(30)
    else:
        ekran.fill(BIAŁY)
        przycisk.draw(ekran)
        obiekt_instrukcja.draw(ekran)

        pygame.display.flip()

time.sleep(0.5)
ekran.fill(BIAŁY)
obiekt_poziom.tekst = "KONIEC GRY"
obiekt_poziom.ustaw([SZEROKOŚĆ // 2, WYSOKOŚĆ // 2])
obiekt_poziom.draw(ekran)
pygame.display.flip()
time.sleep(0.5)
pygame.quit()
