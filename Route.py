import csv
from Airport import Airport

class Route (object):
    def __init__(self, 
                    sourceId,
                    sourceName,
                    sourceCity,
                    sourceCountry, 
                    sourceLatitude,
                    sourceLongitude,
                    sourceAltitude,
                    destinationId,
                    destinationName,
                    destinationCity,
                    destinationCountry,
                    destinationLatitude,
                    destinationLongitude,
                    destinationAltitude,
                    distance
                    ):
        self.source = Airport(
                    sourceId,
                    sourceName,
                    sourceCity,
                    sourceCountry,
                    sourceLatitude,
                    sourceLongitude,
                    sourceAltitude
                    )
        self.destination = Airport(
                    destinationId,
                    destinationName,
                    destinationCity,
                    destinationCountry,
                    destinationLatitude,
                    destinationLongitude,
                    destinationAltitude
                    )
        self.distance = distance

    def __str__(self):
        return f"Origen: {self.source} -> Destino: {self.destination} -> Distancia: {self.distance}"
    
    def getRoute(self):
        return (self.source, self.destination, self.distance)
    
    def getSourceId(self):
        return self.source.id
    
    def getSourceName(self):
        return self.source.name
    
    def getSourceLatitude(self):
        return self.source.latitude
    
    def getSourceLongitude(self):
        return self.source.longitude
    
    def getSourceAltitude(self):
        return self.source.altitude
    
    def getDestinationId(self):
        return self.destination.id
    
    def getDestinationName(self):
        return self.destination.name
    
    def getDestinationLatitude(self):
        return self.destination.latitude
    
    def getDestinationLongitude(self):
        return self.destination.longitude
    
    def getDestinationAltitude(self):
        return self.destination.altitude
    
    def getDistance(self):
        return self.distance

    

class ListRoutes:
    def __init__(self):
        self.list = []

    def __str__(self):
        return f"{self.list}"
    
    def getList(self):
        return self.list
    
    def addRoute(self, route):
        self.list.append(route)

    def addFromCSV(self, filename):
        indice = 0
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if indice == 0:
                    indice += 1
                    continue

                route = Route(
                    row[3],         # sourceId
                    row[4],         # sourceName
                    row[5],         # sourceCity
                    row[6],         # sourceCountry
                    float(row[7]),  # sourceLatitude
                    float(row[8]),  # sourceLongitude
                    float(row[9]),  # sourceAltitude
                    row[12],        # destinationId
                    row[13],        # destinationName
                    row[14],        # destinationCity
                    row[15],        # destinationCountry
                    float(row[16]), # destinationLatitude
                    float(row[17]), # destinationLongitude
                    float(row[18]), # destinationAltitude
                    float(row[20])  # distance
                    )
                self.addRoute(route)
                indice += 1
        
        print(f"Se han leído {indice} rutas de aviones")

            