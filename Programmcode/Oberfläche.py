#Oberflaeche.py

'Import der benoetigten Bibliotheken'
import pygame 
import sys 
import subprocess
import pickle
import os
import pandas as pd
import time

'Import der benoetigten weiteren Programmcodes'
import GrafikSetup


'Zuerst werden generelle Initialisierungen vorgenommen und ggfs. alte Daten geloescht'

#Zunächst erfolgen generelle Festlegungen auf die an spaeterer Stelle referenziert
#werden kann. Dabei werden die Farben mit einem RGB-Code festgelegt und die Fenstergroesse
#mit der Laenge in X- und Y-Richtung
color_passive = (224,255,240)
color_active  = (255,246,143)
black         = (  0,  0,  0)
window_size   = [1400, 950]

#Falls es bereits einen Durchlauf gab, sollen die alten Grafiken geloescht werden
try:
    os.remove('graphic/Best.png')
    os.remove('graphic/Convergence.png')
    os.remove('graphic/Greedy.png')
    os.remove('graphic/Iteration.png')
    os.remove('graphic/Net.png')
    os.remove('graphic/ORTools.png')
except FileNotFoundError:
    pass

#Pygame-Initialisierung, um die Grafikbibliothek zu verwenden und das Fenster mit
#den geforderten Abmessungen zu erstellen
pygame.init() 
screen = pygame.display.set_mode(window_size) 

#Die Schriftgröße wird festgelegt
font = pygame.font.Font(None, 35)

'In diesem Abschnitt erfolgt die Initialisierung der GUI. Dazu zählt die Positionierung'
'und Dimensionierung der einzelnen Bestandteile sowie die Beschriftung'

#Die Felder, in welche die Beschriftungen für die einzelnen Kategorien eingefügt werden,
#werden definiert:  pygame.Rect(x-Position, y-Position, Breite, Höhe)
width = 175
height = 50
field_ants        = pygame.Rect( 25, 50,width,height)
field_evaporation = pygame.Rect( 25,125,width,height)
field_iterations  = pygame.Rect( 25,200,width,height)
field_alpha       = pygame.Rect(375, 50,width,height)
field_beta        = pygame.Rect(375,125,width,height)
field_cities      = pygame.Rect(375,200,width,height)

#Alles wird in einer Liste gespeichert um dies in einem df speichern zu können.
#Dadurch kann die while-Schleife an spätere Stelle übersichtlicher gehalten werden.
Fields            = [field_ants, field_evaporation, field_iterations, field_alpha, 
                     field_beta, field_cities]
df                = pd.DataFrame()
df['Fields']      = Fields

#Wie zuvor werden nun für die Felder in welche später die Parameterwerte eingetragen
#werden die Abmessungen festgelegt und anschließend dem df hinzugefügt.
width = 150
input_field_ants        = pygame.Rect(200, 50,width,height)
input_field_evaporation = pygame.Rect(200,125,width,height)
input_field_iterations  = pygame.Rect(200,200,width,height)
input_field_alpha       = pygame.Rect(550, 50,width,height)
input_field_beta        = pygame.Rect(550,125,width,height)
input_field_cities      = pygame.Rect(550,200,width,height)

Input_Fields            = [input_field_ants, input_field_evaporation, input_field_iterations, input_field_alpha,
                           input_field_beta, input_field_cities]
df['Input Fields']      = Input_Fields

#Die Beschriftungen werden in schwarzer Schriftfarbe erstellt und ebenfalls dem 
#df hinzugefuegt. 'True' sorgt fuer eine Erhoehung der Darstellungsqualitaet.
label_ants        = font.render('Ameisen',        True, black)
label_evaporation = font.render('Verdunstung', True, black)
label_iterations  = font.render('Iterationen', True, black)
label_alpha       = font.render('Alpha',       True, black)
label_beta        = font.render('Beta',        True, black)
label_cities      = font.render('Städte',      True, black)

Labels            = [label_ants, label_evaporation, label_iterations, label_alpha, label_beta,
                     label_cities]
df['Labels']      = Labels

#Damit die Felder zu Beginn nicht leer sind werden die Parameter auf bestimmte Werte
#initialisiert.
ants        =  '10'
evaporation = '  0.02'
iterations  = '500'
alpha       =   '1'
beta        =   '2'
cities      =  '20'

Names       = ['ants', 'evaporation', 'iterations', 'alpha', 'beta', 'cities']
String      = [ants, evaporation, iterations, alpha, beta, cities]

Input       = []
for i in range(len(String)):
    #Alle Werte werden formatiert und angehaengt
    Input.append(font.render(String[i], True, black))

#Das DataFrame wird um die entsprechenden Werte erweitert
df['String'] = String
df['Input']  = Input
df['Names']  = Names

Assignment = []
Color      = []
Logic      = []

#Fuer alle Felder werden weitere Daten angehaengt.
for i in range(len(df)):
    label = df.loc[i, 'Labels']
    field = df.loc[i, 'Fields']
    #Die Zuweisung zwischen den Beschriftungen (Label) und den Feldern erfolgt
    assignment = label.get_rect(center=field.center)
    Assignment.append(assignment)
    #Alle Felder werden zunaechst mit der Farbe "passiv" initalisiert
    Color.append(color_passive)
    #Ausserdem werden sie auf "False" (=nicht ausgewaehlt) initialisiert
    Logic.append(False)
    
df['Assignment'] = Assignment
df['Color']      = Color
df['Logic']      = Logic


#Im folgenden werden die verschiedenen Buttons initalisiert. Dies erfolgt immer gleich:
#Zunaechst werden Masse und Position und die Farbe festgelegt. Danach wird der Text
#formatiert und schliesslich dem Feld zugewiesen.

#Definierung des Start-Buttons
start_rect          = pygame.Rect(25, 325, 250, 100)
start_color         = (69, 139, 0)
start_text          = font.render("Start", True, (0, 0, 0))
text_rect_start     = start_text.get_rect(center=start_rect.center)
#Definierung des Einstellungen-Buttons
settings_rect       = pygame.Rect(375, 325, 250, 100)
settings_color      = (100, 100, 100)
settings_text       = font.render("Einstellungen", True, (0, 0, 0))
text_rect_settings  = settings_text.get_rect(center=settings_rect.center)

#Im folgenden handelt es sich um die Buttons, welche zum Umschalten der Grafiken
#benoetigt werden

#Definierung des Buttons für die Grafik 'Iteration'
iteration_rect      = pygame.Rect(1100, 425, 200, 25)
iteration_color     = color_passive
iteration_text      = font.render("Iteration", True, (0, 0, 0))
text_rect_iteration = iteration_text.get_rect(center=iteration_rect.center)
#Definierung des Buttons für die Grafik 'Netz'
net_rect            = pygame.Rect(800, 425, 200, 25)
net_color           = color_active
net_text            = font.render("Netz", True, (0, 0, 0))
text_rect_net       = net_text.get_rect(center=net_rect.center)
#Definierung des Buttons für die Grafik 'MMAS'
best_rect           = pygame.Rect(800, 900, 150, 25)
best_color          = color_active
best_text           = font.render("MMAS", True, (0, 0, 0))
text_rect_best      = best_text.get_rect(center=best_rect.center)
#Definierung des Buttons für die Grafik 'Greedy'
greedy_rect         = pygame.Rect(1000, 900, 150, 25)
greedy_color        = color_passive
greedy_text         = font.render("Greedy", True, (0, 0, 0))
text_rect_greedy    = greedy_text.get_rect(center=greedy_rect.center)
#Definierung des Buttons für die Grafik 'OR-Tools'
simplex_rect        = pygame.Rect(1200, 900, 150, 25)
simplex_color       = color_passive
simplex_text        = font.render("OR-Tools", True, (0, 0, 0))
text_rect_simplex   = simplex_text.get_rect(center=simplex_rect.center)

#Die Button erhalten zudem eine logische Komponente, um zu wissen, ob sie aktiv
#sind/ geklickt wurden 
button_iteration_active = False
button_net_active       = True #Wird standardmaessig zuerst angezeigt
button_best_active      = True #Wird standardmaessig zuerst angezeigt
button_greedy_active    = False
button_simplex_active   = False
button_start_active     = False
button_settings_active  = False

'Die Standardwerte fuer die Einstellungen werden gesetzt und gespeichert.' 
'Falls nicht explizit die Werte geaendert werden, werden diese verwendet.'
pause         = '0'
with open('pickle/pause.pkl', 'wb') as file:
    pickle.dump(pause, file)
plotRate      = '10'
with open('pickle/plotRate.pkl', 'wb') as file:
    pickle.dump(plotRate, file)
stopCriteria  = '999999'
with open('pickle/stopCriteria.pkl', 'wb') as file:
    pickle.dump(stopCriteria, file)
    
#Fensternamen festlegen
pygame.display.set_caption("Scientific Computing II - Knak und Landwehr")


'Die Funktion sorgt für die Auswahl der richtigen Anzahl an Städten oder der geforderten'
'Instanz. Sie wird aufgerufen, nachdem der Start-Button geklickt wurde.'
def SelectCities():
    #Die Vorlage mit allen Staedten wird geladen
    df = pd.read_excel('Staedte_Vorlage.xlsx').set_index('City')
    #Die Anzahl an auszuwaehlenden Staedten/ der Hexadezimalcode wird geladen
    with open('pickle/cities.pkl', 'rb') as file:
        x = str(pickle.load(file))
    
    if len(x) == 8: #if Code hexadezimal
        cities       = df.index.tolist()
        Cities       = []
        hex_value    = str(x)
        #Der Hexadezimalcode wird fuer die Anzeige gespeichert
        with open('pickle/hex.pkl', 'wb') as file:
            pickle.dump(hex_value, file)
        #Umwandeln des Hexadezimalcodes in Binaercode
        hex_list = [hexd for hexd in hex_value]
        binary_string = ''
        for x in hex_list:
            #Umwandeln und loeschen der (unnoetigen) fuehrenden Zeichen
            binary = str(bin(int(x, 16))[2:])
            #Eine Hexadezimalzahl muss vier Binaerstellen codieren
            while len(binary) < 4:
                binary = '0' + binary
            binary_string += binary
        #Aus dem String wird eine Liste gemacht
        binary_list = [int(binary) for binary in binary_string]
        for i in range(len(binary_list)):
            #Falls die Position mit einer 1 codiert ist, wird die Stadt ausgewaehlt
            if binary_list[i] == 1:
                Cities.append(cities[i])
        #Ein neues df mit den ausgewaehlten Staedten wird erstellt und gespeichert
        new = df.loc[Cities]
        
    else: #Code binaer
        #Falls x >32, wird x auf 32 gesetzt
        x         = min(int(x), len(df))
        #Es werden zufaellig x Staedte ausgewaehlt
        new       = df.sample(n=x)
        City_list = df.index.tolist()
        Binary    = ''
        #Alle Staedte werden mit 1 (ausgewaehlt) oder 0 (nicht-ausgewaehlt) codiert
        #und in eine Hexadezimalzahl umgewandelt, um diesen in den Grafiken anzeigen
        #zu koennen
        for city in City_list:
            if city in new.index.tolist():
                Binary += str(1)
            else:
                Binary += str(0)
        hex_value = hex(int(Binary, 2))
        hex_value = hex_value[2:]
        #Der Hexadezimalcode wird gespeichert
        with open('pickle/hex.pkl', 'wb') as file:
            pickle.dump(hex_value, file)
        
    #Die neue Auswahl wird gespeichert
    new.to_excel('Staedte_Auswahl.xlsx')

'Innerhalb der while-Schleife wird die eigentliche GUI programmiert'
while True: 
    
    #Falls der Button geklickt wurde, wird die Farbe nach 0.25s zurueckgesetzt.
    #Dies sorgt fuer ein optisches Feedback in der GUI.
    if button_start_active == True:
        time.sleep(0.25)
        start_color = (69, 139, 0)
        button_start_active = False
        
    if button_settings_active == True:
        time.sleep(0.25)
        settings_color = (100, 100, 100)
        button_settings_active = False
    
    #Alle moeglichen Events (Tastaturanschlag,Klicken, ...) werden durchgegangen
    for event in pygame.event.get():   
        #Uebprueft ob das Fenster geschlossen wird
        if event.type == pygame.QUIT: 
            #Die Subprozesse werden beendet
            try:
                process_Greedy.terminate()
                process_ORTools.terminate()
                process_MMAS.terminate()
                process_Settings.terminate()
            except NameError:
                pass
            #Das Fenster wird geschlossen
            pygame.quit() 
            sys.exit() 
            
        'Falls mit der Maus geklickt wurde'
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            #An dieser Stelle wird geregelt was geschieht wenn der Start-Button
            #geklickt wurde
            if start_rect.collidepoint(event.pos):
                #Zuerst werden die Werte aller Parameter gespeichert
                for i in range(len(df)):
                    path = 'pickle/' + df.loc[i, 'Names'] + '.pkl'
                    with open(path, 'wb') as file:
                        pickle.dump(df.loc[i, 'String'], file)
                #Anschließend werden die Staedte ausgewaehlt/ die Instanz geladen.
                #Falls es einen ValueError gibt, also ein ungueltiges Format uebergeben
                #wurde, so wird das Fenster geschlossen. Ansonsten wuerde sich das 
                #Programm aufhaengen.
                try:
                    SelectCities()
                except ValueError:
                    pygame.quit() 
                    sys.exit() 
                #Die Subprozesse werden gestartet. Nachdem diese beendet sind koennen
                #die Ergebnisse in der GUI angezeigt werden
                process_ORTools = subprocess.Popen(['python', 'ORTools.py'])
                process_Greedy  = subprocess.Popen(['python', 'Greedy.py'])
                process_MMAS     = subprocess.Popen(['python', 'MMAS.py'])
                #Die Farbe des Buttons wird fuer optisches Feedback geaendert
                start_color = (110, 180, 0)
                pygame.draw.rect(screen, start_color, start_rect)
                screen.blit(start_text, text_rect_start)
                button_start_active = True
        
            #Falls ein Feld fuer die Parameterangabe angeklickt wurde, wird die
            #Farbe geandert und ueber True auf aktiv gesetzt. Die anderen Felder
            #werden auf passiv gestellt.
            for i in range(len(df)):
                if df.loc[i, 'Input Fields'].collidepoint(event.pos):
                    df.at[i, 'Color'] = color_active
                    df.loc[i, 'Logic'] = True
                else:
                    df.at[i, 'Color'] = color_passive
                    df.loc[i, 'Logic'] = False
            
            #An dieser Stelle wird geregelt was geschieht wenn der Einstellungs-Button'
            #geklickt wurde'
            if settings_rect.collidepoint(event.pos):
                #Die Farbe des Buttons wird fuer optisches Feedback geaendert
                settings_color = (110, 180, 50)
                pygame.draw.rect(screen, settings_color, settings_rect)
                screen.blit(settings_text, text_rect_settings)
                button_settings_active = True
                #Das Fenster fuer die Einstellungen wird geoeffnet
                process_Settings = subprocess.Popen(['python', 'Einstellungen.py'])
            
            'Falls ein bestimmter Button zur Auswahl der Grafiken geklickt wurde,'
            'wird dieser aktiviert und alle anderen Grafiken (der gleichen Ebene)'
            'auf passiv gesetzt'
            #Grafik letzte Iteration'
            if iteration_rect.collidepoint(event.pos):
                iteration_color = color_active
                button_iteration_active = True
                net_color = color_passive
                button_net_active = False
            #Grafik Netz
            if net_rect.collidepoint(event.pos):
                net_color = color_active
                button_net_active = True
                iteration_color = color_passive
                button_iteration_active = False                            
            #Grafik beste gefundene Loesung'
            if best_rect.collidepoint(event.pos):
                best_color = color_active
                button_best_active = True
                greedy_color = color_passive
                button_greedy_active = False
                simplex_color = color_passive
                button_simplex_active = False
            #Grafik Greedy
            if greedy_rect.collidepoint(event.pos):
                greedy_color = color_active
                button_greedy_active = True
                best_color = color_passive
                button_best_active = False 
                simplex_color = color_passive
                button_simplex_active = False
            #Grafik OR-Tools
            if simplex_rect.collidepoint(event.pos):
                simplex_color = color_active
                button_simplex_active = True
                best_color = color_passive
                button_best_active = False 
                greedy_color = color_passive
                button_greedy_active = False 
                
        'Wird ausgefuehrt falls eine Taste gedrueckt wurde'
        if event.type == pygame.KEYDOWN:
            #Es wird fuer alle Felder geprueft ob ein Feld aktiv ist
            for i in range(len(df)):
                #In dieses aktive Feld wird geschrieben
                if df.loc[i, 'Logic'] == True:
                    #Durch Backspace wird die Eingabe geloescht
                    if event.key == pygame.K_BACKSPACE:
                        df.loc[i, 'String'] = df.loc[i, 'String'][:-1]
                    #Die gedrueckte Taste wird der Eingabe hinzugefuegt
                    else:
                        df.loc[i, 'String'] += event.unicode
                    #Die Eingabe wird formatiert
                    df.loc[i, 'Input'] = font.render(df.loc[i, 'String'], True, black)
                    #Der neue Wert wird gespeichert
                    path = 'pickle/' + df.loc[i, 'Names'] + '.pkl'
                    with open(path, 'wb') as file:
                        pickle.dump(df.loc[i, 'String'], file)
                    
    'Ist der Button aktiviert, so wird die entsprechende Datei geladen (falls'
    'vorhanden)'
    try:
        if button_net_active == True:
            upper_graph = pygame.image.load('graphic/Net.png')
        if button_iteration_active == True:
            upper_graph = pygame.image.load('graphic/Iteration.png')
        if button_best_active == True:
            lower_graph = pygame.image.load('graphic/Best.png')
        if button_greedy_active == True:
            lower_graph = pygame.image.load('graphic/Greedy.png')
        if button_simplex_active == True:
            lower_graph = pygame.image.load('graphic/ORTools.png')
        screen.blit(upper_graph, (700, -55))
        screen.blit(lower_graph, (700, 400))
        konvergenz = pygame.image.load('graphic/Convergence.png')
        screen.blit(konvergenz, (50, 450))
    except FileNotFoundError:
        pass
        
    #Die Buttons fuer die Grafiken werden zusammengefuegt (Rechteck, Farbe und 
    #Text) und angezeigt
    pygame.draw.rect(screen, iteration_color, iteration_rect)
    screen.blit(iteration_text, text_rect_iteration)    
    pygame.draw.rect(screen, net_color, net_rect)
    screen.blit(net_text, text_rect_net)   
    pygame.draw.rect(screen, best_color, best_rect)
    screen.blit(best_text, text_rect_best)    
    pygame.draw.rect(screen, greedy_color, greedy_rect)
    screen.blit(greedy_text, text_rect_greedy)   
    pygame.draw.rect(screen, simplex_color, simplex_rect)
    screen.blit(simplex_text, text_rect_simplex)   
    pygame.display.flip()
    screen.fill((255, 255, 255)) #Die Hintergrundfarbe ist weiss
    
    #Alle Beschriftungsfelder werden mit der gespeicherten Formattierung angezeigt
    for i in range(len(df)):
        pygame.draw.rect(screen, (173,216,230), df.loc[i, 'Fields'])
        pygame.draw.rect(screen, df.loc[i, 'Color'], df.loc[i, 'Input Fields'])
    
    #Die Buttons Start und Einstellungen werden zusammengefuegt (Rechteck, 
    #Farbe und Text) und angezeigt
    pygame.draw.rect(screen, start_color, start_rect)
    screen.blit(start_text, text_rect_start)   
    pygame.draw.rect(screen, settings_color, settings_rect)
    screen.blit(settings_text, text_rect_settings)
    
    #Platzieren und zusammenfuegen der Labels und der Texteingaben basierend auf 
    #den Informationen im df
    for i in range(len(df)):
        screen.blit(df.loc[i, 'Labels'], df.loc[i, 'Assignment'])    
        #Fuer das Anzeigen der Parameter in der Feldmitte muss noch die Position
        #festgelegt werden
        text_rect = df.loc[i, 'Input'].get_rect(center=df.loc[i, 'Input Fields'].center)
        screen.blit(df.loc[i, 'Input'], text_rect.topleft)