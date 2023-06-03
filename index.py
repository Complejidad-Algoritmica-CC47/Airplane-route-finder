from flask import Flask, render_template, request
from Dijkstra import dijkstrav2
from BFS import bfs
import networkx as nx
import Graph as gp 

app = Flask(__name__)

@app.route('/')
def index():

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
    folium_map.save('templates/mapDijkstra.html') 

    print("-------------------------------------------")

    folium_map = gp.drawMap(grafo, camino, airports)
    folium_map.save('templates/mapBFS.html')

    return render_template('index.html')


@app.route('/mapDijkstra')
def mapDijkstra():
    return render_template('mapDijkstra.html')
 
@app.route('/mapBFS') 
def mapBFS():
    return render_template('mapBFS.html')

if __name__ == "__main__":
    app.run(debug=True)