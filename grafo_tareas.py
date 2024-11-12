import heapq
from collections import deque

# Algoritmo de Dijkstra para la ruta más corta
def dijkstra(grafo, inicio, destino):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    prioridad = [(0, inicio)]
    camino = {nodo: None for nodo in grafo}
    
    while prioridad:
        distancia_actual, nodo_actual = heapq.heappop(prioridad)
        if nodo_actual == destino:
            break
        for vecino, peso in grafo[nodo_actual]:
            nueva_distancia = distancia_actual + peso
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                camino[vecino] = nodo_actual
                heapq.heappush(prioridad, (nueva_distancia, vecino))
    
    ruta = []
    paso = destino
    while paso:
        ruta.append(paso)
        paso = camino[paso]
    ruta.reverse()
    
    return distancias[destino], ruta

# Localidades con conexiones cortas (< 15 km)
def localidades_conexiones_cortas(grafo, limite=15):
    resultado = []
    for localidad, conexiones in grafo.items():
        if all(distancia < limite for _, distancia in conexiones):
            resultado.append(localidad)
    return resultado

# Verificar si el grafo es conexo
def es_conexo(grafo):
    visitados = set()
    def dfs(nodo):
        if nodo in visitados:
            return
        visitados.add(nodo)
        for vecino, _ in grafo[nodo]:
            dfs(vecino)
    
    nodos = list(grafo.keys())
    dfs(nodos[0])
    return len(visitados) == len(nodos)

# Rutas alternativas entre localidades (sin ciclos)
def rutas_sin_ciclos(grafo, inicio, destino):
    def dfs(nodo, destino, visitados, ruta_actual):
        if nodo == destino:
            rutas.append(ruta_actual[:])
            return
        for vecino, _ in grafo[nodo]:
            if vecino not in visitados:
                visitados.add(vecino)
                ruta_actual.append(vecino)
                dfs(vecino, destino, visitados, ruta_actual)
                ruta_actual.pop()
                visitados.remove(vecino)
    
    rutas = []
    dfs(inicio, destino, {inicio}, [inicio])
    return rutas

# Ruta más larga posible entre dos localidades sin ciclos
def ruta_mas_larga(grafo, inicio, destino):
    def dfs(nodo, destino, visitados, distancia_actual):
        if nodo == destino:
            return distancia_actual
        max_distancia = 0
        for vecino, peso in grafo[nodo]:
            if vecino not in visitados:
                visitados.add(vecino)
                max_distancia = max(max_distancia, dfs(vecino, destino, visitados, distancia_actual + peso))
                visitados.remove(vecino)
        return max_distancia
    
    return dfs(inicio, destino, {inicio}, 0)

# Representación del grafo
localidades = {
    "Madrid": [("Alcorcón", 13), ("Villaviciosa de Odón", 22), ("Alcalá de Henares", 35)],
    "Villanueva de la Cañada": [("Villaviciosa de Odón", 11), ("Boadilla del Monte", 7)],
    "Alcorcón": [("Madrid", 13), ("Móstoles", 5)],
    "Móstoles": [("Alcorcón", 5), ("Fuenlabrada", 8)],
    "Fuenlabrada": [("Móstoles", 8), ("Getafe", 10)],
    "Getafe": [("Fuenlabrada", 10), ("Madrid", 16)],
    "Villaviciosa de Odón": [("Madrid", 22), ("Villanueva de la Cañada", 11)],
    "Boadilla del Monte": [("Villanueva de la Cañada", 7), ("Madrid", 15)],
    "Alcalá de Henares": [("Madrid", 35), ("Torrejón de Ardoz", 15)],
    "Torrejón de Ardoz": [("Alcalá de Henares", 15), ("Madrid", 20)],
}

# Ejemplo de uso
print("Ruta más corta:")
distancia, ruta = dijkstra(localidades, "Madrid", "Getafe")
print(f"Distancia: {distancia} km, Ruta: {' -> '.join(ruta)}\n")

print("Localidades con conexiones cortas (< 15 km):")
print(localidades_conexiones_cortas(localidades, 15), "\n")

print("El grafo es conexo:" if es_conexo(localidades) else "El grafo no es conexo", "\n")

print("Rutas alternativas entre Madrid y Getafe:")
print(rutas_sin_ciclos(localidades, "Madrid", "Getafe"), "\n")

print("Ruta más larga posible entre Madrid y Getafe:")
print(f"Distancia: {ruta_mas_larga(localidades, 'Madrid', 'Getafe')} km")


