#GrafikSetup.py

'Import der benoetigten Bibliotheken'
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

'Import der benoetigten weiteren Programmcodes'
import Setup

'In dieser Funktion werden die Grafiken erstellt, welche direkt nach dem oeffnen'
'der GUI angezeigt werden'
def Graphic():
    
    #Ein Graph wird ertstellt. Dadurch koennen die Staedte an den entsprechenden 
    #Positionen dargestellt werden
    G = nx.Graph()      
    # Definiere die Koordinaten für die Knoten
    
    coordinates =  []
    #Die Staedte werden eingelesen
    cities = pd.read_excel('Staedte_Vorlage.xlsx').set_index('City')
    Cities = cities.index.tolist()
    #Die Koordinaten jeder Stadt werden in einem Dictionary gespeichert und einer
    #Liste hinzugefuegt
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

    # Erstelle das Matplotlib-Figure und Achsenobjekte
    fig, ax = plt.subplots()

    # Zeichne das Hintergrundbild basierend auf den maximalen Koordinatenwerten
    ax.imshow(background_image, extent=[-15,115,-15,90], aspect='auto', zorder=-1)
    
    # Positionsinformationen für die Knoten abrufen
    pos = nx.get_node_attributes(G, 'pos')
    #Die Staedte werden hinzugefuegt
    nx.draw(G, pos, with_labels=True, node_size=30, node_color='red', font_size=7,
            font_weight='bold', verticalalignment='bottom', horizontalalignment='center')
    fig = plt.gcf()  
    
    #Die Grafiken werden gespeichert. Durch den Fehler wird der Fall abgefangen, dass
    #die Datei bereits von einem anderen Skript verwendet wird
    try:
        fig.savefig('graphic/Best.png', format='png', dpi=115)
        fig.savefig('graphic/Greedy.png', format='png', dpi=115)
        fig.savefig('graphic/Iteration.png', format='png', dpi=115)
        fig.savefig('graphic/Net.png', format='png', dpi=115)
        fig.savefig('graphic/Simplex.png', format='png', dpi=115)
    except PermissionError:
        pass

'Die Funktion wird aufgerufen'
Graphic()
