import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt

tareas = [{'numero': 0, 'duracion': 0, 'descripcion': 'Inicio', 'tareas_previas': []}]
task_numbers = set()
task_numbers.add(0)

def nuevaTarea_clicked():
    nuevoNumero = numeroTarea.get()
    nuevaDescripcion = descripcionTarea.get()
    nuevaDuracion = duracionTarea.get()
    nuevoNombre = str(nuevoNumero)
    nuevasPredecesoras = [x.strip() for x in tareasPredecesoras.get().split(',')]

    if validarEntradas(nuevoNumero, nuevaDescripcion, nuevaDuracion, nuevasPredecesoras):
        task_numbers.add(int(nuevoNumero))
        nuevasPredecesoras = [int(x) for x in nuevasPredecesoras]
        agregarTareaALista(nuevoNumero, nuevaDescripcion, nuevaDuracion, nuevasPredecesoras)
        return nuevoNumero, nuevaDescripcion, nuevaDuracion, nuevoNombre
    else:
        print("Entradas invalidas")

def validarEntradas(nuevoNumero, nuevaDescripcion, nuevaDuracion, nuevasPredecesoras):
    if not nuevoNumero.isnumeric() or nuevoNumero in task_numbers:
        return False
    if not nuevaDescripcion.isalpha() and len(nuevaDescripcion) > 50:
        return False
    if not nuevaDuracion.isnumeric():
        return False
    for i in nuevasPredecesoras:
        if not i.isnumeric():
            return False
    print(nuevasPredecesoras)
    return True

def agregarTareaALista(numero, descripcion, duracion, predecesoras):
    listaTareas.insert(tk.END, numero + " - " + descripcion)
    tareaAAgregar = {
        'numero': int(numero),
        'duracion': int(duracion),
        'descripcion': descripcion,
        'tareas_previas': predecesoras
    }

    print(listaTareas)

    tareas.append(tareaAAgregar)
    print(tareas)
    clearEntries()

# Cuando le das aqui va a mostrar el grafo con la ruta critica
# TODO: funcionalidad
def mostrarRuta_clicked():
    grafo = inicializarGrafo(tareas)
    mostrarGrafo(grafo)

# Cuando le das aqui va a borrar la tarea elejida
# TODO: funcionalidad y revisar que la tarea ingresada sea valida. Puede causar peos si se quita una que es predecesora de muchas
def borrarTarea_clicked():

    tarea_a_borrar = []
    tarea_a_borrar.append(int(tareaAEliminar.get()))
    global tareas
    tareas = [tarea for tarea in tareas if tarea['numero'] not in tarea_a_borrar]

# Esto solo resetea el grafo
# TODO: funcionalidad
def borrarProyecto_clicked():
    text = entry4.get()
    # Perform an action with the text from entry4
    print("Button 4 clicked with text:", text)


def clearEntries():
    numeroTarea.delete(0, 'end')
    descripcionTarea.delete(0, 'end')
    duracionTarea.delete(0, 'end')
    tareaAEliminar.delete(0, 'end')
    tareasPredecesoras.delete(0, 'end')

    numeroTarea.focus_set()

def calcularRutaCritica(grafo):
    # Calculo la ruta crítica
    rutaCritica = nx.dag_longest_path(grafo)

    # Calculo la duración total de la ruta crítica
    duracionTotal = sum(grafo.nodes[n]['duracion'] for n in rutaCritica)

    return rutaCritica, duracionTotal


def inicializarGrafo(tareas):
    # Creo un grafo dirigido
    grafo = nx.DiGraph()

    print(task_numbers)

    # Agrego las tareas como nodos al grafo
    for tarea in tareas:
        numero = tarea['numero']
        duracion = tarea['duracion']
        descripcion = tarea['descripcion']
        nombre = str(tarea['numero'])
        grafo.add_node(numero, 
                       duracion=duracion, 
                       descripcion=descripcion, 
                       nombre=nombre)

    # Agrego las aristas que representan las dependencias
    for tarea in tareas:
        tareasPrevias = tarea['tareas_previas']
        if not all(previa in task_numbers for previa in tareasPrevias):
            raise ValueError("Tarea predecesora invalida para tarea {}".format(tarea['numero']))
        
        for tareaPrevia in tareasPrevias:

            if nx.has_path(grafo, tareaPrevia, tarea['numero']):
                raise ValueError("Grafo invalido: hay un ciclo en las dependencias de las tareas")
            
            grafo.add_edge(tareaPrevia, tarea['numero'])

    return grafo

def mostrarGrafo(grafo):
    rutaCritica, duracion = calcularRutaCritica(grafo)

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


# Create the main window
window = tk.Tk()
window.title("Proyecto 2 - Ruta Critica")

# Create the text entries
numeroTarea = tk.Entry(window)
descripcionTarea = tk.Entry(window)
duracionTarea = tk.Entry(window)
tareaAEliminar = tk.Entry(window)
tareasPredecesoras = tk.Entry(window)

#  Titulos de las entradas
tituloNumeroTarea = tk.Label(window, text="Número de tarea:")
tituloDescripcionTarea = tk.Label(window, text="Descripción de tarea:")
tituloDuracionTarea = tk.Label(window, text="Duración de tarea:")
tituloTareaAEliminar = tk.Label(window, text="Tarea a eliminar:")
tituloTareasPredecesoras = tk.Label(window, text="Tareas predecesoras:")

# Lista de tareas
listaTareas = tk.Listbox(window, height=10, width=50)
tituloListaTareas = tk.Label(window, text="Lista de tareas:")

# Create the event buttons
nuevaTarea = tk.Button(window, text="Agregar tarea", command=nuevaTarea_clicked)
mostrarRuta = tk.Button(window, text="Mostrar Ruta", command=mostrarRuta_clicked)
borrarTarea = tk.Button(window, text="Borrar Tarea", command=borrarTarea_clicked)
borrarProyecto = tk.Button(window, text="Borrar Proyecto", command=borrarProyecto_clicked)

# Add the text entries and buttons to the window
tituloNumeroTarea.pack()
numeroTarea.pack()
tituloDescripcionTarea.pack()
descripcionTarea.pack()
tituloDuracionTarea.pack()
duracionTarea.pack()
tituloTareasPredecesoras.pack()
tareasPredecesoras.pack()

nuevaTarea.pack()
mostrarRuta.pack()
tituloListaTareas.pack()
listaTareas.pack()
tituloTareaAEliminar.pack()
tareaAEliminar.pack()
borrarTarea.pack()
borrarProyecto.pack()

# Start the main event loop
window.mainloop()