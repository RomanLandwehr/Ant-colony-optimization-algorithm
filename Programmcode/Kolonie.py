#Kolonie.py


'In diesem Skript wird die Klasse Ant definiert, um Ameisen erzeugen zu koennen'

'Import der benoetigten Bibliotheken'
import Setup
import random

class Ant():
    
    #An dieser Stelle werden Parameter festgelegt, welche fuer alle Objekte einer
    #Klasse gelten. 
    Ants = [] #Notwendig um Klassenmethoden anzuwenden
    Best_Distance_Iteration = 9e9 #Initialisierung; hoch damit in Iteration 1 neue beste Loesung gefunden wird
    Best_Tour_Iteration     = []  #Initialisierung
    Best_Distance_Total = 9e9     #Initialisierung; hoch damit in Iteration 1 neue beste Loesung gefunden wird
    Best_Tour_Total     = []      #Initialisierung
    
    'Mit __init__ werden die Objekte mit den entsprechenden Parametern erzeugt'
    def __init__(self, i):
        self.name = i
        self.position = self.StartingPoint()
        self.distance_travelled = 0
        self.visited = [self.position]
        self.to_visit = Setup.city_list[:] 
        
        #Alle erzeugten Objekte werden der bereits erstellten Liste angehaengt, 
        #um Klassenmethoden anwenden zu koennen.
        Ant.Ants.append(self) 
    
    'Der Startpunkt wird zufaellig aus der Liste der Staedte ausgewaehlt'
    def StartingPoint(self):
        startingPoint = random.choice(Setup.city_list)
        return startingPoint
    
    'Der aktuelle Standort wird aus der Liste der zu besuchenden Staedte entfernt'
    def RemoveCity(self):
        self.to_visit.remove(self.position)
    
    'Der aktuelle Standort wird zu der Liste der besuchten Staedte hinzugefuegt'
    def AddCity(self):
        self.visited.append(self.position)
    
    'Die Klassenmethode ermoeglicht fuer alle Ameisen einer Kolonie gleichzeitig'
    'einen Parameter zu aendern. Dies geschieht nach eine Iteration, wenn die'
    'Erinnerungen der Ameisen gewissermassen geloescht werden'
    @classmethod        
    def Reset(cls):
        for ant in cls.Ants:
            ant.to_visit = Setup.city_list[:]
            ant.position = ant.StartingPoint() #Die Ameise wird wieder zufaellig platziert
            ant.visited = [ant.position]
            ant.distance_travelled = 0

