#Grafik.py

'Import der benoetigten Bibliotheken'
import matplotlib.pyplot as plt
import networkx as nx
import pickle
import pandas as pd

'Import der benoetigten weiteren Programmcodes'
import Kolonie

'Die Staedte werden eingelesen und als Liste gespeichert'
cities = pd.read_excel('Staedte_Auswahl.xlsx').set_index('City')
Cities = cities.index.tolist()

#Der Hexadezimalcode wird geladen
with open('pickle/hex.pkl', 'rb') as file:
    hex_value = str(pickle.load(file)) 
#Der Text wird in Grossbuchstaben umgewandelt
hex_value = hex_value.upper()

'Dies erstellt die Grafik fuer die beste bislang gefundene Loesung'        
def Best(G):    
    #Ausgeben der besten gefundenen Tour
    result = Kolonie.Ant.Best_Tour_Total
    for i in range(len(result)-1):
        #Von Stadt A (i) nach Stadt B (i+1)
        G.add_edge(result[i], result[i+1])   
    # Positionsinformationen für die Knoten abrufen
    pos = nx.get_node_attributes(G, 'pos')  
    #Die Staedte werden gezeichnet    
    nx.draw(G, pos, with_labels=True, node_size=30, node_color='red', font_size=7,
            font_weight='bold', verticalalignment='bottom', horizontalalignment='center')
    #Die Beste gefundene Strecke wird hinzugefuegt
    edges = nx.draw_networkx_edges(G, pos, width=5, edge_color='forestgreen') 
    
    #Anschliessend wird die Beschriftung fuer die Distanz und die Dauer vorgenommen
    #bbox sorgt fuer eine Box um den Text mit der Transparenz alpha
    plt.text(-13, 84.5, 'Distanz: ' + str(int(Kolonie.Ant.Best_Distance_Total)) + 'km', 
             fontsize=11, weight='bold', color='forestgreen', bbox=dict(facecolor='white', alpha=0.25))
    plt.text(-13, 75, 'Instanz: ' + str(hex_value), 
             fontsize=11, color='forestgreen', bbox=dict(facecolor='white', alpha=0.25))
    
    #gcf = Get Current Figure', gibt also die Grafik zurueck
    fig = plt.gcf() 
    
    #Die Grafik wird gespeichert
    #Da es sich um einen einen Teil des subprocesses MMAS.py handelt, greift die GUI
    #möglicherweise gleichzeitig auf die Datei zu um diese zu laden, wodurch es zu einem
    #PermissionError kommen kann. Dies wird verhindert, indem der Fehler abgefangen und
    #in diesem Fall nichts getan wird. Bei der naechsten Iteration erfolgt ein erneuter 
    #Versuch. Dadurch ist es jedoch moeglich, dass in der GUI nicht alle Grafiken auf dem gleichen
    #Stand sind.
    try:
        fig.savefig('graphic/Best.png', format='png', dpi=110)
    except PermissionError:
        pass

'Dies erstellt die Grafik fuer die Darstellung der Pheromone'     
def Net(G, pheromones_dict):  
    #Das die Pheromone enthaltende Dictionary wird in ein DataFrame umgewandelt
    df_pm = pd.DataFrame(pheromones_dict)
    #Aus dem DataFrame werden die minimalen und maximalen Pheromonwerte ermittelt
    mini = df_pm.values.min()
    maxi = df_pm.values.max()
    i = 0
    count = 0
    
    #In der for-Schleife wird ermittelt, wie viel Pheromone auf einer Strecke
    #verteilt werden und wie dies in eine Gewichtung uebersetzt wird
    for u in G.nodes():
        j = 0 
        i += 1
        for v in G.nodes():
            j += 1
            #Durch i > j wird jede Strecke nur in eine Richtung gezeichnet
            if i > j:
                #Auslesen der Pheromone
                x = df_pm.loc[u, v]
                #Eine Strecke wird nur gezeichnet, sofern mehr Pheromone vorhanden sind
                #als auf der Strecke mit den wenigsten Pheromonen. Dies sorgt fuer eine 
                #deutlich bessere Uebersichtlichkeit. Bei MMAS wuerde andernfalls keine
                #Strecke gaenzlich verschwinden
                if x > mini:
                    count += 1 #Wird benoetigt, falls nur auf einer Route Pheromone (>min) vorhanden sind
                    #Es erfolgt eine Normalisierung, um bereits im fruehen Stadium der
                    #Optimierung Unterschiede erkennbar werden zu lassen
                    x = (x-mini)/(maxi-mini)
                    x *= 5 #Skalierung
                    G.add_edge(u, v,weight=x)
        
    pos = nx.get_node_attributes(G, 'pos')
    #Die Gewichtung wird aus dem Graphen extrahiert
    edge_width = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw(G, pos, with_labels=True, node_size=30, node_color='red', font_size=7,
            font_weight='bold', verticalalignment='bottom', horizontalalignment='center')
    
    #Falls es nur so viele Verbindungen wie Staedte gibt, wird die Route inschwarz geplottet. Wird 
    #dies nicht beachtet, so ist im Konvergenzfall keine Tour zu erkennen (Farbe=weiss)
    if count == len(Cities):
        #Die entsprechenden Stecken werden gezeichnet/ hinzugefuegt
        edges = nx.draw_networkx_edges(G, pos, width=edge_width, edge_color='black') 
    else:
        #Falls es mehr Strecken als Staedte gibt, wird sowohl bei der Dicke, als auch bei der Farbe
        #eine Gewichtung vorgenommen, um die Menge an Pheromonen hervorzuheben
        edges = nx.draw_networkx_edges(G, pos, width=edge_width, edge_color=edge_width, edge_cmap=plt.cm.binary) 
    
    #Anschliessend wird die Beschriftung fuer die Distanz und die Dauer vorgenommen
    plt.text(-13, 84.5, 'Distanz: ' + str(int(Kolonie.Ant.Best_Distance_Iteration)) +'km', 
             fontsize=11, weight='bold', color='black', bbox=dict(facecolor='white', alpha=0.25))
    plt.text(-13, 75, 'Instanz: ' + str(hex_value), 
             fontsize=11, color='black', bbox=dict(facecolor='white', alpha=0.25))
    
    fig = plt.gcf() 
    
    #Der Plot wird gespeichert     
    try:
        fig.savefig('graphic/Net.png', format='png', dpi=110)
    except PermissionError:
        pass
    
'Dies erstellt die Grafik fuer die beste Loesung der letzten Iteration'     
def Iteration(G):
    #Zuenachst wird die Liste mit den bisherigen Ergebnissen der Optimierung
    #geladen
    with open('pickle/convergence.pkl', 'rb') as file:
        convergence = pickle.load(file)
    #Die beste Loesung der Iteration wird ausgewaehlt
    'BestTour'
    result = Kolonie.Ant.Best_Tour_Iteration
    #Alle in result enthaltenen Strecken werden dem Netz hinzugefuegt
    for i in range(len(result)-1):
        #Von Stadt A (i) nach Stadt B (i+1)
        G.add_edge(result[i], result[i+1])   
    pos = nx.get_node_attributes(G, 'pos') 
    #Der Graph wird gezeichnet
    nx.draw(G, pos, with_labels=True, node_size=30, node_color='red', font_size=7,
            font_weight='bold', verticalalignment='bottom', horizontalalignment='center')
    #Die Strecken (Beste Tour) werden hinzugefuegt
    edges = nx.draw_networkx_edges(G, pos, width=5, edge_color='black')   
    #Anschliessend wird die Beschriftung fuer die Distanz und die Dauer vorgenommen
    plt.text(-13, 84.5, 'Distanz: ' + str(int(Kolonie.Ant.Best_Distance_Iteration)) + 'km', 
             fontsize=11, weight='bold', color='black', bbox=dict(facecolor='white', alpha=0.25))
    plt.text(-13, 75, 'Instanz: ' + str(hex_value), 
             fontsize=11, color='black', bbox=dict(facecolor='white', alpha=0.25))
    
    fig = plt.gcf() 
    #Der Plot wird gespeichert     
    try:
        fig.savefig('graphic/Iteration.png', format='png', dpi=110)
    except PermissionError:
        pass

'Dies erstellt die Grafik fuer die Konvergenz' 
def Convergence():
    #Die Ergebnisse der Algorithmen werden geladen, um sie darstellen zu koennen
    with open('pickle/Cnn.pkl', 'rb') as file:
        Cnn = int(pickle.load(file))
    with open('pickle/convergence.pkl', 'rb') as file:
        convergence = pickle.load(file)
    with open('pickle/ORTools.pkl', 'rb') as file:
        ORTools = pickle.load(file)
    opt = Kolonie.Ant.Best_Distance_Total
    #Aus der Liste der bisherigen Ergebnisse der Optimierung wird ein DataFrame
    #erstellt
    df = pd.DataFrame(convergence)
    #Ein Plot aus dem DataFrame wird erstellt und beschriftet
    ax = df.plot()
    plt.xlabel('Iterationen', fontsize=15)
    plt.ylabel('Distanz', fontsize=15)
    plt.title('Konvergenz', fontsize=20)
    #Die entsprechenden Werte werden in das Diagramm eingezeichnet. Zudem wird
    #die Farbe festgelegt und die Art als gestrichelt definiert
    ax.axhline(y=Cnn, color='r', linestyle='--', label='Greedy')
    ax.axhline(y=opt, color='g', linestyle='--', label='ACO')
    ax.axhline(y=ORTools, color='b', linestyle='--', label='OR-Tools')
    #Eine Legende wird hinzugefuegt
    ax.legend(['Iterationswert', 'Greedy', 'ACO', 'OR-Tools'], loc='best')
    fig = plt.gcf()    
    #Zuletzt wird die Grafik gespeichert
    try:
        fig.savefig('graphic/Convergence.png', format='png', dpi=100)
    except PermissionError:
        pass

'Dies Funktion Plot vereint alle Schritte, die den spezifischen Funktionen gemein sind'         
def Plot(pheromones_dict): 
    coordinates =  [] 
    #Ein Graph wird erstellt. Dies ist die Grundlage fuer die Darstellung der
    #Pheromone als Netz
    G = nx.Graph()         
    #Die Koordinaten jeder Stadt werden in einem Dictionary gespeichert
    for city in Cities:
        c = {city: (cities.loc[city, 'X'], cities.loc[city, 'Y'])}
        coordinates.append(c) 
    #Die Staedte werden als Punkt (Node) dem Netz (Graph) zugewiesen
    for node in coordinates:
        n = list(node) #Wandle das dictionary in eine Liste um
        city = n[0] #Waehle nur die Stadt
        xy = node[city] #Korrdinaten werden mit Hilfe des Schluessels Stadt gewaehlt
        G.add_node(city, pos=xy) #Zuletzt wird die Stadt dem Graphen hinzugefuegt
    
    #Das Hintergrundbild wird geladen
    background_image_path = "graphic/EU.jpg"
    background_image = plt.imread(background_image_path)
    
    #Es wird ein Plot erstellt und diesem das Hintergrundbild zugewiesen
    fig, ax = plt.subplots()
    ax.imshow(background_image, extent=[-15,115,-15,90], aspect='auto', zorder=-1)   
    #Der Graph muss als Kopie uebergeben werden, da er sonst manipuliert wird
    Iteration(G.copy()) #Funktionsaufruf
    
    #Aus praktischen Gruenden muss der Schritt wiederholt werden (Ansonsten keine
    #gelungene grafische Darstellung)
    fig, ax = plt.subplots()
    ax.imshow(background_image, extent=[-15,115,-15,90], aspect='auto', zorder=-1)   
    Best(G.copy()) #Funktionsaufruf
    
    #Siehe oben
    fig, ax = plt.subplots()
    ax.imshow(background_image, extent=[-15,115,-15,90], aspect='auto', zorder=-1)
    Net(G.copy(), pheromones_dict) #Funktionsaufruf  
    
    Convergence() #Funktionsaufruf

    
    