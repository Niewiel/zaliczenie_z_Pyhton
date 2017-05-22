import pygame, time

# zmienne globalne
okno_otwarte = True
plik = 'statek.png'
plik_obcy = 'obcy.png'
życie = 3
poziom = 1
gra_aktywna = False

# stałe
ROZMIAR = SZEROKOŚĆ, WYSOKOŚĆ = (800, 600)
BIAŁY = pygame.color.THECOLORS['white']
CZARNY = pygame.color.THECOLORS['black']
CIEMNOCZERWONY = pygame.color.THECOLORS['darkred']
JASNONIEBIESKI = pygame.color.THECOLORS['lightblue']
obraz = pygame.image.load(plik)
mini_obraz = pygame.transform.scale(obraz, [obraz.get_rect().width // 3,
                                            obraz.get_rect().height // 3])

# ustawienia okna i gry
pygame.init()

ekran = pygame.display.set_mode(ROZMIAR)
pygame.display.set_caption('Prosta gra.')
zegar = pygame.time.Clock()


class Obcy(pygame.sprite.Sprite):
    def __init__(self, plik_obrazu):
        super().__init__()
        self.image = pygame.image.load(plik_obrazu)
        self.rect = self.image.get_rect()
        self.ruch_x = 1

    def update(self):
        self.rect.x += self.ruch_x

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Statek(pygame.sprite.Sprite):
    def __init__(self, plik_obrazu):
        super().__init__()
        self.image = pygame.image.load(plik_obrazu)
        self.rect = self.image.get_rect()
        self.ruch_x = 0

    def skręt_w_lewo(self):
        self.ruch_x = -6

    def skręt_w_prawo(self):
        self.ruch_x = 6

    def stop(self):
        self.ruch_x = 0

    def strzał(self, pociski):
        if len(pociski) < 4:
            pocisk = Pocisk()
            pocisk.rect.centerx = self.rect.centerx
            pocisk.rect.bottom = self.rect.top
            pociski.add(pocisk)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.x += self.ruch_x
        if self.rect.right > SZEROKOŚĆ:
            self.rect.right = SZEROKOŚĆ
        if self.rect.left < 0:
            self.rect.left = 0

    def obsługa_zdarzeń(self, event, pociski):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.skręt_w_lewo()
            if event.key == pygame.K_d:
                self.skręt_w_prawo()
            if event.key == pygame.K_SPACE:
                self.strzał(pociski)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a and self.ruch_x < 0:
                self.stop()
            if event.key == pygame.K_d and self.ruch_x > 0:
                self.stop()


class Pocisk(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(CIEMNOCZERWONY)
        self.rect = self.image.get_rect()
        self.ruch_y = 7

    def update(self):
        self.rect.y -= self.ruch_y
        if self.rect.bottom < 0:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


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
    def __init__(self, tekst, szerokość, wysokość, kolor_tekstu, kolor_tła):
        self.tekst = tekst
        self.szerokość = szerokość
        self.wysokość = wysokość
        self.kolor_tekstu = kolor_tekstu
        self.kolor_tła = kolor_tła
        self.font = pygame.font.SysFont(None, 60)
        self.rect = pygame.Rect(0, 0, self.szerokość, self.wysokość)
        self.rect.center = [SZEROKOŚĆ / 2, WYSOKOŚĆ / 2]
        self.ustaw()

    def ustaw(self):
        self.image = self.font.render(self.tekst, 1, self.kolor_tekstu, self.kolor_tła)
        self.rect_image = self.image.get_rect()
        self.rect_image.center = self.rect.center

    def draw(self, surface):
        surface.fill(self.kolor_tła, self.rect)
        surface.blit(self.image, self.rect_image)


def stwórz_obcych(statek):
    grupa_obcych = pygame.sprite.Group()
    obcy = Obcy(plik_obcy)
    szerokość = SZEROKOŚĆ - 2 * obcy.rect.width
    liczba_obcych_w_rzędzie = int(szerokość / (2 * obcy.rect.width))
    wysokość = WYSOKOŚĆ - 3 * obcy.rect.height - statek.rect.height
    liczba_obcych_w_kolumnie = int(wysokość / (2 * obcy.rect.height))
    for r in range(liczba_obcych_w_kolumnie):
        for p in range(liczba_obcych_w_rzędzie):
            obcy = Obcy(plik_obcy)
            obcy.rect.x = obcy.rect.width + 2 * obcy.rect.width * p
            obcy.rect.y = obcy.rect.height + 2 * obcy.rect.height * r
            grupa_obcych.add(obcy)

    return grupa_obcych


def restart_gry(ekran, statek):
    global grupa_obcych
    time.sleep(0.5)
    ekran.fill(BIAŁY)
    poziom_tekst = 'POZIOM {} '.format(poziom)


# konkretyzacja obiektów
statek = Statek(plik)
statek.rect.centerx = SZEROKOŚĆ // 2
statek.rect.bottom = WYSOKOŚĆ
grupa_pocisków = pygame.sprite.Group()
grupa_obcych = stwórz_obcych(statek)
obiekt_punkty = Tekst(0, CIEMNOCZERWONY, [SZEROKOŚĆ // 2, 15])

# pętla gry
while okno_otwarte:
    # pętla zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            okno_otwarte = False
        else:
            statek.obsługa_zdarzeń(event, grupa_pocisków)

    ekran.fill(BIAŁY)
    statek.update()
    statek.draw(ekran)
    grupa_pocisków.update()
    for p in grupa_pocisków:
        trafione = pygame.sprite.spritecollide(p, grupa_obcych, True)
        if trafione:
            p.kill()

    grupa_pocisków.draw(ekran)

    # rysowanie i aktualizacja punktów
    for p in grupa_pocisków:
        grupa_trafionych = pygame.sprite.spritecollide(p, grupa_obcych, True)
        for t in grupa_trafionych:
            obiekt_punkty.tekst += 50
            obiekt_punkty.ustaw([SZEROKOŚĆ // 2, 20])

            p.kill()

    obiekt_punkty.draw(ekran)

    # rysowanie żyć
    if życie:
        for i in range(życie):
            ekran.blit(mini_obraz, [40 * i - 40, 15])

    for ob in grupa_obcych:
        if ob.rect.bottom > WYSOKOŚĆ - statek.rect.height:
            życie -= 1
            break

    obiekt_punkty.draw(ekran)

    grupa_obcych.update()
    for ob in grupa_obcych:
        if ob.rect.right > SZEROKOŚĆ or ob.rect.left < 0:
            for ob in grupa_obcych:
                ob.ruch_x *= -1
                ob.image = pygame.transform.flip(ob.image, True, False)
                ob.rect.y += 5
            break

    grupa_obcych.draw(ekran)

    pygame.display.flip()
    zegar.tick(30)

pygame.quit()
