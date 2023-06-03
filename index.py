import sys
import io 
import networkx as nx
from Dijkstra import dijkstrav2
from BFS import bfs
import Graph as gp 

def main():

    print("Pruebas con el algoritmo de Dijkstra y BFS") 

    grafo = nx.Graph() 
    grafo, airports = gp.initGraph()

    print("-------------------------------------------")

    print("Realizando pruebas con el algoritmo de Dijkstra")
    caminov1 = dijkstrav2(grafo, '2789', '5415')
    # print("Camino por Dijkstra: ", caminov1)
    print("Camino: ", caminov1[1])  
    peso_totalv1 = sum(nx.shortest_path_length(grafo, caminov1[1][i], caminov1[1][i+1], weight='weight') for i in range(len(caminov1[1])-1))
    print("Peso total: ", peso_totalv1)

    print("-------------------------------------------") 

    print("Realizando pruebas con el algoritmo de BFS")
    camino = bfs(grafo, '2789', '5415')
    print("Camino: ", camino)  
    peso_total = sum(nx.shortest_path_length(grafo, camino[i], camino[i+1], weight='weight') for i in range(len(camino)-1))
    print("Peso total: ", peso_total)

    print("-------------------------------------------")

    folium_map = gp.drawMap(grafo, caminov1[1], airports) 
    folium_map.save("maps/mapDikjstra.html") 

    print("-------------------------------------------")

    folium_map = gp.drawMap(grafo, camino, airports)
    folium_map.save("maps/mapBFS.html")


if __name__ == "__main__":
    main()