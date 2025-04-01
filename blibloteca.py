import os
from datetime import datetime, timedelta

# Archivos donde guardamos la información
ARCHIVO_ALUMNOS = "alumnos.txt"       # Datos de los estudiantes
ARCHIVO_LIBROS = "libros.txt"         # Información de los libros
ARCHIVO_PRESTAMOS = "prestamos.txt"   # Registro de préstamos
ARCHIVO_SANCIONES = "sanciones.txt"   # Alumnos sancionados

# Preparar los archivos si no existen
def preparar_archivos():
    for archivo in [ARCHIVO_ALUMNOS, ARCHIVO_LIBROS, ARCHIVO_PRESTAMOS, ARCHIVO_SANCIONES]:
        if not os.path.exists(archivo):
            open(archivo, 'w').close()  # Creamos archivos vacíos

# Herramientas útiles
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')  # Funciona en Windows y Linux/Mac

def pedir_numero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("¡Ups! Debes ingresar un número entero. Intenta de nuevo.")

def pedir_fecha(mensaje):
    while True:
        fecha_str = input(mensaje + " (formato día/mes/año, ej. 15/06/2023): ")
        try:
            return datetime.strptime(fecha_str, "%d/%m/%Y").date()
        except ValueError:
            print("Formato incorrecto. Por favor usa DD/MM/AAAA.")

# Gestión de estudiantes
def agregar_estudiante():
    limpiar_pantalla()
    print("\n✨ REGISTRAR NUEVO ESTUDIANTE ✨")
    print("Por favor ingresa los datos del estudiante:\n")
    
    cedula = input("Número de cédula: ")
    
    # Verificar si el estudiante ya está registrado
    with open(ARCHIVO_ALUMNOS, 'r') as archivo:
        for linea in archivo:
            if linea.startswith(cedula + "|"):
                print("\n¡Atención! Ya existe un estudiante con esta cédula.")
                input("\nPresiona Enter para volver al menú...")
                return
    
    nombre = input("Nombre completo: ")
    carrera = input("Carrera que estudia: ")
    
    # Guardamos la información
    with open(ARCHIVO_ALUMNOS, 'a') as archivo:
        archivo.write(f"{cedula}|{nombre}|{carrera}\n")
    
    print("\n¡Estudiante registrado con éxito! ✅")
    input("\nPresiona Enter para continuar...")

def mostrar_estudiantes():
    limpiar_pantalla()
    print("\n📚 LISTA DE ESTUDIANTES REGISTRADOS 📚\n")
    
    try:
        with open(ARCHIVO_ALUMNOS, 'r') as archivo:
            estudiantes = archivo.readlines()
            
            if not estudiantes:
                print("Aún no hay estudiantes registrados.")
            else:
                for i, linea in enumerate(estudiantes, 1):
                    cedula, nombre, carrera = linea.strip().split('|')
                    print(f"{i}. {nombre} (Cédula: {cedula})")
                    print(f"   Carrera: {carrera}\n")
    except FileNotFoundError:
        print("No se encontró el archivo de estudiantes.")
    
    input("\nPresiona Enter para volver al menú...")

# Gestión de libros
def agregar_libro():
    limpiar_pantalla()
    print("\n📖 AÑADIR NUEVO LIBRO A LA BIBLIOTECA 📖\n")
    
    codigo = input("Código único del libro: ")
    
    # Verificar si el libro ya existe
    with open(ARCHIVO_LIBROS, 'r') as archivo:
        for linea in archivo:
            if linea.startswith(codigo + "|"):
                print("\n¡Este código de libro ya está registrado!")
                input("\nPresiona Enter para volver...")
                return
    
    titulo = input("Título del libro: ")
    autor = input("Autor(es): ")
    categoria = input("Categoría (ej. Novela, Ciencia, Historia): ")
    cantidad = pedir_numero("Cantidad de ejemplares disponibles: ")
    
    # Guardar el nuevo libro
    with open(ARCHIVO_LIBROS, 'a') as archivo:
        archivo.write(f"{codigo}|{titulo}|{autor}|{categoria}|{cantidad}\n")
    
    print("\n¡Libro agregado exitosamente! 📚✅")
    input("\nPresiona Enter para continuar...")

def mostrar_libros():
    limpiar_pantalla()
    print("\n📚 CATÁLOGO DE LIBROS DISPONIBLES 📚\n")
    
    try:
        with open(ARCHIVO_LIBROS, 'r') as archivo:
            libros = archivo.readlines()
            
            if not libros:
                print("El catálogo de libros está vacío.")
            else:
                for i, linea in enumerate(libros, 1):
                    codigo, titulo, autor, categoria, cantidad = linea.strip().split('|')
                    print(f"{i}. {titulo}")
                    print(f"   Autor: {autor}")
                    print(f"   Categoría: {categoria}")
                    print(f"   Ejemplares disponibles: {cantidad}\n")
    except FileNotFoundError:
        print("No se encontró el archivo de libros.")
    
    input("\nPresiona Enter para volver al menú...")

# Gestión de préstamos
def prestar_libro():
    limpiar_pantalla()
    print("\n🔄 REGISTRAR PRÉSTAMO DE LIBRO 🔄\n")
    
    # Verificar estudiante
    cedula = input("Cédula del estudiante: ")
    estudiante_valido = False
    
    with open(ARCHIVO_ALUMNOS, 'r') as archivo:
        for linea in archivo:
            if linea.startswith(cedula + "|"):
                estudiante_valido = True
                break
    
    if not estudiante_valido:
        print("\n❌ No encontramos un estudiante con esta cédula.")
        input("\nPresiona Enter para volver...")
        return
    
    # Verificar sanciones
    hoy = datetime.now().date()
    sancionado = False
    
    with open(ARCHIVO_SANCIONES, 'r') as archivo:
        for linea in archivo:
            datos = linea.strip().split('|')
            if datos[0] == cedula and datetime.strptime(datos[2], "%d/%m/%Y").date() >= hoy:
                sancionado = True
                print(f"\n⚠️ Este estudiante está sancionado hasta el {datos[2]}")
                print(f"Motivo: {datos[1]}")
                input("\nPresiona Enter para volver...")
                return
    
    # Verificar libro
    codigo = input("Código del libro a prestar: ")
    libro_valido = False
    
    with open(ARCHIVO_LIBROS, 'r') as archivo:
        lineas = archivo.readlines()
    
    for i, linea in enumerate(lineas):
        datos = linea.strip().split('|')
        if datos[0] == codigo:
            libro_valido = True
            if int(datos[4]) <= 0:
                print("\n❌ Lo sentimos, no hay ejemplares disponibles de este libro.")
                input("\nPresiona Enter para volver...")
                return
            
            # Actualizar cantidad disponible
            datos[4] = str(int(datos[4]) - 1)
            lineas[i] = '|'.join(datos) + '\n'
            break
    
    if not libro_valido:
        print("\n❌ No encontramos un libro con este código.")
        input("\nPresiona Enter para volver...")
        return
    
    # Registrar préstamo
    fecha_prestamo = datetime.now().date()
    fecha_devolucion = fecha_prestamo + timedelta(days=3)  # Plazo de 3 días
    
    with open(ARCHIVO_PRESTAMOS, 'a') as archivo:
        archivo.write(f"{cedula}|{codigo}|{fecha_prestamo.strftime('%d/%m/%Y')}|{fecha_devolucion.strftime('%d/%m/%Y')}\n")
    
    # Actualizar archivo de libros
    with open(ARCHIVO_LIBROS, 'w') as archivo:
        archivo.writelines(lineas)
    
    print("\n¡Préstamo registrado con éxito! ✅")
    print(f"📅 Fecha de devolución: {fecha_devolucion.strftime('%d/%m/%Y')}")
    input("\nPresiona Enter para continuar...")

def mostrar_prestamos_activos():
    limpiar_pantalla()
    print("\n📝 PRÉSTAMOS EN CURSO 📝\n")
    
    hoy = datetime.now().date()
    
    try:
        with open(ARCHIVO_PRESTAMOS, 'r') as prestamos_archivo, \
             open(ARCHIVO_ALUMNOS, 'r') as alumnos_archivo:
            
            prestamos = [linea.strip().split('|') for linea in prestamos_archivo]
            alumnos = {linea.split('|')[0]: linea.split('|')[1] for linea in alumnos_archivo}
            
            if not prestamos:
                print("No hay préstamos activos en este momento.")
            else:
                for prestamo in prestamos:
                    cedula, codigo_libro, fecha_p, fecha_dev = prestamo
                    fecha_devolucion = datetime.strptime(fecha_dev, "%d/%m/%Y").date()
                    
                    estado = "✅ En plazo" if hoy <= fecha_devolucion else "⚠️ Atrasado"
                    nombre = alumnos.get(cedula, "Nombre no disponible")
                    
                    print(f"👤 Estudiante: {nombre} (Cédula: {cedula})")
                    print(f"📖 Libro prestado: {codigo_libro}")
                    print(f"📅 Fecha préstamo: {fecha_p}")
                    print(f"📅 Fecha devolución: {fecha_dev}")
                    print(f"🔄 Estado: {estado}\n")
    except FileNotFoundError:
        print("No se encontraron archivos de préstamos o estudiantes.")
    
    input("\nPresiona Enter para volver al menú...")

# Gestión de sanciones
def mostrar_sancionados():
    limpiar_pantalla()
    print("\n🚫 ESTUDIANTES SANCIONADOS ACTUALMENTE 🚫\n")
    
    hoy = datetime.now().date()
    
    try:
        with open(ARCHIVO_SANCIONES, 'r') as sanciones_archivo, \
             open(ARCHIVO_ALUMNOS, 'r') as alumnos_archivo:
            
            sanciones = [linea.strip().split('|') for linea in sanciones_archivo]
            alumnos = {linea.split('|')[0]: linea.split('|')[1] for linea in alumnos_archivo}
            
            if not sanciones:
                print("No hay estudiantes sancionados en este momento.")
            else:
                for sancion in sanciones:
                    cedula, motivo, fecha_fin = sancion
                    fecha_fin_sancion = datetime.strptime(fecha_fin, "%d/%m/%Y").date()
                    
                    if fecha_fin_sancion >= hoy:
                        nombre = alumnos.get(cedula, "Nombre no disponible")
                        print(f"👤 Estudiante: {nombre} (Cédula: {cedula})")
                        print(f"📌 Motivo: {motivo}")
                        print(f"📅 Sancionado hasta: {fecha_fin}\n")
    except FileNotFoundError:
        print("No se encontraron archivos de sanciones o estudiantes.")
    
    input("\nPresiona Enter para volver al menú...")

# Renovación de préstamos
def renovar_prestamo():
    limpiar_pantalla()
    print("\n🔄 RENOVAR PRÉSTAMO DE LIBRO 🔄\n")
    
    cedula = input("Cédula del estudiante: ")
    codigo = input("Código del libro a renovar: ")
    
    # Buscar préstamo
    with open(ARCHIVO_PRESTAMOS, 'r') as archivo:
        lineas = archivo.readlines()
    
    encontrado = False
    for i, linea in enumerate(lineas):
        datos = linea.strip().split('|')
        if datos[0] == cedula and datos[1] == codigo:
            encontrado = True
            hoy = datetime.now().date()
            fecha_dev = datetime.strptime(datos[3], "%d/%m/%Y").date()
            
            if hoy > fecha_dev:
                print("\n❌ No se puede renovar un préstamo atrasado.")
                print("Por favor devuelve el libro y regulariza tu situación.")
                input("\nPresiona Enter para volver...")
                return
            
            # Actualizar fecha de devolución
            nueva_fecha = hoy + timedelta(days=3)
            datos[3] = nueva_fecha.strftime("%d/%m/%Y")
            lineas[i] = '|'.join(datos) + '\n'
            break
    
    if not encontrado:
        print("\n❌ No encontramos el préstamo especificado.")
        input("\nPresiona Enter para volver...")
        return
    
    # Actualizar archivo
    with open(ARCHIVO_PRESTAMOS, 'w') as archivo:
        archivo.writelines(lineas)
    
    print("\n¡Préstamo renovado con éxito! ✅")
    print(f"📅 Nueva fecha de devolución: {nueva_fecha.strftime('%d/%m/%Y')}")
    input("\nPresiona Enter para continuar...")

# Devolución de libros
def devolver_libro():
    limpiar_pantalla()
    print("\n↩️ REGISTRAR DEVOLUCIÓN DE LIBRO ↩️\n")
    
    cedula = input("Cédula del estudiante: ")
    codigo = input("Código del libro a devolver: ")
    
    # Buscar y eliminar préstamo
    with open(ARCHIVO_PRESTAMOS, 'r') as archivo:
        lineas = archivo.readlines()
    
    prestamo_encontrado = False
    nuevas_lineas = []
    datos_prestamo = None
    
    for linea in lineas:
        datos = linea.strip().split('|')
        if datos[0] == cedula and datos[1] == codigo:
            prestamo_encontrado = True
            datos_prestamo = datos
        else:
            nuevas_lineas.append(linea)
    
    if not prestamo_encontrado:
        print("\n❌ No encontramos el préstamo especificado.")
        input("\nPresiona Enter para volver...")
        return
    
    # Verificar retraso
    hoy = datetime.now().date()
    fecha_dev = datetime.strptime(datos_prestamo[3], "%d/%m/%Y").date()
    
    if hoy > fecha_dev:
        fin_sancion = hoy + timedelta(days=7)
        with open(ARCHIVO_SANCIONES, 'a') as archivo:
            archivo.write(f"{cedula}|Retraso en devolución|{fin_sancion.strftime('%d/%m/%Y')}\n")
        print("\n⚠️ El estudiante ha sido sancionado por 7 días por devolución tardía.")
    
    # Actualizar préstamos
    with open(ARCHIVO_PRESTAMOS, 'w') as archivo:
        archivo.writelines(nuevas_lineas)
    
    # Actualizar disponibilidad del libro
    with open(ARCHIVO_LIBROS, 'r') as archivo:
        lineas_libros = archivo.readlines()
    
    for i, linea in enumerate(lineas_libros):
        datos = linea.strip().split('|')
        if datos[0] == codigo:
            datos[4] = str(int(datos[4]) + 1)
            lineas_libros[i] = '|'.join(datos) + '\n'
            break
    
    with open(ARCHIVO_LIBROS, 'w') as archivo:
        archivo.writelines(lineas_libros)
    
    print("\n¡Devolución registrada con éxito! ✅")
    input("\nPresiona Enter para continuar...")

# Menú interactivo
def mostrar_menu():
    preparar_archivos()
    while True:
        limpiar_pantalla()
        print("\n🏛️ SISTEMA DE BIBLIOTECA AMIGABLE 🏛️")
        print("\n¿Qué deseas hacer hoy?")
        print("1. Registrar nuevo estudiante")
        print("2. Agregar nuevo libro al catálogo")
        print("3. Registrar préstamo de libro")
        print("4. Ver préstamos activos")
        print("5. Ver catálogo de libros")
        print("6. Ver estudiantes sancionados")
        print("7. Renovar préstamo de libro")
        print("8. Registrar devolución de libro")
        print("9. Ver todos los estudiantes")
        print("0. Salir del sistema")
        
        opcion = input("\nElige una opción (0-9): ")
        
        if opcion == "1":
            agregar_estudiante()
        elif opcion == "2":
            agregar_libro()
        elif opcion == "3":
            prestar_libro()
        elif opcion == "4":
            mostrar_prestamos_activos()
        elif opcion == "5":
            mostrar_libros()
        elif opcion == "6":
            mostrar_sancionados()
        elif opcion == "7":
            renovar_prestamo()
        elif opcion == "8":
            devolver_libro()
        elif opcion == "9":
            mostrar_estudiantes()
        elif opcion == "0":
            print("\n¡Gracias por usar nuestro sistema de biblioteca! 📚❤️")
            print("Hasta pronto...\n")
            break
        else:
            print("\n❌ Opción no válida. Por favor elige un número del 0 al 9.")
            input("\nPresiona Enter para intentar de nuevo...")

# Iniciar el programa
if __name__ == "__main__":
    mostrar_menu()
