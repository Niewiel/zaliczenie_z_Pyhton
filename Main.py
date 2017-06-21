import pygame, time

pygame.init()

# STAŁE
ROZMIAR = SZEROKOŚĆ, WYSOKOŚĆ = 800, 600
BIAŁY = pygame.color.THECOLORS['white']
CIEMNOCZERWONY = pygame.color.THECOLORS['darkred']
CIEMNOZIELONY = pygame.color.THECOLORS['darkgreen']
CZARNY = pygame.color.THECOLORS['black']
SZARY = pygame.color.THECOLORS['gray']
plik = 'statek.png'
plik_obcy = 'obcy.png'
obraz = pygame.image.load(plik)
mini_obraz = pygame.transform.scale(obraz, (obraz.get_rect().width // 3,
                                            obraz.get_rect().height // 3))

# zmienne globalne
okno_otwarte = True
życia = 3
poziom = 1
prędkość = 20
start = True
gra_aktywna = False

ekran = pygame.display.set_mode(ROZMIAR)
pygame.display.set_caption('Moja gra...')
zegar = pygame.time.Clock()


class Statek(pygame.sprite.Sprite):
    def __init__(self, plik_obrazu):
        super().__init__()
        self.image = pygame.image.load(plik_obrazu)
        self.rect = self.image.get_rect()
        self.ruch_x = 0

    def skreć_w_lewo(self):
        self.ruch_x = -6

    def skreć_w_prawo(self):
        self.ruch_x = 6

    def stop(self):
        self.ruch_x = 0

    def update(self):
        self.rect.x += self.ruch_x
        if self.rect.right > SZEROKOŚĆ:
            self.rect.right = SZEROKOŚĆ
        if self.rect.left < 0:
            self.rect.left = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def strzał(self, grupa_pocisków):
        if len(grupa_pocisków) < 4:
            pocisk = Pocisk()
            pocisk.rect.centerx = self.rect.centerx
            pocisk.rect.bottom = self.rect.top
            grupa_pocisków.add(pocisk)

    def reakcja_na_zdarzenia(self, event, grupa_pocisków):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.skreć_w_lewo()
            if event.key == pygame.K_d:
                self.skreć_w_prawo()
            if event.key == pygame.K_SPACE:
                self.strzał(grupa_pocisków)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a and self.ruch_x < 0:
                self.stop()
            if event.key == pygame.K_d and self.ruch_x > 0:
                self.stop()


class Obcy(pygame.sprite.Sprite):
    def __init__(self, plik_obrazu, ruch_x=1):
        super().__init__()
        self.image = pygame.image.load(plik_obrazu)
        self.rect = self.image.get_rect()
        self.ruch_x = ruch_x

    def sprawdź_krawędzie_boczne(self):
        if self.rect.left < 0 or self.rect.right > SZEROKOŚĆ:
            return True
        else:
            return False

    def sprawdź_krawędź_dolną(self, statek):
        if self.rect.bottom > WYSOKOŚĆ - statek.rect.height:
            return True
        else:
            return False

    def update(self):
        self.rect.x += self.ruch_x


class Pocisk(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.rect = self.image.get_rect()
        self.ruch_y = 7

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.y -= self.ruch_y
        if self.rect.bottom < 0:
            self.kill()


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


def stwórz_obcych(prędkość=1):
    grupa_obcych = pygame.sprite.Group()
    obcy = Obcy(plik_obcy)
    szerokość = SZEROKOŚĆ - 2 * obcy.rect.width
    liczba_obcych_w_rzędzie = int(szerokość / (2 * obcy.rect.width))
    wysokość = WYSOKOŚĆ - 3 * obcy.rect.height - statek.rect.height
    liczba_rzędów = int(wysokość / (2 * obcy.rect.height))
    for i in range(liczba_rzędów):
        for j in range(liczba_obcych_w_rzędzie):
            obcy = Obcy(plik_obcy, prędkość)
            obcy.rect.x = obcy.rect.width + 2 * obcy.rect.width * j
            obcy.rect.y = obcy.rect.height + 2 * obcy.rect.height * i

            grupa_obcych.add(obcy)

    return grupa_obcych


def reset_planszy(statek, ekran):
    global grupa_obcych
    time.sleep(0.5)
    ekran.fill(BIAŁY)
    obiekt_poziom.tekst = "POZIOM {}".format(poziom)
    obiekt_poziom.ustaw([SZEROKOŚĆ // 2, WYSOKOŚĆ // 2])
    obiekt_poziom.draw(ekran)
    pygame.display.flip()
    time.sleep(0.5)
    grupa_obcych.empty()
    grupa_pocisków.empty()
    grupa_obcych = stwórz_obcych(prędkość)
    statek.rect.centerx = SZEROKOŚĆ // 2
    statek.rect.bottom = WYSOKOŚĆ
    ekran.fill(BIAŁY)
    statek.draw(ekran)
    grupa_obcych.draw(ekran)
    obiekt_punkty.draw(ekran)
    # rysowanie żyć
    if życia:
        for i in range(życia):
            ekran.blit(mini_obraz, [40 * i - 40, 15])

    pygame.display.flip()
    time.sleep(0.5)


# konkretyzacja obiektu
statek = Statek(plik)
statek.rect.centerx = SZEROKOŚĆ // 2
statek.rect.bottom = WYSOKOŚĆ
grupa_pocisków = pygame.sprite.Group()
grupa_obcych = stwórz_obcych(10)
obiekt_punkty = Tekst(0, CIEMNOZIELONY, [SZEROKOŚĆ // 2, 20])
obiekt_poziom = Tekst(0, CZARNY, [SZEROKOŚĆ // 2, WYSOKOŚĆ // 2], 56)
przycisk = Przycisk("START", 300, 100, SZARY, CZARNY)

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
                statek.reakcja_na_zdarzenia(event, grupa_pocisków)

    if gra_aktywna:
        if start:
            reset_planszy(statek, ekran)
            start = False
        ekran.fill(BIAŁY)
        statek.update()
        statek.draw(ekran)
        grupa_pocisków.update()
        grupa_pocisków.draw(ekran)
        grupa_obcych.update()
        for ob in grupa_obcych:
            if ob.sprawdź_krawędzie_boczne():
                for o in grupa_obcych:
                    o.image = pygame.transform.flip(o.image, True, False)
                    o.ruch_x *= -1
                    o.rect.y += 10
                break

        grupa_obcych.draw(ekran)
        # rysowanie i aktualizacja punktów
        for p in grupa_pocisków:
            grupa_trafionych = pygame.sprite.spritecollide(p, grupa_obcych, True)
            for t in grupa_trafionych:
                obiekt_punkty.tekst += 50
                obiekt_punkty.ustaw([SZEROKOŚĆ // 2, 20])

                p.kill()

        obiekt_punkty.draw(ekran)

        # rysowanie żyć
        if życia:
            for i in range(życia):
                ekran.blit(mini_obraz, [40 * i - 40, 15])

        for ob in grupa_obcych:
            if ob.sprawdź_krawędź_dolną(statek):
                życia -= 1
                if życia:
                    reset_planszy(statek, ekran)
                break

        if not życia:
            okno_otwarte = False

        if len(grupa_obcych) == 0:
            poziom += 1
            prędkość += 1
            reset_planszy(statek, ekran)

        pygame.display.flip()
        zegar.tick(30)
    else:
        przycisk.draw(ekran)
        pygame.display.flip()

time.sleep(0.5)
ekran.fill(BIAŁY)
obiekt_poziom.tekst = "KONIEC GRY"
obiekt_poziom.ustaw([SZEROKOŚĆ // 2, WYSOKOŚĆ // 2])
obiekt_poziom.draw(ekran)
pygame.display.flip()
time.sleep(0.5)

pygame.quit()
