import sys
import io
import networkx as nx
import folium as fl
from Airport import Airport, ListAirports
import Route as rts
from DijkstraNetworkx import dijkstrav2
from v1BFS import bfs

# Configurar la salida estándar con una codificación adecuada
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Pruebas con el algoritmo de Dijkstra y BFS")

grafo = nx.Graph()
listWeightedNodes = []

routes = rts.ListRoutes()
routes.addFromCSV('unionDatav2.csv')

airports = ListAirports()
airports.addFromCSV('airports.csv')

# Recorrer la lista de rutas de aviones y agregar los nodos al grafo
for route in routes.getList():
        
        # origen = route.getSourceName()
        # destino = route.getDestinationName()

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

print("-------------------------------------------")

print("Realizando pruebas con el algoritmo de Dijkstra")
caminov1 = dijkstrav2(grafo, '2789', '5415') # Jorge Chávez International Airport, Begishevo Airport
print("Camino por Dijkstra: ", caminov1)
print("Camino: ", caminov1[1])  
peso_totalv1 = sum(nx.shortest_path_length(grafo, caminov1[1][i], caminov1[1][i+1], weight='weight') for i in range(len(caminov1[1])-1))
print("Peso total: ", peso_totalv1)

print("-------------------------------------------") 

print("Realizando pruebas con el algoritmo de BFS")
camino = bfs(grafo, '2789', '5415') # Jorge Chávez International Airport, Begishevo Airport
print("Camino: ", camino)  
peso_total = sum(nx.shortest_path_length(grafo, camino[i], camino[i+1], weight='weight') for i in range(len(camino)-1))
print("Peso total: ", peso_total)

print("-------------------------------------------")

def calcular_peso(airport1, airport2):
    return nx.shortest_path_length(grafo, airport1, airport2, weight='weight')

def drawMap(camino, listAirports: ListAirports):
    map = fl.Map()
    airportsAdded = []
    routesPositions = []
    
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
            airport: Airport = listAirports.getAirportById(arpt)
            airportPosition = airport.getPosition()
            routesPositions.append(airportPosition)
            map.add_child(
                fl.Marker(location=airportPosition[0:2],
                            popup=airport.name,
                            icon=fl.Icon(prefix="fa", 
                                        icon="plane",
                                        color=_color)
            )) 
        
    # Iterar sobre la ruta y agregar las aristas con los pesos como popup
    for i in range(len(camino) - 1):
        airport1 = camino[i]
        airport2 = camino[i + 1]
        position1 = listAirports.getAirportById(airport1).getPosition()
        position2 = listAirports.getAirportById(airport2).getPosition()
        
        if position1 and position2:
            # Calcular el peso entre los aeropuertos 
            # print("Aeropuerto 1: ", airport1)
            # print("Aeropuerto 2: ", airport2)
            peso = calcular_peso(airport1, airport2)
            # print("Peso: ", peso)
            
            # Crear la arista y agregar el popup con el peso
            fl.PolyLine([position1, position2], color='purple', weight=2, opacity=0.5,
                            popup=f'Peso: {peso}').add_to(map)
            
    # print("Rutas: ", grafo.edges(data=True))
    # fl.PolyLine(routesPositions, color=colors.pop(0), weight=2, opacity=0.6).add_to(map)
    return map
 

folium_map = drawMap(caminov1[1], airports)
folium_map.save("mapDikjstra.html") 

print("-------------------------------------------")

folium_map = drawMap(camino, airports)
folium_map.save("mapBFS.html")

