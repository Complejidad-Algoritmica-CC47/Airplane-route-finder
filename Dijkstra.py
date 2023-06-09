import networkx as nx
import matplotlib.pyplot as plt
import sympy as sp
import BFS

def dijkstrav2(G,u,v):

    if BFS.bfs(G, u, v) == None:
        print("No hay camino entre los nodos")
        return None
    
    else:
        print("Iniciando Dijkstra...")
        masinf=float('inf')
        nodos=list(G.nodes)
        distancias={w:masinf for w in nodos}
        fijos={w:False for w in nodos}
        padres={w:None for w in nodos}
        distancias[u]=0
        fijos[u]=True
        nuevo_fijo=u

        while not(all(fijos.values())):
            # Acualizar distancias.
            for w in G.neighbors(nuevo_fijo):
                if fijos[w]==False:
                    nueva_dist=distancias[nuevo_fijo]+G[nuevo_fijo][w]['weight']
                    if distancias[w]>nueva_dist:
                        distancias[w]=nueva_dist
                        padres[w]=nuevo_fijo

            # Encontrar el nuevo a fijar.
            mas_chica=masinf
            for w in nodos:
                if fijos[w]==False and distancias[w]<mas_chica:
                    optimo=w
                    mas_chica=distancias[w]
            nuevo_fijo=optimo
            fijos[nuevo_fijo]=True

            # Cuando fije el vértice final v, dar el camino.
            if nuevo_fijo==v:
                camino=[v]
                while camino[0]!=u:
                    camino=[padres[camino[0]]]+camino
                return distancias[v], camino