#Setup.py

import pandas as pd

'Diese Funktion berechnet die Distanz (euklidische Norm) aller Städte und'
'stellt sie als quadratische Matrix in Form eines Dataframes zur Verfügung'
def DistanceMatrix(df):
    I = df.shape[0] #Ermittlung der Spaltenzahl
    #Zunaechst wird ein leeres DataFrame mit der Groesse IxI erstellt
    distanceMatrix = pd.DataFrame(0, index=range(I), columns=range(I))
    for i in range(I):
        # Suche die Koordinaten von Stadt A
        X_i = df.iloc[i,0]
        Y_i = df.iloc[i,1]
        for j in range(I):
            #Suche die Koordinaten von Stadt B
            X_j = df.iloc[j,0]
            Y_j = df.iloc[j,1]
            #Berechne die Differenz der Koordinaten
            x_distance = X_i - X_j
            y_distance = Y_i - Y_j
            #Berechne die Distanz aus der Differenz der Koordinaten
            euclidean = pow(pow(x_distance,2) + pow(y_distance,2),0.5)
            #Rechne mit einem Faktor auf km um und speichere die 
            #Entfernung als Integer. Dieser Faktor wurde ermittelt, indem bei
            #'Luftlinie.org' die Entfernung zwischen Lissabon und Helsinki ermittelt
            #wurde. Diese wurde durch die euklidische Distanz auf Basis der Koordinante
            #geteilt. Es ergibt sich ein Faktor von 28.2
            euclidean *= 28.2
            euclidean = int(euclidean)
            distanceMatrix.iloc[i,j] = euclidean
    #Formatierung
    distanceMatrix = distanceMatrix.set_index(df.index)
    distanceMatrix.columns = df.index
    return distanceMatrix

'Durch diese Funktion wird die Pheromonmatrix erstellt. Dabei handelt es sich'
'um eine quadratische Matrix mit der Anzahl der Städte als Zeilen- bzw.'
'Spaltenzahl. Es werden alle Zellen mit 1 initialisiert'
def PheromoneMatrix(df):
    I = df.shape[0]
    pheromoneMatrix = pd.DataFrame(1, index=range(I), columns=range(I))
    pheromoneMatrix = pheromoneMatrix.set_index(df.index)
    pheromoneMatrix.columns = df.index
    return pheromoneMatrix


#Die Staedte mit ihren Koordinaten werden als DataFrame eingelesen
cities = pd.read_excel('Staedte_Auswahl.xlsx').set_index('City')

'Aufruf der Funktionen'
distanceMatrix = DistanceMatrix(cities)
pheromoneMatrix = PheromoneMatrix(cities)

#Die Staedte werden aus dem Index des DataFrames gelesen
city_list = cities.index.tolist()
