#Greedy.py

'Import der benoetigten Bibliotheken'
import pickle
import networkx as nx
import matplotlib.pyplot as plt

'Import der benoetigten weiteren Programmcodes'
import Kolonie
import Setup

#Der Hexadezimalcode wird geladen
with open('pickle/hex.pkl', 'rb') as file:
    hex_value = str(pickle.load(file)) 
#Der Text wird in Grossbuchstaben umgewandelt
hex_value = hex_value.upper()

'Diese Funktion fuehrt den Greedy-Nearest-Neighbor Algorithmus aus'
def Search(city):
    #Da der Greedy-Algorirthmus nicht mit einer Kolonie, sondern einer einzelnen
    #Ameise arbeitet, wird nur eine erzeugt und ihr eine Position zugewiesen. Die
    #Startposition wird dabei der Funktion uebergeben.
    ant = Kolonie.Ant('Greedy')
    ant.position = city
    ant.visited = []
    
    #Die Entfernungsmatrix wird aufgerufen
    distance_matrix = Setup.distanceMatrix
    
    #Die Suche wird solange durchgefuehrt, bis ein Abbruchkriterium erreicht wird
    while 1:
        #Es wird die Spalte mit den Entfernungen von der aktuellen Position der Ameise
        #aus ausgewaehlt
        distances = distance_matrix.loc[ant.position].sort_values(ascending = True)
        ant.AddCity()
        distances = distances.drop(ant.visited)
        #Hat die Ameise bereits alle Staedte einmal besucht, so gibt es keine weiteren
        #zu besuchenden Staedte und die Bedingung wird erfuellt
        if len(distances) == 0:
            #Die Entfernung zwischen der aktuellen Position und der Startposition
            #wird ermittelt und der Gesamtentfernung hinzugefuegt
            distance = distance_matrix.loc[ant.position, ant.visited[0]]
            ant.distance_travelled += distance
            #Die Position und die Liste der besuchten Staedte werden aktualisiert
            ant.position = ant.visited[0]
            ant.AddCity()
            break #While-Schleife verlassen
        #Falls noch nicht alle Staedte besucht wurden, werden die Schritte unter 'else'
        #abgearbeitet
        else:
            #Die Entfernung zur (entfernungsmaessig) naechsten Stadt wird ermittelt und
            #die aktuelle Position aus der Liste der zu besuchenden Staedte entfernt
            ant.distance_travelled += distances[0]
            ant.RemoveCity()
            #Die (entfernungsmaessig) naechste Stadt wird zur neuen Position
            ant.position = distances.index[0]  
    #Die Tour und die beste Loesung des Greey-Alorithmus (Cnn) werden ausgegeben
    Tour = ant.visited
    Cnn = ant.distance_travelled
    return Cnn, Tour

'Fuer die gefundene Loesung wird eine Grafik erstellt, um diese an spaeterer Stelle'
'in der GUI anzeigen zu koennen'
def Graphic(GreedyTour, Cnn):
    #Ein Graph wird ezeugt
    G = nx.Graph()  

    #Eine Liste wird erstellt und in dieser die Staedte mit ihren Koordinaten als
    #Dictionaty gespeichert
    coordinates =  []
    Cities = Setup.cities.index.tolist()
    for city in Cities:
        c = {city: (Setup.cities.loc[city, 'X'], Setup.cities.loc[city, 'Y'])}
        coordinates.append(c)
   
    #Die einzelnen Staedte werden mit Hilfe ihrer Koordinaten als Node dem Graphen
    #hinzugefuegt
    for node in coordinates:
        n = list(node)
        city = n[0]
        xy = node[city]
        G.add_node(city, pos=xy)
    
    #Das Hintergrundbild wird geladen und hinzugefuegt
    background_image_path = "graphic/EU.jpg"
    background_image = plt.imread(background_image_path)
    fig, ax = plt.subplots()
    ax.imshow(background_image, extent=[-15,115,-15,90], aspect='auto', zorder=-1)

    #Die uebergebene Tour wird dem Graphen hinzugefuegt
    result = GreedyTour
    Result = []
    for i in range(len(result)-1):
        G.add_edge(result[i], result[i+1])
        Result.append((result[i], result[i+1]))
    
    #Die Positionen der Knoten im Graphen werden aus den Attributen 'pos' extrahiert.
    pos = nx.get_node_attributes(G, 'pos')  
    #Der Graph wird mithilfe der nx.draw-Funktion gezeichnet.
    nx.draw(G, pos, with_labels=True, node_size=30, node_color='red', font_size=7,
            font_weight='bold', verticalalignment='bottom', horizontalalignment='center')
    #Die Kanten des Graphen werden gezeichnet.
    edges = nx.draw_networkx_edges(G, pos, width=5, edge_color='red')
    
    
    #Die Texte fuer die Entfernung und die Berechnungsdauer werden hinzugefuegt
    #bbox sorgt fuer eine Box um den Text mit der Transparenz alpha
    plt.text(-13, 84.5, 'Distanz: ' + str(round(Cnn,2)) + 'km', 
             fontsize=11, weight='bold', color='red', bbox=dict(facecolor='white', alpha=0.25))
    #Der Instanzname wird der Grafik hinzugefuegt
    plt.text(-13, 75, 'Instanz: ' + str(hex_value), 
             fontsize=11, color='red', bbox=dict(facecolor='white', alpha=0.25))
    
    #Zuletzt wird die Grafik gespeichert
    fig = plt.gcf()     
    plt.show()
    try:
        fig.savefig('graphic/Greedy.png', format='png', dpi=110)
    except PermissionError:
        pass
    
'Die Funktion fuehrt fuer jede Stadt eine Suche aus und speichert die beste'
'gefundene Loesung'
def Greedy():
    best = 9e9
    #Fuer alle Staedte wird eine Suche durchgefuehrt. Nur die beste gefundene Loesung
    #wird nachfolgend betrachtet
    for city in Setup.city_list:
        x, Tour = Search(city)
        if x < best:
            best = x
            BestTour = Tour
    #Fuer die beste gefundene Loesung wird eine Grafik erstellt
    Graphic(BestTour, best)
    #Die Distanz wird gespeichert
    with open('pickle/Cnn.pkl', 'wb') as file:
        pickle.dump(best, file)

Greedy()