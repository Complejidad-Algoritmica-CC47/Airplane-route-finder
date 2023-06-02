import sys
import io
import networkx as nx
import Route as rts
from DijkstraNetworkx import dijkstrav2
from v1BFS import bfs

# Configurar la salida estándar con una codificación adecuada
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

grafo = nx.Graph()
listWeightedNodes = []
routes = rts.ListRoutes()
routes.addFromCSV('unionDatav2.csv')

# Recorrer la lista de rutas de aviones y agregar los nodos al grafo
for route in routes.getList():
        
        origen = route.getSource()
        destino = route.getDestination()
    
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
caminov1 = dijkstrav2(grafo, 'Jorge Chávez International Airport', 'Begishevo Airport')
print("Camino por Dijkstra: ", caminov1)
print("Camino: ", caminov1[1])
peso_totalv1 = sum(nx.shortest_path_length(grafo, caminov1[1][i], caminov1[1][i+1], weight='weight') for i in range(len(caminov1[1])-1))
print("Peso total: ", peso_totalv1)

print("-------------------------------------------")

print("Realizando pruebas con el algoritmo de BFS")
camino = bfs(grafo, 'Jorge Chávez International Airport', 'Begishevo Airport')
print("Camino: ", camino)
peso_total = sum(nx.shortest_path_length(grafo, camino[i], camino[i+1], weight='weight') for i in range(len(camino)-1))
print("Peso total: ", peso_total)