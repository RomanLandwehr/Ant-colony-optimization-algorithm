#MMAS.py

'In diesem Skript wird der MMAS-Algorithmus implementiert'

'Import der benoetigten Bibliotheken'
import time
import pickle
from tqdm import tqdm 
import random

'Import der benoetigten weiteren Programmcodes'
import Kolonie
import Setup
import Grafik

'Die Funktion ConstructSolution ermittelt fuer eine Ameise das naechste Reiseziel.'
'Sie ist das wesentliche Element um eine Loesung konstruieren zu koennen, da hier'
'auf Basis der Umwelt (Pheromonmatrix und Entfernungsmatrix) eine Entscheidung'
'getroffen wird.'

def ConstructSolution(ant, pheromones_dict):
    #Zunaechst wird fuer die uebergebene Ameise die Stadt in der Liste der zu besuchenden
    #Staedte entfernt, in der sie sich gerade befindet.
    ant.RemoveCity()
    
    #Um das "originale" Dictionary nicht zu verfaelschen wir eine Kopie erstellt und
    #anschliessend aus allen Entfernungen zwischen den Staedten nur die Entfernungen 
    #von der aktuellen zu allen anderen Staedten ausgewaehlt.
    distances = distances_dict.copy()
    distances = distances[ant.position]
    
    #Da zur Berechnung der Wahrscheinlichkeiten der Kehrwert der Entfernungen massgeblich
    #ist, wird eine neues Dictionary erstellt, welches die gleiche Struktur besitzt und
    #die Kehrwerte enthaelt
    dict_eta = {}   
    for City in distances.keys():
        if City != ant.position:
            dict_eta[City] = 1/distances[City]   
    
    #Wie fuer die Entfernungen werden nur die Pheromonmengen von der aktuellen 
    #zu allen anderen Staedten ausgewaehlt.
    pheromones = pheromones_dict[ant.position]   
    
    #An dieser Stelle befindet sich gewissermassen das Herzstueck des Algorithmus.
    #Hier wird gemaess der in der Hausarbeit vorgestellten Formel die Wahrscheinlichkeit
    #berechnet, mit der eine Ameise von der aktuellen Stadt zur betreffenden Stadt
    #reist.
    prob = {}   
    for city_i in ant.to_visit:
        total = 0 #Die Summe fuer jede neue Stadt muss zurueckgesetzt werden
        
        #Dies repraesentiert den Zaehler. Dabei wird die entsprechende Menge an
        #Pheromonen mit alpha potenziert und die Entfernung mit beta. Dies geschieht
        #fuer alle vom Standpunkt ausgehenden Strecken
        alpha_pheromones = pow(pheromones[city_i], alpha)
        beta_distance = pow(dict_eta[city_i], beta)
        
        #Dies repraesentiert den Nenner.
        for city_j in ant.to_visit:
            #Dies entspricht zuenachst dem Vorgehen des Zaehlers
            pheromones_ij = pow(pheromones[city_j], alpha)
            distances_ij = pow(dict_eta[city_j], beta)
            #Durch die for-Schleife geschieht dies jetzt jedoch nicht nur fuer eine
            #Strecke, sondern es wird ueber alle Strecken summiert
            total += pheromones_ij * distances_ij
        
        #Die einzelnen Bestandteile koennen nun in die Formel eingesetzt und die
        #Wahrscheinlichkeiten ausgerechnet werden
        prob[city_i] = alpha_pheromones * beta_distance
        prob[city_i] /= total
    
    #Die Wahrscheinlichkeiten werden aus dem Dictionary extrahiert
    y = list(prob.values())   
    #!An dieser Stelle wird das Ziel ausgewaehlt!
    #Es wird basierend auf der Wahrscheinlichkeit ("weights") eine Stadte 
    #bestimmt und die Position als Integer zurueckgegeben
    index = random.choices(range(len(y)), weights=y)[0]
    #Dieser Integer muss wieder in einen Staedtenamen "uebersetzt" werden
    city = ant.to_visit[index]

    #Zuletzt werden die Attribute der Ameise aktualisert. Die neue zurueckgelegte
    #Entfernung wird beruecksichtigt und die Position aktualisiert.    
    ant.distance_travelled += distances[city]
    ant.position = city
    #Die neue Position wird in die Liste der besuchten Staedte aufgenommen
    ant.AddCity()  
    return 1

'Die Funktion PheromonUpdate sorgt dafuer, dass sowohl zunaechst die Pheromone'
'mit der geforderten Verdampfungsrate evaporieren und anschliessend die neuen'
'Pheromone verteilt werden. Zuletzt wird das aktualisierte Dictionary zurueckgegeben'            
def PheromoneUpdate(pheromones_dict):
    
    #Keys stellt die Staedte dar
    keys = pheromones_dict.keys()    
    #Da die Strecken zwischen allen Staedten aktualisiert werden muessen, werden
    #zwei verschachtelte for-Schleifen benoetigt.
    for key_A in keys:
        for key_B in keys:
            #Auf jeder Strecke verdampfen die Pheromone mit der vorgegeben Rate
            pheromones_dict[key_A][key_B] *= (1-evaporation_rate)

    
    #Die beste Tour der Iteration stellt die Grundlage fuer die Verteilung der
    #Pheromone dar
    tour = Kolonie.Ant.Best_Tour_Iteration
    #Fuer die Menge an zu verteilenden Pheromonen wird die zurueckgelegte Distanz
    #benoetigt
    distance  = Kolonie.Ant.Best_Distance_Iteration
    
    #In dieser Schleife wird die Tour nachvollzogen 
    for i in range(len(tour)-1):
        start = tour[i]
        end = tour[i+1]
        for key_A in keys:
            for key_B in keys:
                #Falls eine Strecke Teil der besten Tour der Iteration ist, so
                #werden ihr zusaetzliche Pheromone hinzugefuegt (Kehrwert der
                #Distanz der Tour)
                if key_A == start and key_B == end:
                    pheromones_dict[key_A][key_B] += 1/distance
                #Dies sorgt dafuer, dass die Matrix symmetrisch bleibt
                if key_B == start and key_A == end:
                    pheromones_dict[key_A][key_B] += 1/distance
    
    #An dieser Stelle erfolgt eine spezifische Implmentierung fuer den MMAS-Ansatz
    #Es wird dafuer gesorgt, dass jede Strecke weder einen maximalen Wert ueber-
    #schreitet noch einen minimalen unterschreitet
    for key_A in keys:
        for key_B in keys:
            #Die Menge an Pheromonen darf nicht geringer sein, als der Maximalwert
            #multipliziert mit dem Faktor MinMax
            pheromones_dict[key_A][key_B] = max(pheromones_dict[key_A][key_B], 
                                                MinMax/evaporation_rate/Cnn)
            #Ausserdem darf sie auch nicht groesser sein als der Maximalwert. Dieser
            #entspricht dem Initialisierungswert vor der ersten Iteration
            pheromones_dict[key_A][key_B] = min(pheromones_dict[key_A][key_B], 
                                                1/evaporation_rate/Cnn)
            
    return pheromones_dict   

'Nachdem die letzte Stadt besucht wurde, muss die Ameise wieder zu ihrer'
'Ausgangsstadt gelangen'
def TravelBack(ant):
    
    #Durch den Index 0 wird sichergestellt, dass zur ersten Stadt
    #zurueckgekehrt wird
    distances = distances_dict.copy()
    
    #Es werden nur die Entfernungen von der aktuellen Stadt aus betrachtet
    distances = distances[ant.position]
    
    #Sofern die Stadt im Dictionary der Ausgangsstadt entspricht, wird die Entfernung
    #zwischen aktuellem Standort und Ausgangsstadt der Gesamtentfernung hinzugefuegt
    for city in distances.keys():
        if city == ant.visited[0]:
            ant.distance_travelled += distances[city]
            
    #Die Position wird aktualisiert und der Liste der besuchten Staedte hinzugefuegt
    ant.position = ant.visited[0]
    ant.AddCity()
    
    #Da es soch um die letzte "Reise" der Iteration handelt, muss ggf. die
    #beste gefundene Loesung aktualisiert werden.
    #Ist die neue Loesung dieser Ameise besser als alles was andere Ameisen in dieser
    #Iteration gefunden haben, so wird der Bestwert der Iteration aktualisiert
    if ant.distance_travelled < Kolonie.Ant.Best_Distance_Iteration:
        Kolonie.Ant.Best_Distance_Iteration = ant.distance_travelled
        Kolonie.Ant.Best_Tour_Iteration = ant.visited 
    
    #Ist die neue Loesung dieser Ameise besser als alles was andere Ameisen jemals
    #gefunden haben, so wird der Bestwert der Optimierung aktualisiert
    if Kolonie.Ant.Best_Distance_Total > Kolonie.Ant.Best_Distance_Iteration:
        Kolonie.Ant.Best_Distance_Total = Kolonie.Ant.Best_Distance_Iteration
        Kolonie.Ant.Best_Tour_Total = Kolonie.Ant.Best_Tour_Iteration  
    return 1
            

'Mit Tour findet die gesamte Kolonie eine Route'    
def Tour(Ants, pheromones_dict):
    #Es sollen sollen alle Städte genau einmal besucht werden und die naechste
    #Stadt durch ConstructSolution ermittelt werden
    for i in range(len(Setup.city_list[:])-1): 
        for ant in Ants:           
            ConstructSolution(ant, pheromones_dict) 
    #Sind alle Staedte besucht, gehen alle Ameisen wird zurück in ihre Ausgangsstadt
    for ant in Ants:                               
        TravelBack(ant)    
    return 1

def ACO():
    
    'Bevor mit der Loesung begonnen wird, werden die Daten vorbereitet'   
    Convergence = []
    
    #Die Pheromonmengen des DataFrames werden auf den Maximalwert initialisiert.
    #Außerdem erfolgt eine Umwandlung in ein Dictionary. Dies hat massive 
    #Geschwindigkeitsvorteile

    df_pm = Setup.pheromoneMatrix[:]
    df_pm.loc[:] = 1/evaporation_rate/Cnn
    pheromones_dict = df_pm.to_dict(orient='index')
    
    
    #Erzeuge die geforderte Anzahl von Ameisen
    Ants = [None] * ants
    for i in range(ants):
        ant = Kolonie.Ant(i)
        Ants[i] = ant
    
    'Es werden so viele Iteration wie vorgegeben durchgefuehrt'
    for i in tqdm(range(iterationen)):
        
        #Falls es ein Abbruchkriterium gibt und dieses erfuellt wird, stoppt 
        #der Algorithmus.
        if len(Convergence) >= stopCriteria:
            Convergence_reverse = Convergence[::-1][:]
            value = Convergence_reverse[0]
            value = [value]*stopCriteria
            
            #Voraussetzung ist, dass sich der Wert in einer bestimmten Anzahl von
            #Iterationen nicht mehr geaendert hat
            if value == Convergence_reverse[:stopCriteria]:
                Grafik.Plot(pheromones_dict)
                break

        #Der Wert fuer die beste Loesung der Iteration wird wieder zurueckgesetzt
        Kolonie.Ant.Best_Distance_Iteration = 9e9
        Kolonie.Ant.Best_Tour_Iteration = [] 
        
        #Die eigentliche Iteration wird durchgefuehrt
        Tour(Ants, pheromones_dict)
        
        #Die Funktion PheromonUpdate wird aufgerufen und die Pheromonmatrix
        #aktualisiert
        pheromones_dict = PheromoneUpdate(pheromones_dict) 
        
        #Speichere die beste Tour der Iteration in der Liste
        Convergence.append(Kolonie.Ant.Best_Distance_Iteration)
        with open('pickle/convergence.pkl', 'wb') as file:
            pickle.dump(Convergence, file)
        
        #In den Einstellungen kann festgelegt werde, wie häufig sich die Grafiken
        #aktualisieren sollen. Außerdem wird immer das Ergebnis nach der letzten
        #Iteration geplotted
        if i%plotRate == 0 or (i+1) == iterationen:
            Grafik.Plot(pheromones_dict)
            
        #Die Kolonie wird zurueckgesetzt. Eine genauere Dokumentation ist im
        #entsprechenden Skript zu finden
        Kolonie.Ant.Reset()
        
        #Falls in den Einstellungen eine Pause festgelegt wurde, wird nach einer
        #Iteration gewartet
        time.sleep(pause)
    return 1  

'Zunaechst werden die in der GUI eingestellten Parameter eingelesen'
with open('pickle/ants.pkl', 'rb') as file:
    ants = int(pickle.load(file))    
with open('pickle/evaporation.pkl', 'rb') as file:
    evaporation_rate = float(pickle.load(file))  
with open('pickle/iterations.pkl', 'rb') as file:
    iterationen = int(pickle.load(file))   
with open('pickle/alpha.pkl', 'rb') as file:
    alpha = int(pickle.load(file))   
with open('pickle/beta.pkl', 'rb') as file:
    beta = int(pickle.load(file))    
with open('pickle/pause.pkl', 'rb') as file:
    pause = float(pickle.load(file))
with open('pickle/Cnn.pkl', 'rb') as file:
    Cnn = int(pickle.load(file))    
with open('pickle/plotRate.pkl', 'rb') as file:
    plotRate = int(pickle.load(file))    
with open('pickle/stopCriteria.pkl', 'rb') as file:
    stopCriteria = int(pickle.load(file))

#Die Distanzmatrix wird eingelesen und in ein Dictionary umgewandelt. Dadruch
#ist der Algorithmus deutlich schneller
distance_matrix = Setup.distanceMatrix
distances_dict = distance_matrix.to_dict(orient='index')

#Das Verhaeltnis zwischen minimalen und maximalen Pheromonwerten wird aus den 
#uebergebenen Parametern berechnet
n = len(distance_matrix)
factor = pow(0.05,1/n)
#Bei n Staedten hat die Ameise zu Anfang n-1 Entscheidungsmoeglichkeiten und im
#letzten Schritt 0 Entscheidungsmoeglichkeiten. Die Anzahl der Entscheidungsmoeglichkeiten
#nimmt linear ab. Somit hat die Ameise im Durchschnitt (n-1-0)/2 = (n-1)/2 Moeglichkeiten
avg = (n-1)/2
MinMax = (1-factor)/((avg-1)*factor)

'Der Algorithmus wird gestrartet'
ACO()