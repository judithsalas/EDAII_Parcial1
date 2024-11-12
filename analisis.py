import heapq
import time
from memory_profiler import memory_usage

# Función Dijkstra para encontrar la ruta más corta
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

# Ruta más larga posible entre localidades sin ciclos
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

# Generar un grafo de prueba
def generar_grafo(tamano_nodos, conexiones_por_nodo):
    grafo = {f"Localidad_{i}": [] for i in range(tamano_nodos)}
    for i in range(tamano_nodos):
        for j in range(1, conexiones_por_nodo + 1):
            if i + j < tamano_nodos:
                grafo[f"Localidad_{i}"].append((f"Localidad_{i + j}", j))
    return grafo

# Medir tiempo de ejecución
def medir_tiempo(func, *args):
    inicio = time.time()
    func(*args)
    fin = time.time()
    return fin - inicio

# Medir consumo de memoria
def medir_memoria(func, *args):
    uso_memoria = memory_usage((func, args), interval=0.1)
    return max(uso_memoria) - min(uso_memoria)

# Ejecutar análisis para una función específica
def analizar_funcion(func, nombre_funcion, grafo, inicio=None, destino=None):
    if func == es_conexo:  # Si la función es es_conexo, solo necesita el grafo
        tiempo = medir_tiempo(func, grafo)
        memoria = medir_memoria(func, grafo)
    else:  # Las otras funciones necesitan inicio y destino
        tiempo = medir_tiempo(func, grafo, inicio, destino)
        memoria = medir_memoria(func, grafo, inicio, destino)
    
    print(f"--- {nombre_funcion} ---")
    print(f"Tiempo de ejecución: {tiempo:.6f} segundos")
    print(f"Consumo de memoria: {memoria:.2f} MiB\n")


# Ejecutar análisis para todas las funciones
if __name__ == "__main__":
    print("Generando grafo de prueba...")
    grafo = generar_grafo(100, 3)  # Grafo con 100 nodos y 3 conexiones por nodo

    print("Analizando Dijkstra...")
    analizar_funcion(dijkstra, "Dijkstra", grafo, "Localidad_0", "Localidad_99")

    print("Analizando es_conexo...")
    analizar_funcion(es_conexo, "es_conexo", grafo)

    print("Analizando rutas_sin_ciclos...")
    analizar_funcion(rutas_sin_ciclos, "rutas_sin_ciclos", grafo, "Localidad_0", "Localidad_99")

    print("Analizando ruta_mas_larga...")
    analizar_funcion(ruta_mas_larga, "ruta_mas_larga", grafo, "Localidad_0", "Localidad_99")
