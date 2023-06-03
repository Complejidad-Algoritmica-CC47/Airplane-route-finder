from flask import Flask, render_template, request
from Dijkstra import dijkstrav2
from BFS import bfs
import networkx as nx
import Graph as gp 

app = Flask(__name__)

# Ruta principal del servidor
@app.route('/')
def index():

    #Pruebas con el algoritmo de Dijkstra y BFS

    # Se crea el grafo (con los id de los aeropuertos como
    # nodos y con las rutas como aristas) y se cargan los aeropuertos
    grafo = nx.Graph() 
    grafo, airports = gp.initGraph()

    # Realizando pruebas con el algoritmo de Dijkstra
    # CaminoDijkstra es una tupla que contiene el peso total y el 
    # camino. El camino es una lista de los nodos que se deben recorrer
    # PesototalDijkstra es el peso total del camino (suma de las distancias de las aristas)
    caminoDijkstra = dijkstrav2(grafo, '2789', '5415')
    print("Camino: ", caminoDijkstra[1])  
    peso_totalDijkstra = sum(nx.shortest_path_length(grafo, caminoDijkstra[1][i], caminoDijkstra[1][i+1], weight='weight') for i in range(len(caminoDijkstra[1])-1))
    print("Peso total: ", peso_totalDijkstra)

    print("-------------------------------------------") 

    # Realizando pruebas con el algoritmo de BFS
    # CaminoBFS es una lista de los nodos que se deben recorrer
    # PesototalBFS es el peso total del camino (suma de las distancias de las aristas)
    caminoBFS = bfs(grafo, '2789', '5415')
    print("Camino: ", caminoBFS)  
    peso_totalBFS = sum(nx.shortest_path_length(grafo, caminoBFS[i], caminoBFS[i+1], weight='weight') for i in range(len(caminoBFS)-1))
    print("Peso total: ", peso_totalBFS)

    print("-------------------------------------------")

    # Se crea el mapa con el camino de Dijkstra
    folium_map = gp.drawMap(grafo, caminoDijkstra[1], airports) 
    # Se guarda el mapa en un archivo html
    folium_map.save('templates/mapDijkstra.html') 

    print("-------------------------------------------")

    # Se crea el mapa con el camino de BFS
    folium_map = gp.drawMap(grafo, caminoBFS, airports)
    # Se guarda el mapa en un archivo html
    folium_map.save('templates/mapBFS.html')

    # Se renderiza el index
    return render_template('index.html')


# Se renderiza el mapa de Dijkstra
# Se llama a esta ruta desde el index.html para mostrar el mapa
@app.route('/mapDijkstra')
def mapDijkstra():
    return render_template('mapDijkstra.html')

# Se renderiza el mapa de BFS
# Se llama a esta ruta desde el index.html para mostrar el mapa
@app.route('/mapBFS') 
def mapBFS():
    return render_template('mapBFS.html')

if __name__ == "__main__":
    app.run(debug=True)