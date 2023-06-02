import networkx as nx
import matplotlib.pyplot as plt
import sympy as sp

def dijkstrav2(G,u,v):
    masinf=float('inf')
    vertices=list(G.nodes)
    distancias={w:masinf for w in vertices}
    fijos={w:False for w in vertices}
    padres={w:None for w in vertices}
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
        for w in vertices:
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