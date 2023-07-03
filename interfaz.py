import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
import rutCrit as rc

diccionarioTareas = {}
def revisarNoInterdependencia(numeroTareaNueva, predecesores):
    if int(numeroTareaNueva) in predecesores:
        return True
    
    for i in predecesores:
        if i in diccionarioTareas.keys():
            siguientesPredecesores = diccionarioTareas[i]['tareas_previas']
            if revisarNoInterdependencia(numeroTareaNueva, siguientesPredecesores):
                return True
        
    return False

# Inicializo el grafo que es el que voy a usar


def nuevaTarea_clicked():
    nuevoNumero = numeroTarea.get()
    nuevaDescripcion = descripcionTarea.get()
    nuevaDuracion = duracionTarea.get()
    nuevoNombre = str(nuevoNumero)
    nuevasPredecesoras = [x.strip() for x in tareasPredecesoras.get().split(',')]

    if validarEntradas(nuevoNumero, nuevaDescripcion, nuevaDuracion, nuevasPredecesoras):
        task_numbers.add(int(nuevoNumero))
        nuevasPredecesoras = [int(x) for x in nuevasPredecesoras if x != '']
        agregarTareaALista(nuevoNumero, nuevaDescripcion, nuevaDuracion, nuevasPredecesoras)
        print(nuevoNumero)
        print(nuevasPredecesoras)
        if revisarNoInterdependencia(nuevoNumero, nuevasPredecesoras):
            eliminarTarea(int(nuevoNumero))
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
    if nuevasPredecesoras == ['']:
        return True
    for i in nuevasPredecesoras:
        if not i.isnumeric():
            return False
        
    return True


def agregarTareaALista(numero, descripcion, duracion, predecesoras):
    if not str(predecesoras) == '[]':
        listaTareas.insert(tk.END, numero + " - " + descripcion + " - " + duracion + " - " + str(predecesoras))
    else:
        listaTareas.insert(tk.END, numero + " - " + descripcion + " - " + duracion)

    tareaAAgregar = {
        'duracion': int(duracion),
        'descripcion': descripcion,
        'tareas_previas': predecesoras
    }

    diccionarioTareas[int(numero)] = tareaAAgregar
    # tareas.append(tareaAAgregar)
    clearEntries()

# Cuando le das aqui va a mostrar el grafo con la ruta critica
def mostrarRuta_clicked():
    grafo = rc.setStartFinish(diccionarioTareas)
    rc.mostrarGrafo(grafo)

# Cuando le das aqui va a borrar la tarea elejida
def borrarTarea_clicked():
    if tareaAEliminar.get().isnumeric():
        # Preguntar si desea eliminar tarea
        eliminarTareaDeLista(int(tareaAEliminar.get())) 
        eliminar = tareaAEliminar.get()
        eliminarTarea(int(eliminar))
        print("tarea " + eliminar + " eliminada")
        # TODO: mostrar mensaje de que se elimino la tarea, no se por que no sirve el messagebox
        # tk.messagebox.showinfo("Tarea eliminada", "La tarea " + eliminar + " ha sido eliminada")
    tareaAEliminar.delete(0, 'end')

def eliminarTareaDeLista(numeroEliminar):
    for i in range(listaTareas.size()):
        if listaTareas.get(i).split(" - ")[0] == str(numeroEliminar):
            listaTareas.delete(i)

def eliminarTarea(numeroEliminar):
    del diccionarioTareas[numeroEliminar]
    eliminarDePredecesores(numeroEliminar)

def eliminarDePredecesores(numeroEliminar):
    for i in diccionarioTareas.keys():
        diccionarioTareas[i]['tareas_previas'] = [x for x in diccionarioTareas[i]['tareas_previas'] if x != numeroEliminar]


# Esto solo resetea el grafo
# TODO: funcionalidad
def borrarProyecto_clicked():
    confirm = input("¿Está seguro que desea borrar el proyecto? (y/n): ") == 'y' or input("¿Está seguro que desea borrar el proyecto? (y/n): ") == 'Y'
    resetearTareas(diccionarioTareas)



def resetearTareas(tareas):
    tareas = {0: {'duracion': 0, 'descripcion': 'Inicio', 'tareas_previas': []}}

def clearEntries():
    numeroTarea.delete(0, 'end')
    descripcionTarea.delete(0, 'end')
    duracionTarea.delete(0, 'end')
    tareaAEliminar.delete(0, 'end')
    tareasPredecesoras.delete(0, 'end')

    numeroTarea.focus_set()

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
listaTareas.insert(tk.END, "Numero - Descripcion - Duracion - Predecesoras")
tituloTareaAEliminar.pack()
tareaAEliminar.pack()
borrarTarea.pack()
borrarProyecto.pack()

testTareasConInicioYFin = {1:{'duracion': 4, 'descripcion': 'Tarea 1', 'tareas_previas': []},
              2:{'duracion': 2, 'descripcion': 'Tarea 2', 'tareas_previas': [1]},
              3:{'duracion': 5, 'descripcion': 'Tarea 3', 'tareas_previas': [1]},
                4:{'duracion': 3, 'descripcion': 'Tarea 4', 'tareas_previas': [1]},
                5:{'duracion': 3, 'descripcion': 'Tarea 5', 'tareas_previas': [2, 3]},
                6:{'duracion': 2, 'descripcion': 'Tarea 6', 'tareas_previas': [3]},
                7:{'duracion': 1, 'descripcion': 'Tarea 7', 'tareas_previas': [4, 5, 6]}
}

tareas = [
    {'numero': 1, 'duracion': 4, 'descripcion': 'Task 1', 'tareas_previas': []},
    {'numero': 2, 'duracion': 3, 'descripcion': 'Task 2', 'tareas_previas': [1]},
    {'numero': 3, 'duracion': 5, 'descripcion': 'Task 3', 'tareas_previas': [1]},
    {'numero': 4, 'duracion': 2, 'descripcion': 'Task 4', 'tareas_previas': [2, 3]},
    {'numero': 5, 'duracion': 3, 'descripcion': 'Task 5', 'tareas_previas': [4]},
    {'numero': 6, 'duracion': 1, 'descripcion': 'Task 6', 'tareas_previas': [4]},
    {'numero': 7, 'duracion': 2, 'descripcion': 'Task 7', 'tareas_previas': [5, 6]},
]

def test():
    G, critical_path, total_duration = rc.calculate_critical_path(tareas)

    # Print the critical path
    print("Critical Path:")
    path = " -> ".join(critical_path)
    print(path)

    print(f"Total Duration: {total_duration} units")

    # Draw the graph
    rc.draw_graph(G, tareas, critical_path)

botonPrueba = tk.Button(window, text="Prueba", command=test)
botonPrueba.pack()

# Start the main event loop
window.mainloop()