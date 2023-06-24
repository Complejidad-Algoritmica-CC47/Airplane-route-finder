from flask import Flask, render_template, request, redirect, url_for, make_response, send_from_directory
from Dijkstra import dijkstrav2
from BFS import bfs
import networkx as nx 
import Graph as gp 
import csv
app = Flask(__name__)

grafo = nx.Graph()
grafo, airports, airportsListFull = gp.initGraph()

mapDijkstra = gp.cleanMap()
mapBFS = gp.cleanMap()

@app.route('/', methods=['GET'])
def index():
    airportsList = airportsListFull          
    # response = make_response(render_template("index.html"))
    # response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    # response.headers["Pragma"] = "no-cache"
    # response.headers["Expires"] = "0" 
    return render_template('index.html', airportsList=airportsList)

# Ruta principal del servidor
@app.route('/', methods=['POST'])
def busqueda():
    origen = 'Pendiente'
    destino = 'Pendiente'
    distanciaDijkstra = 0
    distanciaBFS = 0
    airportsList = airportsListFull   
    # Pruebas con el algoritmo de Dijkstra y BFS

    # Se crea el grafo (con los id de los aeropuertos como
    # nodos y con las rutas como aristas) y se cargan los aeropuertos
    if request.method == 'POST':
        inputSourceAirport = request.form.get('sourceAirportId')
        inputDestinationAirport = request.form.get('destinationAirportId')
        metodo = request.form.get('metodo')

        if(metodo == 'id'):
            source_airport_id = airports.getAirportById(inputSourceAirport)
            if(source_airport_id == None):
                return render_template('index.html',  
                                airportsList=airportsList, error = True,
                                error_message = 'El id del origen no existe')

            destination_airport_id = airports.getAirportById(inputDestinationAirport)
            if(destination_airport_id == None):
                return render_template('index.html',
                                airportsList=airportsList, error = True,
                                error_message = 'El id del destino no existe')

            source_airport_id = inputSourceAirport
            destination_airport_id = inputDestinationAirport

        elif(metodo == 'name'):
            source_airport_id = airports.getAirportByName(inputSourceAirport)
            if(source_airport_id == None):
                return render_template('index.html',
                                airportsList=airportsList, error = True,
                                error_message = 'El nombre del origen no existe')

            destination_airport_id = airports.getAirportByName(inputDestinationAirport)
            if(destination_airport_id == None):
                return render_template('index.html',
                                airportsList=airportsList, error = True,
                                error_message = 'El nombre del destino no existe')

        elif(metodo == 'iata'):
            source_airport_id = airports.getAirportIdByIATA(inputSourceAirport)
            if (source_airport_id == None):
                return render_template('index.html',
                                airportsList=airportsList, error = True,
                                error_message = 'El código IATA del origen ingresado no existe')

            destination_airport_id = airports.getAirportIdByIATA(inputDestinationAirport)
            if (destination_airport_id == None):
                return render_template('index.html',
                                airportsList=airportsList, error = True,
                                error_message = 'El código IATA del destino ingresado no existe')

        elif(metodo == 'icao'): 
            source_airport_id = airports.getAirportIdByICAO(inputSourceAirport)
            if (source_airport_id == None):
                return render_template('index.html',
                                airportsList=airportsList, error = True, 
                                error_message = 'El código ICAO del origen ingresado no existe')
            destination_airport_id = airports.getAirportIdByICAO(inputDestinationAirport)
            if (destination_airport_id == None):
                return render_template('index.html', airportsList=airportsList, error = True,
                                error_message = 'El código ICAO del destino ingresado no existe')
 
        else:
            return redirect(url_for('index'))
        # Realizando pruebas con el algoritmo de Dijkstra
        # CaminoDijkstra es una tupla que contiene el peso total y el
        # camino. El camino es una lista de los nodos que se deben recorrer
        # PesototalDijkstra es el peso total del camino (suma de las distancias de las aristas)
        origen = airports.getAirportById(source_airport_id)['name']
        destino = airports.getAirportById(destination_airport_id)['name']

        camino_dijkstra = dijkstrav2(grafo, source_airport_id, destination_airport_id)
        print("Camino: ", camino_dijkstra)

        # peso_totalDijkstra = sum(nx.shortest_path_length(grafo, caminoDijkstra[1][i], caminoDijkstra[1][i+1], weight='weight') for i in range(len(caminoDijkstra[1])-1))
        # print("Peso total: ", peso_totalDijkstra)

        if not camino_dijkstra:
            folium_map = gp.cleanMap()
            folium_map.save('templates/mapDijkstra.html')
            
        else:
            # Se crea el mapa con el camino de Dijkstra
            folium_map = gp.drawMap(grafo, camino_dijkstra[1], airports)
            mapDijkstra = folium_map
            # Se guarda el mapa en un archivo html
            folium_map.save('templates/mapDijkstra.html')
            distanciaDijkstra = camino_dijkstra[0]

        # Realizando pruebas con el algoritmo de BFS
        # CaminoBFS es una lista de los nodos que se deben recorrer
        # PesototalBFS es el peso total del camino (suma de las distancias de las aristas)
        camino_bfs = bfs(grafo, source_airport_id, destination_airport_id)
        print("Camino: ", camino_bfs)
        # peso_totalBFS = sum(nx.shortest_path_length(grafo, caminoBFS[i], caminoBFS[i+1], weight='weight') for i in range(len(caminoBFS)-1))

        if not camino_bfs:
            folium_map = gp.cleanMap()
            folium_map.save('templates/mapBFS.html')

        else:
            # Se crea el mapa con el camino de BFS
            folium_map = gp.drawMap(grafo, camino_bfs, airports)
            mapBFS = folium_map
            # Se guarda el mapa en un archivo html
            folium_map.save('templates/mapBFS.html')
            distanciaBFS = sum(nx.shortest_path_length(grafo, camino_bfs[i], camino_bfs[i+1], weight='weight') for i in range(len(camino_bfs)-1))


        #return render_template('index.html', caminobfs=caminobfs, caminodijkstra=caminodijkstra)
        return render_template('index.html', 
                               origen=origen, 
                               destino=destino, 
                               distanciaBFS = distanciaBFS, 
                               distanciaDijkstra = distanciaDijkstra,
                               airportsList=airportsList)
    else:
        # response = make_response(render_template("index.html"))
        
        # response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        # response.headers["Pragma"] = "no-cache"
        # response.headers["Expires"] = "0"
        # return response
        return render_template('index.html', airportsList=airportsList)



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
