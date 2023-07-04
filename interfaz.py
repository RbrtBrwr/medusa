import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
import rutCrit as rc

tasks = []
task_numbers = set()

def revisarNoInterdependencia(numeroTareaNueva, predecesores):
    if int(numeroTareaNueva) in predecesores:
        return True
    
    for i in predecesores:
        for task in tasks:
            if i == task['numero']:
                siguientesPredecesores = ['tareas_previas']
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
        messagebox.showerror("Entradas invalidas")
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
        'numero': int(numero),
        'duracion': int(duracion),
        'descripcion': descripcion,
        'tareas_previas': predecesoras
    }

    tasks.append(tareaAAgregar)
    clearEntries()

# Cuando le das aqui va a mostrar el grafo con la ruta critica
def mostrarRuta_clicked():
    G, critical_path, total_duration, earliest_start, earliest_finish, latest_start, latest_finish, slack = rc.calculate_critical_path(tasks)

    # Print the critical path
    print("Critical Path:")
    path = " -> ".join(critical_path)
    print(path)

    print(f"Total Duration: {total_duration} units")

    # Draw the graph
    rc.draw_graph(G, tasks, critical_path, earliest_start, earliest_finish, latest_start, latest_finish, slack)

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
    global tasks
    tasks = [task for task in tasks if task['numero'] != numeroEliminar]


# Esto solo resetea el grafo
# TODO: funcionalidad
def borrarProyecto_clicked():
    resetearTareas()



def resetearTareas():
    global tasks
    tasks = []
    for i in range(listaTareas.size()):
        print(i)
        listaTareas.delete(i)

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
    G, critical_path, total_duration, earliest_start, earliest_finish, latest_start, latest_finish, slack = rc.calculate_critical_path(tareas)

    # Print the critical path
    print("Critical Path:")
    path = " -> ".join(critical_path)
    print(path)

    print(f"Total Duration: {total_duration} units")

    # Draw the graph
    rc.draw_graph(G, tareas, critical_path, earliest_start, earliest_finish, latest_start, latest_finish, slack)

botonPrueba = tk.Button(window, text="Prueba", command=test)
botonPrueba.pack()

# Start the main event loop
window.mainloop()