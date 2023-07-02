import networkx as nx
import matplotlib.pyplot as plt

tareas = [
    {'numero': 1, 'duracion': 4, 'descripcion': 'Task 1', 'tareas_previas': []},
    {'numero': 2, 'duracion': 3, 'descripcion': 'Task 2', 'tareas_previas': [1]},
    {'numero': 3, 'duracion': 5, 'descripcion': 'Task 3', 'tareas_previas': [1]},
    {'numero': 4, 'duracion': 2, 'descripcion': 'Task 4', 'tareas_previas': [2, 3]},
    {'numero': 5, 'duracion': 3, 'descripcion': 'Task 5', 'tareas_previas': [4]},
    {'numero': 6, 'duracion': 1, 'descripcion': 'Task 6', 'tareas_previas': [4]},
    {'numero': 7, 'duracion': 2, 'descripcion': 'Task 7', 'tareas_previas': [5, 6]},
]

task_numbers = {1, 2, 3, 4, 5, 6, 7}

# def calcularRutaCritica(grafo):
#     # Calculo la ruta crítica
#     rutaCritica = nx.dag_longest_path(grafo)

#     # Calculo la duración total de la ruta crítica
#     duracionTotal = sum(grafo.nodes[n]['duracion'] for n in rutaCritica)

#     return rutaCritica, duracionTotal


def inicializarGrafo(diccionarioTareas):
    # Creo un grafo dirigido
    grafo = nx.DiGraph()

    # Agrego las tareas como nodos al grafo
    for tarea in diccionarioTareas.keys():
        numero = tarea
        duracion = diccionarioTareas[tarea]['duracion']
        descripcion = diccionarioTareas[tarea]['descripcion']
        nombre = str(tarea)
        grafo.add_node(numero, 
                       duracion=duracion, 
                       descripcion=descripcion, 
                       nombre=nombre)

    # Agrego las aristas que representan las dependencias
    for tarea in tareas:
        tareasPrevias = tarea['tareas_previas']
        if not all(previa in task_numbers for previa in tareasPrevias):
            raise ValueError("Invalid preceding task number(s) for task {}".format(tarea['numero']))
        
        for tareaPrevia in tareasPrevias:

            if nx.has_path(grafo, tareaPrevia, tarea['numero']):
                raise ValueError("Invalid graph: loop detected in task dependencies")
            
            grafo.add_edge(tareaPrevia, tarea['numero'])

    return grafo

def mostrarGrafo(grafo, diccionarioTareas):
    # earliestStart = calcularEarlyStart(grafo, diccionarioTareas)
    # latestStart = calcularLateStart(grafo, earliestStart, diccionarioTareas)
    # rutaCritica, duracion = calcularRutaCritica(grafo, earliestStart, latestStart)

    # posiciono los nodos
    posiciones = nx.planar_layout(grafo)

    # Dibujo los nodos
    colorNodos = ['lightblue' if nodo not in rutaCritica else 'green' for nodo in grafo.nodes()]
    nx.draw_networkx_nodes(grafo, posiciones, node_size=500, node_color=colorNodos)
    
    # Dibujo las aristas
    colorAristas = ['black' if (u, v) not in grafo.edges() or u not in rutaCritica or v not in rutaCritica else 'green' for u, v in grafo.edges()]
    nx.draw_networkx_edges(grafo, posiciones, arrows=True, edge_color=colorAristas)

    # Dibujo las etiquetas de los nodos
    etiquetas = nx.get_node_attributes(grafo, 'nombre')
    nx.draw_networkx_labels(grafo, posiciones, etiquetas, font_size=10)

    # Muestro el gráfico
    plt.title("Ruta Crítica de Tareas")
    # Muestro la duracion en el gráfico
    plt.text(0.5, 0.5, "Duracion: " + str(duracion), horizontalalignment='right', verticalalignment='bottom')
    plt.axis('off')
    plt.show()

def getStartFinishCandidates(diccionarioTareas):
    startCandidates = []
    endCandidates = []
    for tarea in diccionarioTareas.keys():
        if diccionarioTareas[tarea]['tareas_previas'] == []:
            startCandidates.append(tarea)
        
        isCandidate = True
        for i in diccionarioTareas:
            if tarea in i['tareas_previas']:
                isCandidate = False
                break
        if isCandidate:
            endCandidates.append(tarea)
    return startCandidates, endCandidates

def setStartFinish(diccionarioTareas):
    startCandidates, endCandidates = getStartFinishCandidates(diccionarioTareas)
    startIndex = 998
    endIndex = 999
    if len(startCandidates) > 1:
        # Agregar una nueva tarea que va a ser el inicio
        diccionarioTareas[998] = {'numero': 998, 'duracion': 0, 'descripcion': 'Start', 'tareas_previas': []}
        for i in startCandidates:
            diccionarioTareas[i]['tareas_previas'].append(998)
    else:
        startIndex = startCandidates[0]
    if len(endCandidates) > 1:
        # Agregar una nueva tarea que va a ser el fin
        diccionarioTareas[999] = {'numero': 999, 'duracion': 0, 'descripcion': 'End', 'tareas_previas': []}
        for i in endCandidates:
            diccionarioTareas[999]['tareas_previas'].append(i)
    else:
        endIndex = endCandidates[0]
    
    return inicializarGrafo(diccionarioTareas), startIndex, endIndex

def calcularRutaCritica(diccionarioTareas, startIndex, endIndex):
    # {nroNodo: {ES: 0, EF: 0, LS: 0, LF: 0}}
    startFinish = forwardPass(diccionarioTareas)
    startFinish = backwardPass(diccionarioTareas, startFinish)

def forwardPass(diccionarioTareas, startIndex, endIndex):
    startFinish = {}
    startFinish[startIndex] = {'ES': 0, 'EF': diccionarioTareas[startIndex]['duracion'], 'LS': 0, 'LF': 0}
    

# def calcularEarlyStart(grafo, mapaTareas):
#     earlyStart = {}
#     for nodo in nx.topological_sort(grafo):
#         maxEarlyStart = 0
#         for predecesor in mapaTareas[nodo]['tareas_previas']:
#             maxEarlyStart = max(maxEarlyStart, earlyStart[predecesor] + mapaTareas[predecesor]['duracion'])
#         earlyStart[nodo] = maxEarlyStart
#     return earlyStart

# def calcularLateStart(earlyStart, mapaTareas):
#     lateStart = {}
#     # A cada nodo le asigno lo mas tarde que puede empezar
#     for nodo in mapaTareas.keys():

#         predecesores = mapaTareas[nodo]['tareas_previas']
#         duracionPredecesores = [mapaTareas[predecesor]['duracion'] for predecesor in predecesores]
#         lateStart[nodo] = earlyStart[max(duracionPredecesores, default=0)]
#     return lateStart

# def calcularRutaCritica(grafo, earliest, latest):
#     rutaCritica = []
#     duracionRutaCritica = 0
#     for nodo in grafo.nodes:
#         if earliest[nodo] == latest[nodo]:
#             rutaCritica.append(nodo)
#             duracionRutaCritica += grafo.nodes[nodo]['duracion']
#     return rutaCritica, duracionRutaCritica

# grafo = inicializarGrafo(tareas)
# mostrarGrafo(grafo)