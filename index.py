from flask import Flask, render_template, request, redirect, url_for, make_response, send_from_directory
from Dijkstra import dijkstrav2
from BFS import bfs
import networkx as nx
import Graph as gp 

app = Flask(__name__)

grafo = nx.Graph()
grafo, airports = gp.initGraph()

mapDijkstra = gp.cleanMap()
mapBFS = gp.cleanMap()

# Ruta principal del servidor
@app.route('/', methods=['GET', 'POST'])
def index():
    caminobfs = 'Pendiente'
    caminodijkstra = 'Pendiente'

    # Pruebas con el algoritmo de Dijkstra y BFS

    # Se crea el grafo (con los id de los aeropuertos como
    # nodos y con las rutas como aristas) y se cargan los aeropuertos

    if request.method == 'POST':
        # Se obtienen los datos del formulario
        source_airport_id = request.form.get('sourceAirportId')
        destination_airport_id = request.form.get('destinationAirportId')

        # Realizando pruebas con el algoritmo de Dijkstra
        # CaminoDijkstra es una tupla que contiene el peso total y el
        # camino. El camino es una lista de los nodos que se deben recorrer
        # PesototalDijkstra es el peso total del camino (suma de las distancias de las aristas)
        camino_dijkstra = dijkstrav2(grafo, source_airport_id, destination_airport_id)
        print("Camino: ", camino_dijkstra[1])

        # peso_totalDijkstra = sum(nx.shortest_path_length(grafo, caminoDijkstra[1][i], caminoDijkstra[1][i+1], weight='weight') for i in range(len(caminoDijkstra[1])-1))
        # print("Peso total: ", peso_totalDijkstra)

        if not camino_dijkstra:
            folium_map = gp.cleanMap()
            folium_map.save('templates/mapDijkstra.html')
            caminodijkstra = 'NO se encontró un camino de Dijkstra'
            print("-------------------------------------------")
            print("No se encontró un camino de Dijkstra")
        else:
            # Se crea el mapa con el camino de Dijkstra
            folium_map = gp.drawMap(grafo, camino_dijkstra[1], airports)
            mapDijkstra = folium_map
            # Se guarda el mapa en un archivo html
            folium_map.save('templates/mapDijkstra.html')
            caminodijkstra = 'SI se encontró un camino de Dijkstra'
            print("-------------------------------------------")
            print("Se encontró un camino de Dijkstra")

        # Realizando pruebas con el algoritmo de BFS
        # CaminoBFS es una lista de los nodos que se deben recorrer
        # PesototalBFS es el peso total del camino (suma de las distancias de las aristas)
        camino_bfs = bfs(grafo, source_airport_id, destination_airport_id)
        print("Camino: ", camino_bfs)
        # peso_totalBFS = sum(nx.shortest_path_length(grafo, caminoBFS[i], caminoBFS[i+1], weight='weight') for i in range(len(caminoBFS)-1))

        if not camino_bfs:
            folium_map = gp.cleanMap()
            folium_map.save('templates/mapBFS.html')
            caminobfs = 'NO se encontró un camino de BFS'
            print("-------------------------------------------")
            print("No se encontró un camino de BFS")
        else:
            # Se crea el mapa con el camino de BFS
            folium_map = gp.drawMap(grafo, camino_bfs, airports)
            mapBFS = folium_map
            # Se guarda el mapa en un archivo html
            folium_map.save('templates/mapBFS.html')
            caminobfs = 'SI se encontró un camino de BFS'
            print("-------------------------------------------")
            print("Se encontró un camino de BFS")

        # return render_template('index.html', caminobfs=caminobfs, caminodijkstra=caminodijkstra)
        return redirect(url_for('index'))

    else:
        # folium_map = gp.cleanMap()
        # folium_map.save('templates/mapDijkstra.html')
        # folium_map.save('templates/mapBFS.html')
        # Se renderiza el index
        #return render_template('index.html', caminobfs=caminobfs, caminodijkstra=caminodijkstra)

        response = make_response(render_template("index.html"))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response


# Ruta para obtener el camino de Dijkstra
# Se llama a esta ruta desde el index.html
# @app.route('/dijkstra', methods=['POST'])
# def dijkstra():
#     # Se obtienen los datos del formulario
#     origen = request.form['origen']
#     destino = request.form['destino']
#
#     # Se crea el grafo (con los id de los aeropuertos como
#     # nodos y con las rutas como aristas) y se cargan los aeropuertos
#     grafo = nx.Graph()
#     grafo, airports = gp.initGraph()
#
#     # Se obtiene el camino de Dijkstra
#     caminoDijkstra = dijkstrav2(grafo, origen, destino)
#     # Se obtiene el peso total del camino
#     peso_totalDijkstra = sum(
#         nx.shortest_path_length(grafo, caminoDijkstra[1][i], caminoDijkstra[1][i + 1], weight='weight') for i in
#         range(len(caminoDijkstra[1]) - 1))
#
#     # Se crea el mapa con el camino de Dijkstra
#     folium_map = gp.drawMap(grafo, caminoDijkstra[1], airports)
#     # Se guarda el mapa en un archivo html
#     folium_map.save('templates/mapDijkstra.html')
#
#     # Se renderiza el index
#     return render_template('index.html')  # , caminoDijkstra=caminoDijkstra[1], peso_totalDijkstra=peso_totalDijkstra)
#


# Se renderiza el mapa de Dijkstra
# Se llama a esta ruta desde el index.html para mostrar el mapa
@app.route('/mapDijkstra')
def mapDijkstra():
    #return render_template('mapDijkstra.html')
    #return '<a href="mapDijkstra.html" target="_blank">Ver mapa Dijkstra</a>'
    return send_from_directory('templates', 'mapDijkstra.html')


# Se renderiza el mapa de BFS
# Se llama a esta ruta desde el index.html para mostrar el mapa
@app.route('/mapBFS')
def mapBFS():
    #return render_template('mapBFS.html')
    #return '<a href="mapBFS.html" target="_blank">Ver mapa BFS</a>'
    return send_from_directory('templates', 'mapBFS.html')


@app.context_processor
def inject_version():
    import time
    return {'version': int(time.time())}

if __name__ == "__main__":
    app.run(debug=True)