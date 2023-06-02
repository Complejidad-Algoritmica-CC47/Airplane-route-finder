import csv


class Airport:
    def __init__(self, name, city, country, latitude, longitude, altitude):
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
    
class ListAirports:
    def __init__(self):
        self.list = []

    def __str__(self):
        return f"{self.list}"
    
    def getList(self):
        return self.list
    
    def addAirport(self, airport):
        self.list.append(airport)

    def getAirportByName(self, name):
        for airport in self.list:
            if airport.name == name:
                return airport
        return None
    
    def getAirportByCountry(self, country):
        airports = []
        for airport in self.list:
            if airport.country == country:
                airports.append(airport)
        return airports
    
    def addFromCSV(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                airport = Airport(
                    row[1],         # name
                    row[3],         # country
                    float(row[6]),  # latitude
                    float(row[7]),  # longitude
                    float(row[8])   # altitude
                    )
                self.addAirport(airport)