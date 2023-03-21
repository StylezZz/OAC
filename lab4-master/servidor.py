import socket
import time
import statistics

arregloFecha = []
arregloKilometer = []
arregloFuelType = []
arregloBrand = []


#Función A
def mainLineaPorLinea():
    idx = 0
    with open("Lab4_viernes.csv","r") as f:
        while True:
            linea = f.readline()
            if not linea:
                break
            #Splitear la linea por comas
            if idx == 0:
                idx += 1
                continue
            data = linea.split(",")
            fecha = data[0]     #DD/MM/AAAA HH:MM
            fecha =modificarFecha(fecha)
            kilometer = data[11]
            fuelType = data[13]
            brand = data[14]

            #Añadir a los arreglos 
            arregloFecha.append(fecha)
            arregloKilometer.append(kilometer)
            arregloFuelType.append(fuelType)
            arregloBrand.append(brand)

def modificarFecha(fecha)->int:
    # Como el formato es DD/MM/AAAA HH:MM y solo se necesitan los datos de la hora y minutos
    # Se debe modificar el formato para que quede HH:MM
    aux = fecha.split(" ")
    if len(aux) < 2:
        # Si no se encontró un espacio en blanco, devuelve un mensaje de error
        return 0
    # Aqui queda HH:MM
    fecha = aux[1]
    # Se debe separar la hora de los minutos
    aux = fecha.split(":")
    # Aqui queda HH
    hora = aux[0]
    # Aqui queda MM
    minutos = aux[1]
    # Se debe multiplicar por 100 la hora y sumarle los minutos
    hora = int(hora) * 100
    minutos = int(minutos)
    hora = hora + minutos
    return hora


#Función B
def devolverHoraMasDatos(arregloFecha)->str:
    maximo = max(arregloFecha)
    hora = maximo // 100
    minutos = maximo % 100
    return str(hora) + ":" + str(minutos)

#Función E
def devolverDatosEstadisticos(arregloKilometer)->list[float,float,float]:
    #Filter para eliminar los datos que no son números
    arregloKilometer = list(filter(lambda x: x.isnumeric(), arregloKilometer))
    #Convertir a float
    arregloKilometer = list(map(lambda x: float(x), arregloKilometer))
    
    #Devolver la media, la mediana y la desviación estandard
    return [statistics.mean(arregloKilometer),statistics.median(arregloKilometer),statistics.stdev(arregloKilometer)]

#Funcion D
def devolverNumeroMarcasyNumeroAutosXMarca(arregloBrand):
    arregloUnicoMarcas = []
    #Para filtrar los repetidos
    arregloUnicoMarcas = list(set(arregloBrand))
    #Para contar cuantos hay de cada marca se debe usar un diccionario
    diccionario = {}
    for marca in arregloUnicoMarcas:
        if marca == "":
            continue
        diccionario[marca] = arregloBrand.count(marca)
    return [len(arregloUnicoMarcas),diccionario]

#Funcion C
def devolverDatosCombustibles(arregloCombustibles):
    arregloContadorCombustible = []
    #Asi se filtran los repetidos
    arregloContadorCombustible = set(arregloCombustibles)
    diccionario = {}
    for combustible in arregloContadorCombustible:
        if combustible == "":
            continue
        diccionario[combustible] = arregloCombustibles.count(combustible)
    #Indicar el combustible más popular 
    maximo = max(diccionario.values())
    for key in diccionario:
        if diccionario[key] == maximo:
            keyFinal = key

    
    return [len(arregloContadorCombustible),diccionario,keyFinal]

SOCK_BUFFER = 1024
if __name__ == "__main__":
    #Con esto se lee el archivo linea por linea y se guardan los valores en los arreglos
    mainLineaPorLinea()

    #Hacer el servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serverAddress = ("0.0.0.0", 5000)
    print(f"Iniciando Servidor en {serverAddress[0]}:{serverAddress[1]}")
    sock.bind(serverAddress)

    sock.listen(6)

    while True:
        print("Esperando conexión")
        conex, clientAddress = sock.accept()

        try:
            print(f"Conexión desde {clientAddress}")
            while True:
                data = conex.recv(SOCK_BUFFER)
                if data:
                    print(f"Recibido: {data.decode()}")
                    if data.decode() == "Hora":
                        hora = devolverHoraMasDatos(arregloFecha)
                        conex.sendall(hora.encode())
                    elif data.decode() == "Combustible":
                        datos = devolverDatosCombustibles(arregloFuelType)
                        conex.sendall(str(datos).encode())
                    elif data.decode() == "Marcas":
                        datos = devolverNumeroMarcasyNumeroAutosXMarca(arregloBrand)
                        conex.sendall(str(datos).encode())
                    elif data.decode() == "Kilometros":
                        datos = devolverDatosEstadisticos(arregloKilometer)
                        conex.sendall(str(datos).encode())
                    elif data.decode()=="Cerrar Sesion":
                        conex.sendall("Sesion Cerrada".encode())
                        #Crear un archivo txt que presentará un resumen de los datos que se han consultado
                        with open("lab04_reporte.txt","w") as f:
                            f.write("Hora: " + devolverHoraMasDatos(arregloFecha) + "\n")
                            f.write("Combustible: " + str(devolverDatosCombustibles(arregloFuelType)) + "\n")
                            f.write("Marcas: " + str(devolverNumeroMarcasyNumeroAutosXMarca(arregloBrand)) + "\n")
                            f.write("Kilometros: " + str(devolverDatosEstadisticos(arregloKilometer)) + "\n")
                        break
                    else:
                        conex.sendall("Comando no reconocido".encode())

        except Exception as e:
            print(f"Exception {e}")
        finally:
            print("Cerrando conexión con el cliente")
            conex.close()









    
    
    

