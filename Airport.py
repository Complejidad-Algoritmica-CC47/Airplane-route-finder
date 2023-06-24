import csv

class Airport:
    def __init__(self, id, name, city, country, latitude, longitude, altitude):
        self.id = id
        self.name = name
        self.city = city
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
                 
    def __str__(self):
        return f"Nombre: {self.name} -> Pais: {self.country} -> Latitud: {self.latitude} -> Longitud: {self.longitude} -> Altitud: {self.altitude}"
    
    def getPosition(self):
        return (self.latitude, self.longitude)

    def getId(self):
        return self.id
    
class ListAirports:
    def __init__(self):
        self.dict = {}

    def __str__(self):
        return f"{self.dict}"
    
    def getList(self):
        return self.dict
    
    def addAirport(self, id, info):
        self.dict[id] = info

    def getAirportByName(self, name):
        for key, airport in self.dict.items():
            if airport['name'] == name:
                 return key
        return None
    
    def getAirportById(self, id):
        if id in self.dict:
            return self.dict[id]
        
        return None
    
    def getAirportByCountry(self, country):
        airports = []
        for airport in self.dict.values():
            if airport['country'] == country:
                airports.append(airport)
        return airports
    
    def getAirportIdByIATA(self, iata):
        for key, airport in self.dict.items():
            if airport['iata'] == iata:
                return key
        return None
    
    def getAirportIdByICAO(self, icao):
        for key, airport in self.dict.items():
            if airport['icao'] == icao:
                return key
        return None
    
    def addFromCSV(self, filename):
        indice = 0
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if indice == 0:
                    indice += 1
                    continue

                # airport = Airport(
                #     row[0],         # id
                #     row[1],         # name
                #     row[2],         # city
                #     row[3],         # country
                #     float(row[6]),  # latitude
                #     float(row[7]),  # longitude
                #     float(row[8])   # altitude
                #     )
                # self.addAirport(airport)

                airport = {     
                    # 'id': row[0],         # id
                    'name': row[1],         # name
                    'city': row[2],         # city
                    'country': row[3],         # country
                    'latitude': float(row[6]),  # latitude
                    'longitude': float(row[7]),  # longitude
                    'altitude': float(row[8]),   # altitude
                    'iata': row[4],          # codigo IATA
                    'icao': row[5],          # codigo ICAO
                    }
                
                self.dict[row[0]] = airport

                indice += 1

        print(f"Se han cargado {indice} aeropuertos")