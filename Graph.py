import sys
import io
import networkx as nx
import folium as fl
from Airport import Airport, ListAirports
import Route as rts

# Configurar la salida estándar con una codificación adecuada
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def initGraph():
    grafo = nx.Graph()
    listWeightedNodes = []

    routes = rts.ListRoutes()
    routes.addFromCSV('database/routes.csv')

    airports = ListAirports()
    airports.addFromCSV('database/airports.csv')

    # Recorrer la lista de rutas de aviones y agregar los nodos al grafo
    for route in routes.getList():

            origen = route.getSourceId()
            destino = route.getDestinationId()
        
            try: 
                latitud_origen = float(route.getSourceLatitude())
                longitud_origen = float(route.getSourceLongitude())
                latitud_destino = float(route.getDestinationLatitude())
                longitud_destino = float(route.getDestinationLongitude())
            except:
                continue
            
            distancia = route.getDistance()
        
            if not grafo.has_node(origen):
                grafo.add_node(origen)
            
            if not grafo.has_node(destino):
                grafo.add_node(destino)

            nodo = (origen, destino, distancia)
            listWeightedNodes.append(nodo)
        
    grafo.add_weighted_edges_from(listWeightedNodes)

    return grafo, airports

def calcular_peso(grafo, airport1, airport2):
    return nx.shortest_path_length(grafo, airport1, airport2, weight='weight')

def drawMap(grafo, camino, listAirports: ListAirports):
    map = fl.Map()
    airportsAdded = []
    routesPositions = []
    
    # Iterar sobre el camino y agregar los aeropuertos al mapa (arpt es el id del aeropuerto)
    for arpt in camino:
        if arpt not in airportsAdded:
            if arpt == camino[0]:
                _color = 'red'
            elif arpt == camino[-1]:
                _color = 'green'
            else:
                _color = 'blue'

            airportsAdded.append(arpt)

            print("Aeropuerto: ", arpt)
            airport = listAirports.getAirportById(arpt)
            airportPosition = (airport['latitude'], airport['longitude'])
            routesPositions.append(airportPosition)
            map.add_child(
                fl.Marker(location=airportPosition,
                            popup=airport['name'],
                            icon=fl.Icon(prefix="fa", 
                                        icon="plane",
                                        color=_color)
            ))  
        
    # Iterar sobre la ruta y agregar las aristas con los pesos como popup
    for i in range(len(camino) - 1):
        airport1 = camino[i]
        airport2 = camino[i + 1]
        position1 = (listAirports.getAirportById(airport1)['latitude'], listAirports.getAirportById(airport1)['longitude'])
        position2 = (listAirports.getAirportById(airport2)['latitude'], listAirports.getAirportById(airport2)['longitude'])
        
        if position1 and position2:
            peso = calcular_peso(grafo, airport1, airport2)
            
            # Crear la arista y agregar el popup con el peso
            fl.PolyLine([position1, position2], color='purple', weight=2, opacity=0.5,
                            popup=f'Distancia: {peso}').add_to(map)
            
    # print("Rutas: ", grafo.edges(data=True))
    # fl.PolyLine(routesPositions, color=colors.pop(0), weight=2, opacity=0.6).add_to(map)
    return map