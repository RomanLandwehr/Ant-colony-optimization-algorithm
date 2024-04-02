'Import der benoetigten Bibliotheken'
import pickle
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

'Import der benoetigten weiteren Programmcodes'
import Setup

#Import der Distanzmatrix
df_dm = Setup.distanceMatrix
#Das DataFrame wird in eine geschachtelte Liste umgewandelt
Distances = df_dm.values.tolist()
#Staedteliste erstellen
Cities = df_dm.index.tolist()

#Der Hexadezimalcode wird geladen
with open('pickle/hex.pkl', 'rb') as file:
    hex_value = str(pickle.load(file)) 
#Der Text wird in Grossbuchstaben umgewandelt
hex_value = hex_value.upper()

'Fuer die gefundene Tour wird die Distanz berechnet'
def Distance(Tour):
    distance = 0
    for i in range(len(Tour)-1):
        #Die Distanz von Punkt A zu Punkt B wird hinzuaddiert 
        distance += df_dm.loc[Tour[i], Tour[i+1]]
        print(distance)
    return distance

'Die Grafik wir erzeugt'
def Graphic(Tour):
    #Die Entfernung wird berechnet
    solution = Distance(Tour)
    #Ein Graph wird erzeugt
    G = nx.Graph()       

    #Eine Liste wird erstellt und in dieser die Staedte mit ihren Koordinaten als
    #Dictionaty gespeichert
    coordinates =  []
    for city in Cities:
        c = {city: (Setup.cities.loc[city, 'X'], Setup.cities.loc[city, 'Y'])}
        coordinates.append(c)  
        
    #Die einzelnen Staedte werden mit Hilfe ihrer Korrdinaten als Node dem Graphen
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
    result = Tour
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
    edges = nx.draw_networkx_edges(G, pos, width=5, edge_color='blue')  
    
    #bbox sorgt fuer eine Box um den Text mit der Transparenz alpha
    plt.text(-13, 84.5, 'Distanz: ' + str(int(solution)) + 'km', 
             fontsize=11, weight='bold', color='blue', bbox=dict(facecolor='white', alpha=0.25))
    #Der Instanzname wird der Grafik hinzugefuegt
    plt.text(-13, 75, 'Instanz: ' + str(hex_value), 
             fontsize=11, color='blue', bbox=dict(facecolor='white', alpha=0.25))
    
    #Die gefundene Loesung wird gespeichert
    with open('pickle/ORTools.pkl', 'wb') as file:
        pickle.dump(solution, file)

    #Zuletzt wird die Grafik gespeichert
    fig = plt.gcf()      
    try:
        fig.savefig('graphic/ORTools.png', format='png', dpi=110)
    except PermissionError:
        pass


'Im folgenden wird das Programm von OR-Tools zur Lösung des TSP-Problemsverwendet.'
'Der Code ist der Website entnommen und wurdeprinzipiell nicht verändert. An einigen'
'Stellen wurden jedoch Abschnitte hinzugefuegt, um Daten abgreifen zu koennen. Ausserdem'
'wurde die dortige Beispielinstanz durch die eigenen Daten ersetzt.'
'Quelle: https://developers.google.com/optimization/routing/tsp?hl=de'


from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    'BEGINN ÄNDERUNG'
    #Anstelle der Beispielinstanz wird die eigene Instanz eingelesen
    data["distance_matrix"] = Distances
    'ENDE ÄNDERUNG'
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data


def print_solution(manager, routing, solution):
    'BEGINN AENDERUNG'
    Tour = []
    'ENDE AENDERUNG'
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()} km")
    index = routing.Start(0)
    plan_output = "Route for vehicle 0:\n"
    route_distance = 0
    'BEGINN AENDERUNG'
    #Vor Durchlauf der Schleife muss der Startpunkt gespeichert werden
    Tour.append(manager.IndexToNode(index))
    'ENDE AENDERUNG'
    while not routing.IsEnd(index):
        plan_output += f" {manager.IndexToNode(index)} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        'BEGINN AENDERUNG'
        #Die weiteren Stationen werden ebenfalls als Index gespeichert
        Tour.append(manager.IndexToNode(index))
        'BEGINN AENDERUNG'
    plan_output += f" {manager.IndexToNode(index)}\n"
    print(plan_output)
    plan_output += f"Route distance: {route_distance}km\n"
    'BEGINN AENDERUNG'
    return route_distance, Tour
    'ENDE AENDERUNG'


def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        'BEGINN AENDERUNG'
        #Die Werte distance und tour werden ausgegeben
        distance, tour = print_solution(manager, routing, solution)
        #Die Tour wird als Liste gespeichert. Dabei dient die j als Schluessel
        #zwischen der gefunden Tour und der Staedteliste. Es wird also von einem
        #Index in einen Staedtenamen uebersetzt.
        for i in range(len(tour)):
            j = tour[i]
            tour[i] = Cities[j]
        #Grafik erzeugen
        print(tour)
        Graphic(tour)
        'ENDE AENDERUNG'


if __name__ == "__main__":
    main()