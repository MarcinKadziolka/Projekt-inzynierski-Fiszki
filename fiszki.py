# -*- coding: iso-8859-2 -*- 
import pygame
import sys
import mysql.connector
from math import ceil
from time import sleep


#***********************************************************************#
#                               MYSSQL

# Połaczenie z bazą danych

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="baza_fiszek"
)

mycursor = mydb.cursor()
"""
mycursor.execute("SELECT pytanie, odpowiedz FROM fiszki")

lista_fiszek = mycursor.fetchall()

liczba_elementow = len(lista_fiszek)
"""



#***********************************************************************#
#                               PYGAME I ZMIENNE



# initializing the constructor
pygame.init()
pygame.key.set_repeat(500, 35)

screen_resolution = (720,720)

# opens up a window
screen = pygame.display.set_mode(screen_resolution)

pygame.display.set_caption('Fiszki')

white = (255,255,255)
color_background = (60, 20, 60)
color_light = (170,170,170)
color_dark = (100,100,100)


width = screen.get_width()
height = screen.get_height()



# Ustawienie czcionki
smallfont = pygame.font.SysFont('Corbel',35)


click = False


#***********************************************************************#
#                               FUNKCJE POMOCNICZE



# Tworzy obiekt, prostokąt, którego środek jest o współrzędnych (x, y)
def create_button(x, y, width, height):
   
    button = pygame.Rect(x, y, width, height)

    button.center = (x, y)
        
    return button


def create_buttons(x, starting_y, width, height, liczba_przyciskow, y_skok):
    y = starting_y
    buttons = []
    licznik_przyciskow = 0
    while(licznik_przyciskow < liczba_przyciskow):
        buttons.append(create_button(x, y, width, height))
        licznik_przyciskow += 1
        y += y_skok
    return buttons
        

# Rysuje prostokąt na ekran
def draw_button(button, color):
    pygame.draw.rect(screen, color, button)

# Wpisuje tekst w środek podanego prostokąta
def draw_text_on_button(button, text):
    text_surface_obj = smallfont.render(text, True, white, None)

    text_rect_obj = text_surface_obj.get_rect()

    text_rect_obj.center = button.center

    screen.blit(text_surface_obj, text_rect_obj)

# Wypisuje tekst na ekran, którego środek jest o współrzędnych (x, y)
def draw_text_on_screen(text, x, y):
    text_surface_obj = smallfont.render(text, True, white, None)

    text_rect_obj = text_surface_obj.get_rect()

    text_rect_obj.center = x, y

    screen.blit(text_surface_obj, text_rect_obj)



#***********************************************************************#
#                               FUNCKJE GŁÓWNE

"""
                                WZÓR FUNKCJI

def nazwa():
    
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False                                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        # colors the screen
        screen.fill(color_background)

        pygame.display.update()
"""

# TODO
# [] Ujednolicenie nazewnictwa


# main_menu() - wyświetla menu główne, wykonuje się w nieskończoność, aż do ESCAPE albo kliknięcia X

# tworzenie wszystkich potrzebych przyciskow
fiszki_button = create_button(width/2, 200, 140, 40)        
dodaj_button = create_button(width/2, 250, 140, 40)
edytuj_button = create_button(width/2, 300, 140, 40)
wyjdz_button = create_button(width/2, 350, 140, 40)

def main_menu():
    # TODO
    # [] poruszanie się strzałkami i klawiszami po menu
    # [] podświetlanie przycisków wybranych klawiszami
    while True:
        #print("Main menu")
        
        # Przechowuje pozycje myszy na ekranie
        mouse = pygame.mouse.get_pos()  
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Rejestruje kliknięcie lewego przycisku myszy
                if event.button == 1:
                    click = True


        # colors the screen
        screen.fill(color_background)
               
        draw_button(fiszki_button, color_dark)
        draw_button(dodaj_button, color_dark)
        draw_button(edytuj_button, color_dark)
        draw_button(wyjdz_button, color_dark)
          
        # .collidepoint sprawdza czy podane zmienne nachodzą na dany prostokąt, True/False
        # Jeśli współrzędne myszy nachodzą na przycisk to rysujemy go w innym kolorze
        # Jeśli zostało zarejstrowane kliknięcie i wspołrzędne myszy nachodzą na dany przycisk, to został on kliknięty -> if click:
        # i przechodzimy do odpowiedniej funkcji
        
        if fiszki_button.collidepoint(mouse):
            draw_button(fiszki_button, color_light)
            if click:
                # Najpierw zawsze wyswietlamy kategorie fiszek, ale dla uzytkownika przejrzyciej jest kliknąć przycisk "Fiszki"
                #fiszki()
                kategorie()
                
        if dodaj_button.collidepoint(mouse):
            draw_button(dodaj_button, color_light)
            if click:
                dodaj()
                
        if edytuj_button.collidepoint(mouse):
            draw_button(edytuj_button, color_light)
            if click:
                edytuj()
                
        if wyjdz_button.collidepoint(mouse):
            draw_button(wyjdz_button, color_light)
            if click:
                pygame.quit()
                sys.exit()

        # Wpisuje tekst w dany przycisk
        draw_text_on_button(fiszki_button, "Fiszki")        
        draw_text_on_button(dodaj_button, "Dodaj")
        draw_text_on_button(edytuj_button, "Edytuj")
        draw_text_on_button(wyjdz_button, "Wyjdź")

        pygame.display.update()





# fiszki(id_kategorii) - iteruje po fiszkach z bazy danych

# Iteruje po fiszkach z bazy danych korzystając ze zmiennej globalnej indeks_fiszek
# Przyjmuje id_kategorii, z której ma wyświetlać fiszki (matematyka, polski itp.)
# Kiedy zmienna running == False, pętla się kończy, funkcja się kończy i wraca
# do głównego menu

# Tworzenie potrzebnych przycisków
dobrze_button = create_button(width/2-100, 600, 170, 40)
zle_button = create_button(width/2+100, 600, 170, 40)

def fiszki(id_kategorii):
    # TODO
    # [X] Polskie znaki

    # Aby uniknąć przekazywania w funkcji, zmienne są globalne
    global lista_fiszek
    global liczba_elementow
    global indeks_fiszek
    global ilosc_poprawnych_odpowiedzi
    
    ilosc_poprawnych_odpowiedzi = 0
   
    indeks_fiszek = 0

    # Wykonywanie poleceń SQL
    mycursor.execute("SELECT idfiszki, pytanie, odpowiedz, fk_idkategorie, wyswietlono, odpowiedziano_poprawnie FROM fiszki")

    # Zgarnia wynik mycursor.execute do zmiennej
    lista_fiszek = mycursor.fetchall()

    #lista_fiszek[0][0] - idfiszki
    #lista_fiszek[0][1] - pytanie
    #lista_fiszek[0][2] - odpowiedz
    #lista_fiszek[0][3] - fk_idkategorie
    #lista_fiszek[0][4] - wyswietlono
    #lista_fiszek[0][5] - opowiedziano_poprawnie

    lista_fiszek_z_danej_kategorii = []
    # Kategoria o id 17 == Wszystkie
    # Usuwanie fiszek nie pasujących do kategorii, poprzez kopiowanie i tymczasową listę
    if id_kategorii != 17:
        for fiszka in lista_fiszek:
            if fiszka[3] == id_kategorii:
                lista_fiszek_z_danej_kategorii.append(fiszka)
        lista_fiszek = lista_fiszek_z_danej_kategorii 
   

    liczba_elementow = len(lista_fiszek)

    running = True

    # W sytuacji gdy nie ma fiszek, wyświetlamy odpowiedni komunikat
    # powracamy do wyboru kategorii poprzez running = False
    if liczba_elementow == 0:
        screen.fill(color_background)
        draw_text_on_screen("Nie ma jeszcze fiszek w tej kategorii", width/2, 400)
        pygame.display.update()
        sleep(1.5)
        running = False
    
    while running:
        #print("Fiszki")
        mouse = pygame.mouse.get_pos()  
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    
        # colors the screen
        screen.fill(color_background)


        # Wypisujemy pytanie
        draw_text_on_screen(lista_fiszek[indeks_fiszek][1], width/2, height/2-50)
        
        
        draw_button(odpowiedz_button, color_dark)

        # Jeśli dotarliśmy do końca -> zerujemy indeks
        # Jeśli wciąż są fiszki do wyświetlania -> indeks++
        if odpowiedz_button.collidepoint(mouse):
            draw_button(odpowiedz_button, color_light)
            if click:
                running = odpowiedz()
                """
                if indeks_fiszek+1 == liczba_elementow:
                    indeks_fiszek = 0
                    return podsumowanie()
                    # Usunąć return False, jeśli ma wracać od nowa do wyświetlania fiszek
                else:
                    indeks_fiszek += 1
                return True
                """
        draw_text_on_button(odpowiedz_button, "Odpowiedź")        

        
                     
        pygame.display.update()

# Wyświetla odpowiedź do obecnej fiszki

# Tworzenie potrzebnych przycisków
odpowiedz_button = create_button(width/2, 600, 370, 40)

def odpowiedz():
    global indeks_fiszek
    global ilosc_poprawnych_odpowiedzi

    
    running = True
    while running:
        mouse = pygame.mouse.get_pos()  
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    
        # colors the screen
        screen.fill(color_background)


        # Wyswietla pytanie [indeks][1] i odpowiedz [indeks][2]
        draw_text_on_screen(lista_fiszek[indeks_fiszek][1], width/2, height/2-50)   
        draw_text_on_screen(lista_fiszek[indeks_fiszek][2], width/2, height/2+50)




        # TODO
        # [X] ukonczyc updatowanie licznika wyswietlen

        wyswietlono = lista_fiszek[indeks_fiszek][4]
        id_fiszki = lista_fiszek[indeks_fiszek][0]
        #print("Wyswietlono ", wyswietlono, ", id_fiszki ", id_fiszki)
        ### update_table_wyswietlono
        
        wyswietlono += 1
        mycursor.execute("UPDATE fiszki SET wyswietlono = %s WHERE idfiszki = %s", (wyswietlono, id_fiszki))
        
        mydb.commit()
        # mycursor.execute wymaga tupli jako wartości, stąd -> (id_fiszki,)
        #mycursor.execute("SELECT wyswietlono FROM fiszki WHERE idfiszki = %s", (id_fiszki,))
        
        #wyswietlono = mycursor.fetchall()
        #id_fiszki = lista_fiszek[indeks_fiszek][0]       
        #print("Wyswietlono ", wyswietlono, ", id_fiszki ", id_fiszki, "\n")

        draw_button(dobrze_button, color_dark)
        draw_button(zle_button, color_dark)

        if dobrze_button.collidepoint(mouse):
            draw_button(dobrze_button, color_light)
            if click:
                ### udate_Table = odpowiedziano_poprawnie += 1
                id_fiszki = lista_fiszek[indeks_fiszek][0]
                odpowiedziano_poprawnie = lista_fiszek[indeks_fiszek][5]
                odpowiedziano_poprawnie += 1
                mycursor.execute("UPDATE fiszki SET odpowiedziano_poprawnie = %s WHERE idfiszki = %s", (odpowiedziano_poprawnie, id_fiszki))
                mydb.commit()
                ilosc_poprawnych_odpowiedzi += 1
                

                if indeks_fiszek+1 == liczba_elementow:
                    indeks_fiszek = 0
                    running = podsumowanie()
                    return running
                    
                    # Usunąć return False, jeśli ma wracać od nowa do wyświetlania fiszek
                else:
                    indeks_fiszek += 1
                    
                return True


                
        if zle_button.collidepoint(mouse):
            draw_button(zle_button, color_light)
            if click:
                if indeks_fiszek+1 == liczba_elementow:
                    indeks_fiszek = 0
                    running = podsumowanie()
                    return running
                else:
                    indeks_fiszek += 1
                return True



        draw_text_on_button(dobrze_button, "Dobrze")        
        draw_text_on_button(zle_button, "Źle")



                      
        pygame.display.update()


# Podmenu wyboru kategorii, po której wybraniu uruchamia się funkcja fiszki(id_kategorii)

# Tworzenie 5 przycisków, które służą do wyświetlania kategorii
"""
y = 65
buttons = []
licznik_przyciskow = 0
while(licznik_przyciskow < 5):
    buttons.append(create_button(width/2, y, 680, 80))
    licznik_przyciskow += 1
    y += 90
"""

buttons = []
buttons = create_buttons(width/2, 65, 680, 80, 5, 90)



# Tworzenie przycisków statycznych, korzysta z nich: kategorie(), edytuj()
poprzednia_strona_button = create_button(width/2-100, 600, 170, 40)
nastepna_strona_button = create_button(width/2+100, 600, 170, 40)

def kategorie():
    # TODO
    # 

    """
    # Pobieranie danych z bazy i ustawianie zmiennych
    mycursor.execute("SELECT idfiszki, pytanie, odpowiedz FROM fiszki")
    lista_fiszek = mycursor.fetchall()
    liczba_elementow = len(lista_fiszek)
    licznik_strony = 1
    ilosc_stron = ceil(liczba_elementow / 5)
    indeks_fiszek = 0
    """

    mycursor.execute("SELECT idkategorie, kategoria FROM kategorie")


    lista_kategorii = mycursor.fetchall()
    liczba_elementow = len(lista_kategorii)
    licznik_strony = 1
    ilosc_stron = ceil(liczba_elementow / 5)
    indeks_kategorii = 0 

    
    
    # lista_kategorii[i][0] = idkategorii
    # lista_kategorii[i][1] = idkategorii

    # Główna pętla
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Przestawianie stron strzałkami (zmiana indeksu, sprawdzanie czy indeks nie poza listą)
                if event.key == pygame.K_LEFT:
                    if indeks_kategorii == 0:
                        pass
                    else:
                        indeks_kategorii -= 5
                        licznik_strony -= 1
                if event.key == pygame.K_RIGHT:
                    if indeks_kategorii+5 >= liczba_elementow:
                        pass
                    else:
                        indeks_kategorii += 5
                        licznik_strony += 1
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

                    
        # colors the screen
        screen.fill(color_background)


        # Wypisywanie 5 fiszek na ekran, od indeksu j, do j + 4/5
        # Rysowanie osobno przyciskow, tyle, ile jest fiszek na ekranie
        
        y = 50 # początkowa wysokość
        indeks_kategorii_tmp = indeks_kategorii 
        licznik_kategorii = 0
        
        
        # jeśli nie przekraczamy ilości kategorii i nie przekraczamy 5 kategorii na ekran to rysujemy
        while(indeks_kategorii_tmp < liczba_elementow and licznik_kategorii < 5):
            # Przyciski w kolorze tła
            draw_button(buttons[licznik_kategorii], color_background)
            if buttons[licznik_kategorii].collidepoint(mouse):
                draw_button(buttons[licznik_kategorii], color_dark)
                if click:
                    # Przekazujemy id wybranej kategorii
                    indeks_kategorii_klikniety = indeks_kategorii_tmp
                    print(lista_kategorii[indeks_kategorii_tmp][0])
                    fiszki(lista_kategorii[indeks_kategorii_tmp][0])

            
            draw_text_on_button(buttons[licznik_kategorii], lista_kategorii[indeks_kategorii_tmp][1])

            licznik_kategorii += 1
            indeks_kategorii_tmp += 1
            y += 90 

 
        draw_button(poprzednia_strona_button, color_dark)
        draw_button(nastepna_strona_button, color_dark)
        

        # Zmiana strony poprzez zmianę indeksu kategorii
        # liczenie strony
        # Podświetlanie przycisków
        
        if poprzednia_strona_button.collidepoint(mouse):
            draw_button(poprzednia_strona_button, color_light)
            if click:
                if indeks_kategorii == 0:
                    pass
                else:
                    indeks_kategorii -= 5
                    licznik_strony -= 1
            

        if nastepna_strona_button.collidepoint(mouse):
            draw_button(nastepna_strona_button, color_light)
            if click:
                if indeks_kategorii+5 >= liczba_elementow:
                    pass
                else:
                    indeks_kategorii += 5
                    licznik_strony += 1
                    
        draw_text_on_button(poprzednia_strona_button, "Poprzednia")
        draw_text_on_button(nastepna_strona_button, "Następna")
        

       
        draw_text_on_screen("Strona " + str(licznik_strony) + " / " + str(ilosc_stron), width/2, 660)   
        
     
        pygame.display.update()



class OptionBox():

    def __init__(self, x, y, w, h, color, highlight_color, font, option_list, selected = 0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = 0
        #self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.highlight_color if self.menu_active else self.color, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, white)
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, white)
                surf.blit(msg, msg.get_rect(center = rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        
        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    return self.active_option
        return -1





# create_buttons(x, starting_y, width, height, liczba_przyciskow, y_skok):
buttons_dodaj = []

buttons_dodaj = create_buttons(width/2, 280, 200, 40, 5, 60)

dodaj_fiszke_button = create_button(100, 40, 140, 40)
dodaj_kategorie_button = create_button(100, 100, 140, 40)


def dodaj():
    # TODO
    # [] Postprzątać ten kod w funkcje
    # [X] Przytrzymanie BACKSPACE usuwa kolejne litery
    # [] alt + d itp. wyświetla po prostu literę
    # [] TAB przełącza pola tekstowe


    dodaj_button = create_button(width/2, 600, 140, 40)


    mycursor.execute("SELECT idkategorie, kategoria FROM kategorie")


    lista_kategorii = mycursor.fetchall()
    liczba_elementow = len(lista_kategorii)
    licznik_strony = 1
    ilosc_stron = ceil(liczba_elementow / 5)
    indeks_kategorii = 0
    indeks_kategorii_klikniety = -1


    #print(lista_kategorii[1])

    nazwy_kategorii = []

    tmp = 1
    
    while(tmp < liczba_elementow):
        nazwy_kategorii.append(lista_kategorii[tmp][1])
        tmp += 1
        
    #print(nazwy_kategorii)



    list1 = OptionBox(
    width/2-150, 260, 300, 40, (color_dark), (color_light), smallfont, 
    nazwy_kategorii)



    pytanie = ""
    odpowiedz = ""
    base_font = pygame.font.Font(None, 32)
    odpowiedz_rect = pygame.Rect(200, 200, 140, 32)
    pytanie_rect = pygame.Rect(200, 100, 140, 32)
    color_active = pygame.Color("lightskyblue3")
    color_passive = (255,255,255)
    pytanie_color_text = color_passive

    pytanie_active = False
    odpowiedz_active = False



    zaznaczony = "Fiszka"

    
    running = True
    while running:
        mouse = pygame.mouse.get_pos()  
        #print("dodaj")
        click = False
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if the mouse is clicked on the
                # button the game is terminated
                if event.button == 1:
                    click = True
                if pytanie_rect.collidepoint(event.pos):
                    pytanie_active = True
                else:
                    pytanie_active = False

                if odpowiedz_rect.collidepoint(event.pos):
                    odpowiedz_active = True
                else:
                    odpowiedz_active = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if pytanie_active == True:
                    if event.key == pygame.K_BACKSPACE:
                        pytanie = pytanie[:-1]
                    else:
                        pytanie += event.unicode
                
                if odpowiedz_active == True:
                    if event.key == pygame.K_BACKSPACE:
                        odpowiedz = odpowiedz[:-1]
                    else:
                        odpowiedz += event.unicode

        # colors the screen
        screen.fill(color_background)
        """
        y = 50 # początkowa wysokość
        # Pomijamy kategorię wszystkie dlatego "+ 1"
        indeks_kategorii_tmp = indeks_kategorii + 1
        licznik_kategorii = 0
        

        # jeśli nie przekraczamy ilości kategorii i nie przekraczamy 5 kategorii na ekran to rysujemy
        while(indeks_kategorii_tmp < liczba_elementow and licznik_kategorii < 5):
            # Przyciski w kolorze tła
            if indeks_kategorii_tmp == indeks_kategorii_klikniety:
                draw_button(buttons_dodaj[licznik_kategorii], color_light)
            else:
                draw_button(buttons_dodaj[licznik_kategorii], color_dark)
            if buttons_dodaj[licznik_kategorii].collidepoint(mouse):
                draw_button(buttons_dodaj[licznik_kategorii], color_light)
                if click:
                    print(lista_kategorii[indeks_kategorii_tmp][0])
                    indeks_kategorii_klikniety = indeks_kategorii_tmp


            draw_text_on_button(buttons_dodaj[licznik_kategorii], lista_kategorii[indeks_kategorii_tmp][1])

            licznik_kategorii += 1
            indeks_kategorii_tmp += 1
            y += 90 
        """
        draw_button(dodaj_button, color_dark)
        

        if dodaj_button.collidepoint(mouse):
            draw_button(dodaj_button, color_light)
            if click:
                print(indeks_kategorii_klikniety)
                mycursor.execute("INSERT INTO fiszki (pytanie, odpowiedz, fk_idkategorie) VALUES (%s, %s, %s)", (pytanie, odpowiedz, lista_kategorii[indeks_kategorii_klikniety][0]))
                mydb.commit()
                pytanie = ""
                odpowiedz = ""

        draw_text_on_button(dodaj_button, "Dodaj")


        if odpowiedz_active:
            odpowiedz_color_text = color_active
        else:
            odpowiedz_color_text = color_passive

        if pytanie_active:
            pytanie_color_text = color_active
        else:
            pytanie_color_text = color_passive
       
        pygame.draw.rect(screen, pytanie_color_text, pytanie_rect, 2)
        pytanie_text_surface = base_font.render(pytanie, True, (255,255,255))
        screen.blit(pytanie_text_surface, (pytanie_rect.x + 5, pytanie_rect.y + 5))
        pytanie_rect.w = max(400, pytanie_text_surface.get_width() + 10)

        pygame.draw.rect(screen, odpowiedz_color_text, odpowiedz_rect, 2)
        odpowiedz_text_surface = base_font.render(odpowiedz, True, (255,255,255))
        screen.blit(odpowiedz_text_surface, (odpowiedz_rect.x + 5, odpowiedz_rect.y + 5))
        odpowiedz_rect.w = max(400, pytanie_text_surface.get_width() + 10)




        selected_option = list1.update(event_list)
        if selected_option >= 0:
            print(lista_kategorii[selected_option+1][1])
            indeks_kategorii_klikniety = selected_option + 1

        list1.draw(screen)


        if zaznaczony == "Fiszka":
            draw_button(dodaj_fiszke_button, color_light)
            draw_button(dodaj_kategorie_button, color_dark)
        else:
            draw_button(dodaj_fiszke_button, color_dark)
            draw_button(dodaj_kategorie_button, color_light)

        
        
        

        if dodaj_fiszke_button.collidepoint(mouse):
            draw_button(dodaj_fiszke_button, color_light)
            if click:
                zaznaczony = "Fiszka"
        if dodaj_kategorie_button.collidepoint(mouse):
            draw_button(dodaj_kategorie_button, color_light)
            if click:
                #zaznaczony = "Kategoria"
                dodaj_kategorie()

                print("Wyszedlem z dodaj_kategorie()")
                
                mycursor.execute("SELECT idkategorie, kategoria FROM kategorie")
            

                lista_kategorii = mycursor.fetchall()
                liczba_elementow = len(lista_kategorii)
                licznik_strony = 1
                ilosc_stron = ceil(liczba_elementow / 5)
                indeks_kategorii = 0
                indeks_kategorii_klikniety = -1


                #print(lista_kategorii[1])

                nazwy_kategorii = []

                tmp = 1
                
                while(tmp < liczba_elementow):
                    nazwy_kategorii.append(lista_kategorii[tmp][1])
                    tmp += 1
                    
                list1 = OptionBox(
                    width/2-100, 260, 200, 40, (color_dark), (color_light), smallfont, 
                    nazwy_kategorii)



        draw_text_on_button(dodaj_fiszke_button, "Fiszka")
        draw_text_on_button(dodaj_kategorie_button, "Kategoria")
            
        pygame.display.update()


def dodaj_kategorie():


    dodaj_button = create_button(width/2, 600, 140, 40)
    

    pytanie = ""
    base_font = pygame.font.Font(None, 32)
    pytanie_rect = pygame.Rect(200, 100, 140, 32)
    color_active = pygame.Color("lightskyblue3")
    color_passive = (255,255,255)
    pytanie_color_text = color_passive

    pytanie_active = False

    zaznaczony = "Kategoria"
    
    running = True
    while running:
        mouse = pygame.mouse.get_pos()  
        #print("dodaj")
        click = False
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if the mouse is clicked on the
                # button the game is terminated
                if event.button == 1:
                    click = True
                if pytanie_rect.collidepoint(event.pos):
                    pytanie_active = True
                else:
                    pytanie_active = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if pytanie_active == True:
                    if event.key == pygame.K_BACKSPACE:
                        pytanie = pytanie[:-1]
                    else:
                        pytanie += event.unicode
                
        screen.fill(color_background)


        draw_button(dodaj_button, color_dark)
        

        if dodaj_button.collidepoint(mouse):
            draw_button(dodaj_button, color_light)
            if click:
                print(pytanie)
                mycursor.execute("INSERT INTO kategorie (kategoria) VALUES (%s)", (pytanie, ))
                mydb.commit()
                pytanie = ""

        draw_text_on_button(dodaj_button, "Dodaj")




        if pytanie_active:
            pytanie_color_text = color_active
        else:
            pytanie_color_text = color_passive
       


        pygame.draw.rect(screen, pytanie_color_text, pytanie_rect, 2)
        pytanie_text_surface = base_font.render(pytanie, True, (255,255,255))
        screen.blit(pytanie_text_surface, (pytanie_rect.x + 5, pytanie_rect.y + 5))
        pytanie_rect.w = max(400, pytanie_text_surface.get_width() + 10)


        if zaznaczony == "Fiszka":
            draw_button(dodaj_fiszke_button, color_light)
            draw_button(dodaj_kategorie_button, color_dark)
        else:
            draw_button(dodaj_fiszke_button, color_dark)
            draw_button(dodaj_kategorie_button, color_light)

        
        
        

        if dodaj_fiszke_button.collidepoint(mouse):
            draw_button(dodaj_fiszke_button, color_light)
            if click:
                running = False
        if dodaj_kategorie_button.collidepoint(mouse):
            draw_button(dodaj_kategorie_button, color_light)
            if click:
                zaznaczony = "Kategoria"
            

        draw_text_on_button(dodaj_fiszke_button, "Fiszka")
        draw_text_on_button(dodaj_kategorie_button, "Kategoria")



        pygame.display.update()


# Tworzenie 5 przycisków, które służą do edycji danej fiszki
"""
y = 65
buttons = []
licznik_przyciskow = 0
while(licznik_przyciskow < 5):
    buttons.append(create_button(width/2, y, 600, 80))
    licznik_przyciskow += 1
    y += 90
"""
def edytuj():
    # TODO
    # [X] Zrobić wyświetlanie fiszek tak, aby nie wychodzić poza zakres liczby elementow
    #       [X] Poprawne wyświetlanie w sytuacji, gdy fiszek jest mniej niż 5
    # [X] Zrobić przewijanie stron i warunek, sprawdzajacy czy nie dodamy i poza zakres
    # [X] Sprawdzic dzialnaie funkcji przy wiekszej liczbie fiszek w bazie Mysql
    # [] edycja poszczególnych fiszek
    # [X] licznik strony
    # [X] przycisk do każdej fiszki, który posłuży do przyszłej edycji


    # Pobieranie danych z bazy i ustawianie zmiennych
    mycursor.execute("SELECT idfiszki, pytanie, odpowiedz FROM fiszki")
    lista_fiszek = mycursor.fetchall()
    liczba_elementow = len(lista_fiszek)
    licznik_strony = 1
    ilosc_stron = ceil(liczba_elementow / 5)
    indeks_fiszek = 0 

    # Główna pętla
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_LEFT:
                    if indeks_fiszek == 0:
                        pass
                    else:
                        indeks_fiszek -= 5
                        licznik_strony -= 1
                if event.key == pygame.K_RIGHT:
                    if indeks_fiszek+5 >= liczba_elementow:
                        pass
                    else:
                        indeks_fiszek += 5
                        licznik_strony += 1
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

                    
        # colors the screen
        screen.fill(color_background)


        # Wypisywanie 5 fiszek na ekran, od indeksu j, do j + 4/5
        # Rysowanie osobno przyciskow, tyle, ile jest fiszek na ekranie
        
        y = 50 # początkowa wysokość
        indeks_fiszek_tmp = indeks_fiszek 
        licznik_fiszek = 0  
        while(indeks_fiszek_tmp < liczba_elementow and licznik_fiszek < 5):

            draw_button(buttons[licznik_fiszek], color_background)
            if buttons[licznik_fiszek].collidepoint(mouse):
                draw_button(buttons[licznik_fiszek], color_dark)
                if click:
                    print(indeks_fiszek_tmp)
            # Koordynaty przycisków oraz tekstu na ekranie się pokrywają
            draw_text_on_screen(lista_fiszek[indeks_fiszek_tmp][1], width/2, y)
            draw_text_on_screen(lista_fiszek[indeks_fiszek_tmp][2], width/2, y + 30)

            licznik_fiszek += 1
            indeks_fiszek_tmp += 1
            y += 90 
       
    
        draw_button(poprzednia_strona_button, color_dark)
        draw_button(nastepna_strona_button, color_dark)
        

        # Zmiana strony poprzez zmianę indeksu fiszek
        # Podświetlanie przycisków
        
        if poprzednia_strona_button.collidepoint(mouse):
            draw_button(poprzednia_strona_button, color_light)
            if click:
                if indeks_fiszek == 0:
                    pass
                else:
                    indeks_fiszek -= 5
                    licznik_strony -= 1
            

        if nastepna_strona_button.collidepoint(mouse):
            draw_button(nastepna_strona_button, color_light)
            if click:
                if indeks_fiszek+5 >= liczba_elementow:
                    pass
                else:
                    indeks_fiszek += 5
                    licznik_strony += 1
                    
                    
        draw_text_on_button(poprzednia_strona_button, "Poprzednia")
        draw_text_on_button(nastepna_strona_button, "Następna")
        

       
        draw_text_on_screen("Strona " + str(licznik_strony) + " / " + str(ilosc_stron), width/2, 660)   
             
        pygame.display.update()


powtorz_wszystkie = create_button(width/2, 400, 280, 40)
powtorz_bledne = create_button(width/2, 450, 280, 40)
zakoncz_nauke = create_button(width/2, 500, 280, 40)

def podsumowanie():

    global ilosc_poprawnych_odpowiedzi
    global liczba_elementow
    
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        # colors the screen
        screen.fill(color_background)

        draw_text_on_screen("Odpowiedziałeś poprawnie " + str(ilosc_poprawnych_odpowiedzi)+ " / "  + str(liczba_elementow), width/2, 300)

        draw_button(powtorz_wszystkie, color_dark)
        draw_button(powtorz_bledne, color_dark)
        draw_button(zakoncz_nauke, color_dark)


        if powtorz_wszystkie.collidepoint(mouse):
            draw_button(powtorz_wszystkie, color_light)
            if click:
                ilosc_poprawnych_odpowiedzi = 0
                return True
                
            
        if powtorz_bledne.collidepoint(mouse):
            draw_button(powtorz_bledne, color_light)
            if click:
                ilosc_poprawnych_odpowiedzi = 0
                pass
               
        if zakoncz_nauke.collidepoint(mouse):
            draw_button(zakoncz_nauke, color_light)
            if click:
                ilosc_poprawnych_odpowiedzi = 0
                return False

        draw_text_on_button(powtorz_wszystkie, "Powtórz wszystkie")
        draw_text_on_button(powtorz_bledne, "Powtórz błędne")
        draw_text_on_button(zakoncz_nauke, "Zakończ naukę")
        

        pygame.display.update()


















def test():
    run = True
    while run:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False


        selected_option = list1.update(event_list)
        if selected_option >= 0:
            print(selected_option)

        
        screen.fill((color_background))
        list1.draw(screen)
        pygame.display.flip()
    






#test()
main_menu()
#wynik()
