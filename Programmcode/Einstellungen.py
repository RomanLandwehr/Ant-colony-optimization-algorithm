#Einstellungen.py

'In diesem Skript wird durch das Fenster Einstellungen eine Erweiterung der GUI'
'implementiert. Es wird durch die GUI als subprocess gestartet'

'Import der benoetigten Bibliotheken'
import pygame 
import sys 
import pickle
import pandas as pd
import time

def Einstellungen():

    'Es werden sich grundlegende Einstellungen wie die Farbocdierung oder die'
    'Fenstergroesse vorgenommen'
    color_passive = (224,255,240)
    color_active =(255,246,143)
    color_grafic = (100,100,100)
    black = (0,0,0)
    window_size = [750, 375]
    
    'Diese Standardbefehle initialisieren eine GUI in pygames'
    pygame.init() 
    screen = pygame.display.set_mode(window_size) 
    font = pygame.font.Font(None, 30)
    
    'Die Eingabefelder werden definiert'
    #Zunächst die Groesse und Position der Felder fuer die Beschriftungen
    field_pause = pygame.Rect(25,50,500,50)
    field_plotRate = pygame.Rect(25,125,500,50)
    field_stopCriteria = pygame.Rect(25,200,500,50)
    
    #Um die while-Schleife uebersichtlicher zu gestalten, werden die Parameter der
    #Felder in ein DataFrame 'verpackt'
    Fields = [field_pause, field_plotRate, field_stopCriteria]
    df = pd.DataFrame()
    df['Fields'] = Fields
    
    #Anschließend wird die Groesse und Position der Felder fuer die Eingabe festgelegt
    input_field_pause = pygame.Rect(550,50,100,50)
    input_field_plotRate = pygame.Rect(550,125,100,50)
    input_field_stopCriteria = pygame.Rect(550,200,100,50)
    
    #und dem DataFrame hinzugefuegt
    Input_Fields = [input_field_pause, input_field_plotRate, input_field_stopCriteria]    
    df['Input Fields'] = Input_Fields
    
    #Nun muss den Feldern noch eine Beschriftung zugeordnet werden
    label_pause = font.render('Pause nach jeder Iteration [s]', True, black)
    label_plotRate = font.render('Plotte nach jeder X-ten Iteration', True, black)
    label_stopCriteria = font.render('Stoppe, wenn X Iterationen stagniert', True, black)
    
    #und wird anschliessend dem DataFrame hinzugefuegt
    Labels = [label_pause, label_plotRate, label_stopCriteria]   
    df['Labels'] = Labels
    
    'Die einstellbaren Parameter werden initialisiert'
    with open('pickle/pause.pkl', 'rb') as file:
        pause = str(pickle.load(file))
    with open('pickle/plotRate.pkl', 'rb') as file:
        plotRate = str(pickle.load(file))
    with open('pickle/stopCriteria.pkl', 'rb') as file:
        stopCriteria = str(pickle.load(file))
    
    #Aufgrund der Uerbsichtlichkeit werden sie ebenfalls in einer Liste gespeichert
    Names = ['pause', 'plotRate', 'stopCriteria']
    String = [pause, plotRate, stopCriteria]
    
    #Die initialisierten Werte werden einer neuen Liste angehaengt und dabei in das 
    #benoetigte Format umgewandelt
    Input = []
    for i in range(len(String)):
        Input.append(font.render(String[i], True, black))
    
    #Dem DataFrame werden neue Spalten mit den entsprechenden Werten hinzugefuegt
    df['String'] = String
    df['Input'] = Input
    df['Names'] = Names
    
    Assignment = []
    Color = []
    Logic = []
    Input = []
    
    'Durch die for-Schleife wird die Beschriftung mit dem Feld verknuepft und die'
    'Zuweisung anschließend in einer Liste gespeichert'
    for i in range(len(df)):
        label = df.loc[i, 'Labels']
        field = df.loc[i, 'Fields']
        assignment = label.get_rect(center=field.center)
        Assignment.append(assignment)
        #Die Farbkennung wird benutzt, um optisch anzeigen zu koennen, ob ein Feld
        #bereit fuer die Eingabe ist
        Color.append(color_passive)
        Logic.append(False)
    
    #Anschließend werden diese Parameter ebenfalls dem DataFrame angehaengt
    df['Assignment'] = Assignment
    df['Color'] = Color
    df['Logic'] = Logic
    
    
    
    'Zuletzt wird der Button initialisiert'
    setting_rect = pygame.Rect(200, 300, 300, 50)
    setting_color = (80, 80, 80)
    #Der Text wird im entsprechenden Format erstellt
    setting_text = font.render("Einstellungen speichern", True, (0, 0, 0))
    #und anschließend dem Feld zugewiesen
    text_rect_setting = setting_text.get_rect(center=setting_rect.center)
    button_setting_active = False
    
    #Fensternamen festlegen
    pygame.display.set_caption("Einstellungen")
    
    'Das Fenster wird geoeffnet und durch eine while-Schleife aufrecht erhalten'
    while True: 
        
        #Falls der Button geklickt wurde, veraendert sich dessen Farbe fuer 0.25s
        if button_setting_active == True:
            time.sleep(0.25)
            setting_color = (80, 80, 80)
            button_setting_active = False
            #Nachdem das optische Feedback erfolgt ist, schliesst sich das Fenster
            try:
                process.terminate()
            except NameError:
                pass
            pygame.quit() 
            sys.exit() 
        
        'Falls es ein Event gibt (also etwas mit Maus oder Tastatur eingegeben wurde)'
        'wird die Schleife durchlaufen'
        for event in pygame.event.get(): 
            #Diese Funktion stellt das sichere Schliessen des Fensters sicher
            if event.type == pygame.QUIT: 
                try:
                    process.terminate()
                except NameError:
                    pass
                pygame.quit() 
                sys.exit() 
            
            #Falls auf ein Eingabefeld geklickt wurde, so veraendert sich dessen Farbe
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Es wird fuer alle Felder geprueft, ob sich beim Tastaturanschlag die Maus
                #uber dem Feld befand ('collidepoint). Falls ja, wird die Farbe geandert
                #und mit 'True' kann an spaeterer Stelle die Tastatureingabe zugewiesen 
                #werden
                for i in range(len(df)):
                    if df.loc[i, 'Input Fields'].collidepoint(event.pos):
                        df.at[i, 'Color'] = color_active
                        df.loc[i, 'Logic'] = True
                    else:
                        df.at[i, 'Color'] = color_passive
                        df.loc[i, 'Logic'] = False
                
            #Wird ein Buchstabe auf der Tastatur gedrueckt, so wird er einem aktiven
            #Feld zugewiesen
            if event.type == pygame.KEYDOWN:
                for i in range(len(df)):
                    if df.loc[i, 'Logic'] == True:
                        #Falls es sich jedoch um die Backspace-Taste handelt, wird
                        #der eingegebene Text geloescht
                        if event.key == pygame.K_BACKSPACE:
                            df.loc[i, 'String'] = df.loc[i, 'String'][:-1]
                        #Eingegebene Buchstaben werden dem Text hinzugefuegt
                        else:
                            df.loc[i, 'String'] += event.unicode
                        #Der Text wird dem Feld zugewiesen
                        df.loc[i, 'Input'] = font.render(df.loc[i, 'String'], True, black)
    
            'Einstellungen speichern'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if setting_rect.collidepoint(event.pos):
                    #Wird auf den Button geklicht, so werden alle getroffenen
                    #Einstellungen gespeichert
                    for i in range(len(df)):
                        path = 'pickle/' + df.loc[i, 'Names'] + '.pkl'
                        with open(path, 'wb') as file:
                            pickle.dump(df.loc[i, 'String'], file)
                    #Die Farbe wird geandert und fuer die Aktualisierung der GUI
                    #gesorgt
                    setting_color = (110, 180, 0)
                    pygame.draw.rect(screen, setting_color, setting_rect)
                    screen.blit(setting_text, text_rect_setting)
                    #Mit True wird sichergestellt, dass die if-Bedingung zu Beginn
                    #der Schleife erfuellt wird und die Farbe anschliessend wieder
                    #zurueckgesetzt wird
                    button_setting_active = True
        
        #Die GUI wird aktualisiert
        pygame.display.flip()
        #Der Hintergrund wird ausgefuehrt
        screen.fill((255, 255, 255))
        
        #Durch die Verknuepfung der einzelnen Parameter werden alle Felder
        #gezeichnet (draw)
        for i in range(len(df)):
            pygame.draw.rect(screen, (173,216,230), df.loc[i, 'Fields'])
            pygame.draw.rect(screen, df.loc[i, 'Color'], df.loc[i, 'Input Fields'])
        
        #Durch die Verknuepfung der einzelnen Parameter wird der Button gezeichnet
        pygame.draw.rect(screen, setting_color, setting_rect)
        screen.blit(setting_text, text_rect_setting)
        
        #Mit blit werden alle Rechtecke (in df) in die GUI eingezeichnet
        for i in range(len(df)):
            screen.blit(df.loc[i, 'Labels'], df.loc[i, 'Assignment'])  
            #Fuer das Anzeigen der Parameter in der Feldmitte muss noch die Position
            #festgelegt werden
            text_rect = df.loc[i, 'Input'].get_rect(center=df.loc[i, 'Input Fields'].center)
            screen.blit(df.loc[i, 'Input'], text_rect.topleft)


'Wird das Skript als subprocess ausgefuehrt, so wird an dieser Stelle die Funktion'
'aufgerufen und somit die GUI geöffnet'    
Einstellungen()