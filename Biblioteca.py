import json
import datetime

#Almacenamiento
db_files = {
    "alumnos": "alumnos.txt",
    "prestamos": "prestamos.txt",
    "libros": "libros.txt",
    "sancionados": "sancionados.txt"
}

#Para cargar los datos desde archivos
def cargar_datos(nombre):
    try:
        with open(db_files[nombre], "r") as file:
            return json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        return {} if nombre != "sancionados" else []
    
#Para guardas datos en los archivos
def guardar_datos(nombre, datos):
    with open(db_files[nombre], "w") as file:
        json.dump(datos, file, indent=4)
        
#Base de datos cargada
db = {k: cargar_datos(k) for k in db_files}

def registrar_alumno():
    cedula = input("Ingrese la cedula:")
    if cedula in db["alumnos"]:
        print("alumno ya registrado")
        return
    db["alumnos"][cedula] = input("ingrese el nombre:")
    guardar_datos("alumnos", db["alumnos"])
    print("alumno registrado")
    

                  