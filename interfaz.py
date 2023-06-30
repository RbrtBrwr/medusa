import tkinter as tk

# Cuando le das aqui va a sacar el numero, descripcion y duracion de las entradas de texto para pasarselo al grafo de rutCrit.py
# TODO: funcionalidad y revisar que las entradas sean validas.
# TODO: cuando se agrega una tarea nueva, agregarla a la lista de tareas. Solo numero y descripcion 
# TODO: OPCIONAL limitar la longitud de la descripcion?
def nuevaTarea_clicked():
    nuevoNumero = numeroTarea.get()
    nuevaDescripcion = descripcionTarea.get()
    nuevaDuracion = duracionTarea.get()
    nuevoNombre = str(nuevoNumero)

    if validarEntradas(nuevoNumero, nuevaDescripcion, nuevaDuracion, nuevoNombre):
        agregarTareaALista(nuevoNumero, nuevaDescripcion)
        return nuevoNumero, nuevaDescripcion, nuevaDuracion, nuevoNombre
    else:
        print("Entradas invalidas")

def validarEntradas(nuevoNumero, nuevaDescripcion, nuevaDuracion):
    if not nuevoNumero.isnumeric():
        return False
    if not nuevaDescripcion.isalpha() and len(nuevaDescripcion) > 50:
        return False
    if not nuevaDuracion.isnumeric():
        return False
    return True

def agregarTareaALista(numero, descripcion):
    listaTareas.insert(tk.END, numero + " - " + descripcion)

# Cuando le das aqui va a mostrar el grafo con la ruta critica
# TODO: funcionalidad
def mostrarRuta_clicked():
    text = entry2.get()
    # Perform an action with the text from entry2
    print("Button 2 clicked with text:", text)

# Cuando le das aqui va a borrar la tarea elejida
# TODO: funcionalidad y revisar que la tarea ingresada sea valida. Puede causar peos si se quita una que es predecesora de muchas
def borrarTarea_clicked():
    text = entry3.get()
    # Perform an action with the text from entry3
    print("Button 3 clicked with text:", text)

# Esto solo resetea el grafo
# TODO: funcionalidad
def borrarProyecto_clicked():
    text = entry4.get()
    # Perform an action with the text from entry4
    print("Button 4 clicked with text:", text)

# Create the main window
window = tk.Tk()
window.title("Proyecto 2 - Ruta Critica")

# Create the text entries
numeroTarea = tk.Entry(window)
descripcionTarea = tk.Entry(window)
duracionTarea = tk.Entry(window)
tareaAEliminar = tk.Entry(window)

#  Titulos de las entradas
tituloNumeroTarea = tk.Label(window, text="Número de tarea:")
tituloDescripcionTarea = tk.Label(window, text="Descripción de tarea:")
tituloDuracionTarea = tk.Label(window, text="Duración de tarea:")
tituloTareaAEliminar = tk.Label(window, text="Tarea a eliminar:")

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