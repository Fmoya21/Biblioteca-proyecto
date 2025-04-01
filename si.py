import os
from datetime import datetime, timedelta

# Archivos de datos
ARCHIVO_ALUMNOS = "alumnos.txt"
ARCHIVO_LIBROS = "libros.txt"
ARCHIVO_PRESTAMOS = "prestamos.txt"
ARCHIVO_SANCIONES = "sanciones.txt"

# Inicializar archivos si no existen
def inicializar_archivos():
    for archivo in [ARCHIVO_ALUMNOS, ARCHIVO_LIBROS, ARCHIVO_PRESTAMOS, ARCHIVO_SANCIONES]:
        if not os.path.exists(archivo):
            open(archivo, 'w').close()

# Funciones de utilidad
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Debe ingresar un número entero.")

def leer_fecha(mensaje):
    while True:
        fecha_str = input(mensaje + " (DD/MM/AAAA): ")
        try:
            return datetime.strptime(fecha_str, "%d/%m/%Y").date()
        except ValueError:
            print("Formato de fecha incorrecto. Use DD/MM/AAAA.")

# Funciones para manejar alumnos
def registrar_alumno():
    limpiar_pantalla()
    print("\n--- REGISTRAR NUEVO ALUMNO ---")
    cedula = input("Cédula del alumno: ")
    
    # Verificar si el alumno ya existe
    with open(ARCHIVO_ALUMNOS, 'r') as f:
        for linea in f:
            if linea.startswith(cedula + "|"):
                print("Error: Ya existe un alumno con esta cédula.")
                input("Presione Enter para continuar...")
                return
    
    nombre = input("Nombre completo: ")
    carrera = input("Carrera: ")
    
    with open(ARCHIVO_ALUMNOS, 'a') as f:
        f.write(f"{cedula}|{nombre}|{carrera}\n")
    
    print("\nAlumno registrado exitosamente!")
    input("Presione Enter para continuar...")

def listar_alumnos():
    limpiar_pantalla()
    print("\n--- LISTA DE ALUMNOS ---")
    with open(ARCHIVO_ALUMNOS, 'r') as f:
        for linea in f:
            cedula, nombre, carrera = linea.strip().split('|')
            print(f"Cédula: {cedula}, Nombre: {nombre}, Carrera: {carrera}")
    input("\nPresione Enter para continuar...")

# Funciones para manejar libros
def registrar_libro():
    limpiar_pantalla()
    print("\n--- REGISTRAR NUEVO LIBRO ---")
    codigo = input("Código del libro: ")
    
    # Verificar si el libro ya existe
    with open(ARCHIVO_LIBROS, 'r') as f:
        for linea in f:
            if linea.startswith(codigo + "|"):
                print("Error: Ya existe un libro con este código.")
                input("Presione Enter para continuar...")
                return
    
    titulo = input("Título: ")
    autor = input("Autor: ")
    categoria = input("Categoría: ")
    cantidad = leer_entero("Cantidad disponible: ")
    
    with open(ARCHIVO_LIBROS, 'a') as f:
        f.write(f"{codigo}|{titulo}|{autor}|{categoria}|{cantidad}\n")
    
    print("\nLibro registrado exitosamente!")
    input("Presione Enter para continuar...")

def listar_libros():
    limpiar_pantalla()
    print("\n--- LIBROS DISPONIBLES ---")
    with open(ARCHIVO_LIBROS, 'r') as f:
        for linea in f:
            codigo, titulo, autor, categoria, cantidad = linea.strip().split('|')
            print(f"Código: {codigo}, Título: {titulo}, Autor: {autor}, Categoría: {categoria}, Disponibles: {cantidad}")
    input("\nPresione Enter para continuar...")

# Funciones para préstamos
def registrar_prestamo():
    limpiar_pantalla()
    print("\n--- REGISTRAR PRÉSTAMO ---")
    
    # Verificar alumno
    cedula = input("Cédula del alumno: ")
    alumno_encontrado = False
    with open(ARCHIVO_ALUMNOS, 'r') as f:
        for linea in f:
            if linea.startswith(cedula + "|"):
                alumno_encontrado = True
                break
    
    if not alumno_encontrado:
        print("Error: No existe un alumno con esta cédula.")
        input("Presione Enter para continuar...")
        return
    
    # Verificar sanción
    fecha_actual = datetime.now().date()
    with open(ARCHIVO_SANCIONES, 'r') as f:
        for linea in f:
            datos = linea.strip().split('|')
            if datos[0] == cedula and datetime.strptime(datos[2], "%d/%m/%Y").date() >= fecha_actual:
                print(f"Error: El alumno está sancionado hasta {datos[2]}")
                input("Presione Enter para continuar...")
                return
    
    # Verificar libro
    codigo_libro = input("Código del libro: ")
    libro_encontrado = False
    with open(ARCHIVO_LIBROS, 'r') as f:
        lineas = f.readlines()
    
    for i, linea in enumerate(lineas):
        datos = linea.strip().split('|')
        if datos[0] == codigo_libro:
            libro_encontrado = True
            if int(datos[4]) <= 0:
                print("Error: No hay ejemplares disponibles de este libro.")
                input("Presione Enter para continuar...")
                return
            
            # Actualizar cantidad disponible
            datos[4] = str(int(datos[4]) - 1)
            lineas[i] = '|'.join(datos) + '\n'
            break
    
    if not libro_encontrado:
        print("Error: No existe un libro con este código.")
        input("Presione Enter para continuar...")
        return
    
    # Registrar préstamo
    fecha_prestamo = datetime.now().date()
    fecha_devolucion = fecha_prestamo + timedelta(days=3)
    
    with open(ARCHIVO_PRESTAMOS, 'a') as f:
        f.write(f"{cedula}|{codigo_libro}|{fecha_prestamo.strftime('%d/%m/%Y')}|{fecha_devolucion.strftime('%d/%m/%Y')}\n")
    
    # Actualizar archivo de libros
    with open(ARCHIVO_LIBROS, 'w') as f:
        f.writelines(lineas)
    
    print("\nPréstamo registrado exitosamente!")
    print(f"Fecha de devolución: {fecha_devolucion.strftime('%d/%m/%Y')}")
    input("Presione Enter para continuar...")

def listar_prestamos_activos():
    limpiar_pantalla()
    print("\n--- PRÉSTAMOS ACTIVOS ---")
    fecha_actual = datetime.now().date()
    
    with open(ARCHIVO_PRESTAMOS, 'r') as f_prestamos, \
         open(ARCHIVO_ALUMNOS, 'r') as f_alumnos:
        
        prestamos = [linea.strip().split('|') for linea in f_prestamos]
        alumnos = {linea.split('|')[0]: linea.split('|')[1] for linea in f_alumnos}
        
        for prestamo in prestamos:
            cedula, codigo_libro, fecha_p, fecha_dev = prestamo
            fecha_devolucion = datetime.strptime(fecha_dev, "%d/%m/%Y").date()
            
            estado = "En plazo" if fecha_actual <= fecha_devolucion else "Atrasado"
            nombre_alumno = alumnos.get(cedula, "Desconocido")
            
            print(f"Alumno: {nombre_alumno} ({cedula}), Libro: {codigo_libro}")
            print(f"Fecha préstamo: {fecha_p}, Fecha devolución: {fecha_dev}, Estado: {estado}\n")
    
    input("\nPresione Enter para continuar...")

# Funciones para sanciones
def listar_alumnos_sancionados():
    limpiar_pantalla()
    print("\n--- ALUMNOS SANCIONADOS ---")
    fecha_actual = datetime.now().date()
    
    with open(ARCHIVO_SANCIONES, 'r') as f_sanciones, \
         open(ARCHIVO_ALUMNOS, 'r') as f_alumnos:
        
        sanciones = [linea.strip().split('|') for linea in f_sanciones]
        alumnos = {linea.split('|')[0]: linea.split('|')[1] for linea in f_alumnos}
        
        for sancion in sanciones:
            cedula, motivo, fecha_fin = sancion
            fecha_fin_sancion = datetime.strptime(fecha_fin, "%d/%m/%Y").date()
            
            if fecha_fin_sancion >= fecha_actual:
                nombre_alumno = alumnos.get(cedula, "Desconocido")
                print(f"Alumno: {nombre_alumno} ({cedula})")
                print(f"Motivo: {motivo}, Sancionado hasta: {fecha_fin}\n")
    
    input("\nPresione Enter para continuar...")

# Función para renovar préstamo
def renovar_prestamo():
    limpiar_pantalla()
    print("\n--- RENOVAR PRÉSTAMO ---")
    cedula = input("Cédula del alumno: ")
    codigo_libro = input("Código del libro: ")
    
    # Buscar préstamo
    with open(ARCHIVO_PRESTAMOS, 'r') as f:
        lineas = f.readlines()
    
    encontrado = False
    for i, linea in enumerate(lineas):
        datos = linea.strip().split('|')
        if datos[0] == cedula and datos[1] == codigo_libro:
            encontrado = True
            fecha_actual = datetime.now().date()
            fecha_devolucion = datetime.strptime(datos[3], "%d/%m/%Y").date()
            
            if fecha_actual > fecha_devolucion:
                print("Error: No se puede renovar un préstamo atrasado.")
                input("Presione Enter para continuar...")
                return
            
            # Actualizar fecha de devolución
            nueva_fecha = fecha_actual + timedelta(days=3)
            datos[3] = nueva_fecha.strftime("%d/%m/%Y")
            lineas[i] = '|'.join(datos) + '\n'
            break
    
    if not encontrado:
        print("Error: No se encontró el préstamo especificado.")
        input("Presione Enter para continuar...")
        return
    
    # Actualizar archivo de préstamos
    with open(ARCHIVO_PRESTAMOS, 'w') as f:
        f.writelines(lineas)
    
    print("\nPréstamo renovado exitosamente!")
    print(f"Nueva fecha de devolución: {nueva_fecha.strftime('%d/%m/%Y')}")
    input("Presione Enter para continuar...")

# Función para devolución
def registrar_devolucion():
    limpiar_pantalla()
    print("\n--- REGISTRAR DEVOLUCIÓN ---")
    cedula = input("Cédula del alumno: ")
    codigo_libro = input("Código del libro: ")
    
    # Buscar y eliminar préstamo
    with open(ARCHIVO_PRESTAMOS, 'r') as f:
        lineas = f.readlines()
    
    prestamo_encontrado = False
    nuevas_lineas = []
    prestamo_data = None
    
    for linea in lineas:
        datos = linea.strip().split('|')
        if datos[0] == cedula and datos[1] == codigo_libro:
            prestamo_encontrado = True
            prestamo_data = datos
        else:
            nuevas_lineas.append(linea)
    
    if not prestamo_encontrado:
        print("Error: No se encontró el préstamo especificado.")
        input("Presione Enter para continuar...")
        return
    
    # Verificar si está atrasado para aplicar sanción
    fecha_actual = datetime.now().date()
    fecha_devolucion = datetime.strptime(prestamo_data[3], "%d/%m/%Y").date()
    
    if fecha_actual > fecha_devolucion:
        fecha_fin_sancion = fecha_actual + timedelta(days=7)
        with open(ARCHIVO_SANCIONES, 'a') as f:
            f.write(f"{cedula}|Retraso en devolución|{fecha_fin_sancion.strftime('%d/%m/%Y')}\n")
        print("Alumno sancionado por 7 días por retraso en la devolución.")
    
    # Actualizar archivo de préstamos
    with open(ARCHIVO_PRESTAMOS, 'w') as f:
        f.writelines(nuevas_lineas)
    
    # Actualizar cantidad de libros disponibles
    with open(ARCHIVO_LIBROS, 'r') as f:
        lineas_libros = f.readlines()
    
    for i, linea in enumerate(lineas_libros):
        datos = linea.strip().split('|')
        if datos[0] == codigo_libro:
            datos[4] = str(int(datos[4]) + 1)
            lineas_libros[i] = '|'.join(datos) + '\n'
            break
    
    with open(ARCHIVO_LIBROS, 'w') as f:
        f.writelines(lineas_libros)
    
    print("\nDevolución registrada exitosamente!")
    input("Presione Enter para continuar...")

# Menú principal
def menu_principal():
    inicializar_archivos()
    while True:
        limpiar_pantalla()
        print("\n=== SISTEMA DE GESTIÓN DE BIBLIOTECA ===")
        print("1. Registrar nuevo alumno")
        print("2. Registrar nuevo libro")
        print("3. Registrar préstamo")
        print("4. Listar préstamos activos")
        print("5. Listar libros disponibles")
        print("6. Listar alumnos sancionados")
        print("7. Renovar préstamo")
        print("8. Registrar devolución")
        print("9. Listar todos los alumnos")
        print("0. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            registrar_alumno()
        elif opcion == "2":
            registrar_libro()
        elif opcion == "3":
            registrar_prestamo()
        elif opcion == "4":
            listar_prestamos_activos()
        elif opcion == "5":
            listar_libros()
        elif opcion == "6":
            listar_alumnos_sancionados()
        elif opcion == "7":
            renovar_prestamo()
        elif opcion == "8":
            registrar_devolucion()
        elif opcion == "9":
            listar_alumnos()
        elif opcion == "0":
            print("\n¡Gracias por usar el sistema!")
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
            input("Presione Enter para continuar...")

# Ejecutar programa
if __name__ == "__main__":
    menu_principal()