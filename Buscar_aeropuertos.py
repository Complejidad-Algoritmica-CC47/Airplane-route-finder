import csv
from unidecode import unidecode

def cambiar_texto(text):
    transliterated_text = unidecode(text)
    return transliterated_text

def guardar_aeropuertos(filename, lista):
    indice = 0
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if indice == 0:
                indice += 1
                continue

            aeropuerto = {     
                'id': row[0],         # id
                'name': cambiar_texto(row[1]).upper(),         # name
                'iata': row[4],          # codigo IATA
                'icao': row[5],          # codigo ICAO
                }
            
            lista.append(aeropuerto)
                


def buscar_id(input, lista):
    if len(input) == 3:
        for i in range(len(lista)):
            if lista[i]['iata'] == input:
                return lista[i]['id']
        print("!!!No se pudo encontrar un aeropuerto con ese codigo!")
    elif len(input) == 4:
        for i in range(len(lista)):
            if lista[i]['icao'] == input:
                return lista[i]['id']
        print("!!!No se pudo encontrar un aeropuerto con ese codigo!")
    else:
        for i in range(len(lista)):
            if lista[i]['name'] == input:
                return lista[i]['id']
        print("!!!No se pudo encontrar un aeropuerto con ese nombre!")

def todo_numeros(string):
    return string.isdigit()
