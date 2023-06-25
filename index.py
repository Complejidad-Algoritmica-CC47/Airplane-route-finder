from flask import Flask, render_template, request, redirect, url_for, make_response, send_from_directory
from Dijkstra import dijkstrav2
from BFS import bfs
import networkx as nx 
import Graph as gp 
import csv
app = Flask(__name__)

# Se crea el grafo (con los id de los aeropuertos como
# nodos y con las rutas como aristas) y se cargan los aeropuertos
grafo = nx.Graph()
grafo, airports, airportsListFull = gp.initGraph()

mapDijkstra = gp.cleanMap()
mapBFS = gp.cleanMap()

# Ruta principal del servidor
@app.route('/', methods=['GET'])
def index():
    airportsList = airportsListFull          
    return render_template('index.html', airportsList=airportsList)

# Ruta principal del servidor
@app.route('/', methods=['POST'])
def busqueda():
    origen = 'Pendiente'
    destino = 'Pendiente'
    distanciaDijkstra = 0
    distanciaBFS = 0
    airportsList = airportsListFull
    pathNotExists = False

    # Algoritmo de Dijkstra y BFS
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
        
        origen = airports.getAirportById(source_airport_id)['name']
        destino = airports.getAirportById(destination_airport_id)['name']

        camino_dijkstra = dijkstrav2(grafo, source_airport_id, destination_airport_id)
        print("Camino: ", camino_dijkstra)

        if not camino_dijkstra:
            folium_map = gp.cleanMap()
            folium_map.save('templates/mapDijkstra.html')
            pathNotExists = True
            
        else:
            # Se crea el mapa con el camino de Dijkstra
            folium_map = gp.drawMap(grafo, camino_dijkstra[1], airports)
            mapDijkstra = folium_map
            # Se guarda el mapa en un archivo html
            folium_map.save('templates/mapDijkstra.html')
            distanciaDijkstra = round(camino_dijkstra[0], 2)

        camino_bfs = bfs(grafo, source_airport_id, destination_airport_id)
        print("Camino: ", camino_bfs)

        if not camino_bfs:
            folium_map = gp.cleanMap()
            folium_map.save('templates/mapBFS.html')
            pathNotExists = True

        else:
            # Se crea el mapa con el camino de BFS
            folium_map = gp.drawMap(grafo, camino_bfs, airports)
            mapBFS = folium_map
            # Se guarda el mapa en un archivo html
            folium_map.save('templates/mapBFS.html')
            distanciaBFS = round(sum(nx.shortest_path_length(grafo, camino_bfs[i], camino_bfs[i+1], weight='weight') for i in range(len(camino_bfs)-1)), 2)

        return render_template('index.html', 
                               origen=origen, 
                               destino=destino, 
                               distanciaBFS = distanciaBFS, 
                               distanciaDijkstra = distanciaDijkstra,
                               airportsList=airportsList,
                               pathNotExists = pathNotExists)
    else:
        return render_template('index.html', airportsList=airportsList)



# Se renderiza el mapa de Dijkstra
# Se llama a esta ruta desde el index.html para mostrar el mapa
@app.route('/mapDijkstra')
def mapDijkstra():
    return send_from_directory('templates', 'mapDijkstra.html')


# Se renderiza el mapa de BFS
# Se llama a esta ruta desde el index.html para mostrar el mapa
@app.route('/mapBFS')
def mapBFS():
    return send_from_directory('templates', 'mapBFS.html')

@app.context_processor
def inject_version():
    import time
    return {'version': int(time.time())}

if __name__ == "__main__":
    app.run(debug=True)
