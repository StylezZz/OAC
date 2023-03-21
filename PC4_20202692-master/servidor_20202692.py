import random
import socket
import time
import asyncio

"""
Consideraciones a tomar en cuenta:

    La posición 3 es el player
    La posición 4 es el equipo
    La posición 6 es el MIN
    La posción 21 es el PTS (Se debe sumar los PTS de cada jugador y retornar el promedio de los puntos)
    No estoy tomando en cuenta empates en ninguno de los partidos
    No se toma en cuenta si los jugadores han jugado por diferentes equipos o no
    No se toma en cuenta si los jugadores han jugado en diferentes temporadas
"""

EQUIPOS_PARTICIPANTES = ["ATL","BOS","BRK","CHA","DAL","DEN","DET","GSW","LAC","LAL","MEM","MIA",
                        "NOP","NYK","OKC","ORL","POR","SAC","SAS","SEA","WAS","CHI","CLE","UTA",
                        "HOU","IND","MIL","MIN","PHI","PHX","TOR","BOL"]

#Estos son los grupos que se van a enfrentar
GRUPO_A= ["ATL","BOS","BRK","CHA"]
GRUPO_B= ["DAL","DEN","DET","GSW"]
GRUPO_C= ["LAC","LAL","MEM","MIA"]
GRUPO_D= ["NOP","NYK","OKC","ORL"]
GRUPO_E= ["POR","SAC","SAS","SEA"]
GRUPO_F= ["WAS","CHI","CLE","UTA"]
GRUPO_G= ["HOU","IND","MIL","MIN"]
GRUPO_H= ["PHI","PHX","TOR","BOL"]


#Funcion A
def leerArchivo()->dict:
    with open('datos.csv') as f:
        f.readline()
        equipos = {}
        for linea in f:
            datos = linea.split(',')
            equipo = datos[4]
            jugador = datos[3]
            minutos = float(datos[6])
            puntos = int(datos[21])
            
            if equipo not in EQUIPOS_PARTICIPANTES:
                continue
            
            if equipo not in equipos:
                equipos[equipo] = {'Jugadores': {}, 'Promedio Puntos':0}
            
            equipos[equipo]['Jugadores'][jugador] = {'Minutos':minutos, 'Puntos':puntos}
            equipos[equipo]['Promedio Puntos'] += puntos
    return equipos

#Funcion B
listaTop5 = []
def generarListaTop5JuagdoresXEquipo(equipos:dict)->list:
    for equipo in equipos:
        #Lo que hace esto es que va a ir agregando tuplas a la listaTop5
        #La tupla va a tener el nombre del equipo y una lista con los 5 mejores jugadores
        listaTop5.append((equipo, obtenerTop5Jugadores(equipos[equipo]['Jugadores'])))
    #Luego me retornará la listaTop5 pedida
    return listaTop5

#Lo que hace esto es tener una lista de jugadores 
def obtenerTop5Jugadores(jugadores:dict)->list:
    listaJugadores = []
    for jugador in jugadores:
        #Se iterará por jugador y se agregará una tupla con el nombre del jugador y sus puntos
        listaJugadores.append((jugador, jugadores[jugador]['Puntos']))
    #Se ordena la lista de mayor a menor con la función sort
    listaJugadores.sort(key=lambda x: x[1], reverse=True)
    #Se retorna los primeros 5 jugadores por eso el [0:5]
    return listaJugadores[:5]
        
#Funcion C
def partido(equipo1:str,equipo2:str)->str:
    #Elegir al ganador de manera aleatoria
    probabilidadEquipo1 = random.randint(0,10)
    probabilidadEquipo2 = random.randint(0,10)
    if probabilidadEquipo1 > probabilidadEquipo2:
        return equipo1
    else:
        return equipo2

#Funcion F
async def eliminatorias_async(clasificados_async):
    podio = []
    GRUPO_I = clasificados_async[0:4]
    GRUPO_J = clasificados_async[4:8]
    GRUPO_K = clasificados_async[8:12]
    GRUPO_L = clasificados_async[12:16]

    #Asumiré que la segunda fase tambien se juega en grupos de 4 y tambien se usará los puntajes promedio de los equipos para determinar 
    #el ganador de cada partido
    imprimirLineas("=", 50)
    print(f"Se iniciara con la segunda fase de eliminatorias")
    clasificadosFaseFinal = await realizarSegundaFase(GRUPO_I, GRUPO_J, GRUPO_K, GRUPO_L)
    #Luego de cada etapa se deberá hacer una espera de 0.15 segundos
    await asyncio.sleep(0.15)

    crucesCuartos = [(clasificadosFaseFinal[0],clasificadosFaseFinal[3]),(clasificadosFaseFinal[1],clasificadosFaseFinal[2]),
                    (clasificadosFaseFinal[4],clasificadosFaseFinal[7]),(clasificadosFaseFinal[5],clasificadosFaseFinal[6])]
    imprimirLineas("=", 50)
    print(f"Se iniciara con los cuartos de final")
    ganadoresCuartos = await realizarCuartosDeFinal(crucesCuartos)
    #Luego de cada etapa se deberá hacer una espera de 0.15 segundos
    await asyncio.sleep(0.15)

    crucesSemis = [(ganadoresCuartos[0],ganadoresCuartos[1]),(ganadoresCuartos[2],ganadoresCuartos[3])]
    imprimirLineas("=", 50)
    print(f"Se iniciara con las semifinales")
    ganadoresSemis = await realizarSemis(crucesSemis)
    #Se retorna un diccionario en la función anterior
    #Aqui en ganadoresSemis se almacenara todos los equipos que pasaron a la final y los que pasaran para el tercer puesto
    #Luego de cada etapa se deberá hacer una espera de 0.15 segundos
    await asyncio.sleep(0.15)

    imprimirLineas("=", 50)
    print(f"Se iniciara con el tercer puesto")
    equipoA_TercerPuesto = ganadoresSemis[2][0]
    equipoB_TercerPuesto = ganadoresSemis[3][0]

    equipoA_Final = ganadoresSemis[0][0]
    equipoB_Final = ganadoresSemis[1][0]
    
    tercerPuesto = await realizarTercerPuesto(equipoA_TercerPuesto,equipoB_TercerPuesto)
    #Luego de cada etapa se deberá hacer una espera de 0.15 segundos
    await asyncio.sleep(0.15)

    imprimirLineas("=", 50)
    print(f"Se iniciara con la final")
    listaGanadores = await realizarFinal(equipoA_Final,equipoB_Final)

    primerPuesto = listaGanadores[0]
    segundoPuesto = listaGanadores[1]
    podio.append(primerPuesto)
    podio.append(segundoPuesto)
    podio.append(tercerPuesto)
    return podio

#Funcion G
def eliminatorias_sync(clasificados_async):
    podio = []
    GRUPO_I = clasificados_async[0:4]
    GRUPO_J = clasificados_async[4:8]
    GRUPO_K = clasificados_async[8:12]
    GRUPO_L = clasificados_async[12:16]

    #Asumiré que la segunda fase tambien se juega en grupos de 4 y tambien se usará los puntajes promedio de los equipos para determinar 
    #el ganador de cada partido
    imprimirLineas("=", 50)
    print(f"Se iniciara con la segunda fase de eliminatorias")
    clasificadosFaseFinal = realizarSegundaFaseSync(GRUPO_I, GRUPO_J, GRUPO_K, GRUPO_L)
    #Luego de cada etapa se deberá hacer una espera de 0.15 segundos
    time.sleep(0.15)

    crucesCuartos = [(clasificadosFaseFinal[0],clasificadosFaseFinal[3]),(clasificadosFaseFinal[1],clasificadosFaseFinal[2]),
                    (clasificadosFaseFinal[4],clasificadosFaseFinal[7]),(clasificadosFaseFinal[5],clasificadosFaseFinal[6])]
    imprimirLineas("=", 50)
    print(f"Se iniciara con los cuartos de final")
    ganadoresCuartos = realizarCuartosDeFinalSync(crucesCuartos)
    #Luego de cada etapa se deberá hacer una espera de 0.15 segundos
    time.sleep(0.15)

    crucesSemis = [(ganadoresCuartos[0],ganadoresCuartos[1]),(ganadoresCuartos[2],ganadoresCuartos[3])]
    imprimirLineas("=", 50)
    print(f"Se iniciara con las semifinales")
    ganadoresSemis = realizarSemisSync(crucesSemis)
    #Se retorna un diccionario en la función anterior
    #Aqui en ganadoresSemis se almacenara todos los equipos que pasaron a la final y los que pasaran para el tercer puesto
    #Luego de cada etapa se deberá hacer una espera de 0.15 segundos
    time.sleep(0.15)

    imprimirLineas("=", 50)
    print(f"Se iniciara con el tercer puesto")
    equipoA_TercerPuesto = ganadoresSemis[2][0]
    equipoB_TercerPuesto = ganadoresSemis[3][0]
    
    equipoA_Final = ganadoresSemis[0][0]
    equipoB_Final = ganadoresSemis[1][0]

    tercerPuesto = realizarTercerPuestoSync(equipoA_TercerPuesto,equipoB_TercerPuesto)
    #Luego de cada etapa se deberá hacer una espera de 0.15 segundos
    time.sleep(0.15)

    imprimirLineas("=", 50)
    print(f"Se iniciara con la final")
    listaGanadores = realizarFinalSync(equipoA_Final,equipoB_Final)
    
    primerPuesto = listaGanadores[0][0]
    segundoPuesto = listaGanadores[1][0]
    podio.append(primerPuesto)
    podio.append(segundoPuesto)
    podio.append(tercerPuesto)
    return podio

def realizarSegundaFaseSync(grupoI,grupoJ,grupoK,grupoL)->list:
    #Se debe usar la funcion partido(equipo1,equipo2) para determinar el ganador de cada partido
    grupos = [grupoI,grupoJ,grupoK,grupoL]
    clasificados = []
    aux = 0
    for grupo in grupos:
        partidos = []
        for j in range(len(grupo)):
            for i in range(j+1,len(grupo)):
                partidos.append(partido(grupo[j],grupo[i]))
                time.sleep(0.15)
        resultados = partidos
        puntos = {equipo:0 for equipo in grupo}
        for resultado in resultados:
            puntos[resultado] += 3
        classified = sorted(puntos.items(), key=lambda x: x[1], reverse=True)
        clasificados.append(classified[0][0])
        clasificados.append(classified[1][0])
        imprimirTablaPosicionesPrimeraFase(classified,aux+8)
        aux = aux + 1
    return clasificados

def realizarCuartosDeFinalSync(crucesCuartos:list)->list:
    #Se debe usar la funcion partido(equipo1,equipo2) para determinar el ganador de cada partido
    ganadoresCuartos = []
    for cruce in crucesCuartos:
        print(f"Jugando partido entre {cruce[0]} y {cruce[1]}")
        ganadoresCuartos.append(partido(cruce[0],cruce[1]))
        print("Ganador: ",ganadoresCuartos[-1])
        time.sleep(0.15)
    return ganadoresCuartos

def realizarSemisSync(crucesSemis:list):
    tablasPosiciones = {crucesSemis[0][0]:0,crucesSemis[0][1]:0,crucesSemis[1][0]:0,crucesSemis[1][1]:0}
    for cruce in crucesSemis:
        print(f"Jugando partido entre {cruce[0]} y {cruce[1]}")
        ganador = partido(cruce[0],cruce[1])
        print("Ganador: ",ganador)
        tablasPosiciones[ganador] += 3
        time.sleep(0.15)
    return sorted(tablasPosiciones.items(), key=lambda x: x[1], reverse=True)

def realizarTercerPuestoSync(equipoA:str,equipoB:str)->str:
    #Se debe usar la funcion partido(equipo1,equipo2) para determinar el ganador de cada partido
    print(f"Jugando partido entre {equipoA} y {equipoB}")
    ganador = partido(equipoA,equipoB)
    print("Ganador: ",ganador)
    return ganador

def realizarFinalSync(equipoA:str,equipoB:str)->list:
    #Se debe usar la funcion partido(equipo1,equipo2) para determinar el ganador de cada partido
    diccionarioFinal = {equipoA:0,equipoB:0}
    print(f"Jugando partido entre {equipoA} y {equipoB}")
    ganador = partido(equipoA,equipoB)
    print("Ganador: ",ganador)
    diccionarioFinal[ganador] += 1
    #Ordenar el diccionario para obtener el ganador
    return sorted(diccionarioFinal.items(), key=lambda x: x[1], reverse=True)

async def realizarTercerPuesto(equipoA:str,equipoB:str)->str:
    #Se debe usar la funcion partido(equipo1,equipo2) para determinar el ganador de cada partido
    print(f"Jugando partido entre {equipoA} y {equipoB}")
    ganador = partido(equipoA,equipoB)
    print("Ganador: ",ganador)
    return ganador

async def realizarFinal(equipoA:str,equipoB:str)->list:
    #Se debe usar la funcion partido(equipo1,equipo2) para determinar el ganador de cada partido
    diccionarioFinal = {equipoA:0,equipoB:0}
    print(f"Jugando partido entre {equipoA} y {equipoB}")
    ganador = partido(equipoA,equipoB)
    print("Ganador: ",ganador)
    diccionarioFinal[ganador] += 1
    #Ordenar el diccionario de mayor a menor
    diccionarioFinal = dict(sorted(diccionarioFinal.items(), key=lambda item: item[1], reverse=True))
    #Se retorna una lista con el ganador y el perdedor
    return list(diccionarioFinal.keys())

async def realizarCuartosDeFinal(crucesCuartos)->list:
    #Se debe usar la funcion partido(equipo1,equipo2) para determinar el ganador de cada partido
    ganadoresCuartos = []
    for cruce in crucesCuartos:
        print(f"Jugando partido entre {cruce[0]} y {cruce[1]}")
        ganadoresCuartos.append(partido(cruce[0],cruce[1]))
        print("Ganador: ",ganadoresCuartos[-1])
    return ganadoresCuartos

async def realizarSemis(crucesSemis):
    #Se debe usar la funcion partido(equipo1,equipo2) para determinar el ganador de cada partido
    tablaPosiciones = {crucesSemis[0][0]:0,crucesSemis[0][1]:0,crucesSemis[1][0]:0,crucesSemis[1][1]:0}
    for cruce in crucesSemis:
        print(f"Jugando partido entre {cruce[0]} y {cruce[1]}")
        ganador = partido(cruce[0],cruce[1])
        print("Ganador: ",ganador)
        tablaPosiciones[ganador] += 3
        await asyncio.sleep(0.15)
    tablaPosiciones = sorted(tablaPosiciones.items(), key=lambda x: x[1], reverse=True)
    return tablaPosiciones
    
async def realizarSegundaFase(grupoI,grupoJ,grupoK,grupoL)->list:
    grupos = [grupoI,grupoJ,grupoK,grupoL]
    clasificados = []
    aux =0
    for grupo in grupos:
        partidos = []
        for i in range(len(grupo)):
            for j in range(i+1,len(grupo)):
                partidos.append(partido_async(grupo[i],grupo[j]))
        resultados = await asyncio.gather(*partidos)
        puntos = {equipo : 0 for equipo in grupo}
        for resultado in resultados:
            puntos[resultado] += 3
        classified = sorted(puntos.items(), key=lambda x: x[1], reverse=True)
        imprimirTablaPosicionesPrimeraFase(classified,aux+8)
        clasificados.append(classified[0][0])
        clasificados.append(classified[1][0])
        aux = aux + 1
    return clasificados

def modificarPuntosTotales(equipos:dict)->dict:
    #Los puntos totales se modificaran para que en ese valor se encuentre el puntaje promedio de cada equipo
    for equipo in equipos:
        #Se divide el puntaje total entre la cantidad de equipos participantes
        equipos[equipo]['Promedio Puntos'] = equipos[equipo]['Promedio Puntos'] / len(EQUIPOS_PARTICIPANTES)
    return equipos

async def partido_async(equipo1,equipo2):
    puntajePromedioEquipo1 = equipos[equipo1]['Promedio Puntos']
    puntajePromedioEquipo2 = equipos[equipo2]['Promedio Puntos']
    if puntajePromedioEquipo1 > puntajePromedioEquipo2:
        await asyncio.sleep(0.15)
        return equipo1
    else:
        await asyncio.sleep(0.15)
        return equipo2
    
#Funcion D
async def grupos_async() -> list:
    aux = 0
    clasificados_async = []
    #Se crea una lista con los grupos
    grupos = [GRUPO_A, GRUPO_B, GRUPO_C, GRUPO_D, GRUPO_E, GRUPO_F, GRUPO_G, GRUPO_H]
    #Se itera por cada grupo
    for grupo in grupos:
        #Se crea una lista de partidos para cada grupo que almacenara los partidos
        partidos = []
        #Se itera por cada equipo del grupo
        for i in range(len(grupo)):
            #Se itera por cada equipo del grupo para crear los partidos
            for j in range(i+1, len(grupo)):
                #Con esto se crea un partido y se agrega a la lista de partidos 
                partidos.append(partido_async(grupo[i], grupo[j]))
        #Se espera a que todos los partidos se resuelvan y se almacenan en la lista de ganadores
        ganadores = await asyncio.gather(*partidos)
        #Se crea un diccionario con los equipos y sus puntos
        puntos = {equipo: 0 for equipo in grupo}
        #Con esto se le asignan los puntos a cada equipo y se verifica quien gano
        #Y se lo busca en el diccionario ganadores y se le suma 3 puntos
        for resultado in ganadores:
            puntos[resultado] += 3
        #Se ordena el diccionario de mayor a menor 
        equiposClasificados = sorted(puntos.items(), key=lambda x: x[1], reverse=True)
        # Mostrar la tabla de posiciones de cada grupo
        #Para ver a los equipos clasificados
        imprimirTablaPosicionesPrimeraFase(equiposClasificados,aux)
        aux = aux + 1
        #Y con esto añadimos a la lista clasificados_async los equipos clasificados que serian los dos primeros
        #Y como se requiere el nombre del equipo se accede a la posición 0 de la tupla
        clasificados_async.append(equiposClasificados[0][0])
        clasificados_async.append(equiposClasificados[1][0])
        
    #Y luego de las iteraciones se retornará la lista de clasificados
    return clasificados_async

def imprimirTablaPosicionesPrimeraFase(equiposClasificados,index):
    print("Tabla del Grupo ",chr(65+index))
    print("------------------------------------------------------------------")
    print(f"Equipo\t\tPuntos")
    for equipo in equiposClasificados:
        print(f"{equipo[0]}\t\t{equipo[1]}")
    print("------------------------------------------------------------------")

#Funcion E
def grupos_sync()->list:
    aux = 0
    clasificados_sync = []
    #Se crea una lista con los grupos
    grupos = [GRUPO_A, GRUPO_B, GRUPO_C, GRUPO_D, GRUPO_E, GRUPO_F, GRUPO_G, GRUPO_H]
    #Se itera por cada grupo
    for grupo in grupos:
        #Se crea una lista de partidos para cada grupo que almacenara los partidos
        partidos = []
        #Se itera por cada equipo del grupo
        for i in range(len(grupo)):
            #Se itera por cada equipo del grupo para crear los partidos
            for j in range(i+1, len(grupo)):
                #Con esto se crea un partido y se agrega a la lista de partidos 
                partidos.append(partido_sync(grupo[i], grupo[j]))
        #Se crea un diccionario con los equipos y sus puntos
        puntos = {equipo: 0 for equipo in grupo}
        #Con esto se le asignan los puntos a cada equipo y se verifica quien gano
        #Y se lo busca en el diccionario ganadores y se le suma 3 puntos
        for resultado in partidos:
            puntos[resultado] += 3
        #Se ordena el diccionario de mayor a menor 
        equiposClasificados = sorted(puntos.items(), key=lambda x: x[1], reverse=True)
        # Mostrar la tabla de posiciones de cada grupo
        imprimirTablaPosicionesPrimeraFase(equiposClasificados,aux)
        aux = aux + 1
        #Y con esto añadimos a la lista clasificados_sync los equipos clasificados que serian los dos primeros
        #Y como se requiere el nombre del equipo se accede a la posición 0 de la tupla
        clasificados_sync.append(equiposClasificados[0][0])
        clasificados_sync.append(equiposClasificados[1][0])

    #Y luego de las iteraciones se retornará la lista de clasificados
    return clasificados_sync

def partido_sync(equipo1,equipo2)->str:
    puntajePromedioEquipo1 = equipos[equipo1]['Promedio Puntos']
    puntajePromedioEquipo2 = equipos[equipo2]['Promedio Puntos']
    if puntajePromedioEquipo1 > puntajePromedioEquipo2:
        time.sleep(0.15)
        return equipo1
    else:
        time.sleep(0.15)
        return equipo2

def imprimirLineas(caracter,cantidad):
    print(caracter*cantidad)



SOCK_BUFFER_SIZE = 10000
if __name__ == "__main__":
    equipos = leerArchivo()
    equipos=modificarPuntosTotales(equipos)
    listaTop5 = generarListaTop5JuagdoresXEquipo(equipos)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddres = ("0.0.0.0", 5000)

    print(f"Iniciando Servidor en {serverAddres[0]}:{serverAddres[1]}")
    sock.bind(serverAddres)

    sock.listen(1)

    while True:
        print(f"Esperando conexión del cliente....")
        connex, clientAddres = sock.accept()
        tiempos = []
        try:
            print(f"Conexión establecida con {clientAddres[0]}:{clientAddres[1]}")
            while True:
                data = connex.recv(SOCK_BUFFER_SIZE)
                if data:
                    print(f"Recibido: {data.decode()}")
                    if data.decode()== "nombre":
                        connex.sendall("Procesando data".encode())
                    elif data.decode()== "equipos":
                        listaTop5 = generarListaTop5JuagdoresXEquipo(equipos)
                        #Se manda lo generado en listaTop5 al servidor
                        connex.sendall(str(listaTop5).encode())
                    elif data.decode()=="fase de grupos asincrono":
                        tiempo1 = time.time()
                        clasificados_async = asyncio.run(grupos_async())
                        tiempo2 = time.time()
                        #Se manda lo generado en clasificados_async al servidor y al cliente
                        tiempos.append(tiempo2-tiempo1)
                        connex.sendall(str(clasificados_async).encode())
                    elif data.decode()=="fase de grupos sincrono":
                        tiempo3 = time.time()
                        clasificados_sync = grupos_sync()
                        tiempo4 = time.time()
                        #Se manda lo generado en clasificados_sync al servidor y al cliente
                        tiempos.append(tiempo4-tiempo3)
                        connex.sendall(str(clasificados_sync).encode())
                    elif data.decode()=="eliminatorias asincrono":
                        tiempo5 = time.time()
                        podio_async = asyncio.run(eliminatorias_async(clasificados_async))
                        tiempo6 = time.time()
                        #Se manda lo generado en podio_async al servidor y al cliente
                        tiempos.append(tiempo6-tiempo5)
                        connex.sendall(str(podio_async).encode())
                    elif data.decode()=="eliminatorias sincrono":
                        tiempo7 = time.time()
                        podio_sync = eliminatorias_sync(clasificados_sync)
                        tiempo8 = time.time()
                        #Se manda lo generado en podio_sync al servidor y al cliente
                        tiempos.append(tiempo8-tiempo7)
                        connex.sendall(str(podio_sync).encode())
                    elif data.decode() == "reporte":
                        #Se crea un archivo de texto con los tiempos de ejecución de cada inciso y con las listas 
                        #Creadas en cada inciso
                        with open("reporte.txt", "w") as file:
                            file.write("Tiempo de ejecucion de la fase de grupos asincrono: " + str(tiempos[0]) + " segundos \n")
                            file.write(str(clasificados_async) + "\n\n")
                            file.write("Tiempo de ejecucion de la fase de grupos sincrono: " + str(tiempos[1]) + " segundos \n")
                            file.write(str(clasificados_sync) + "\n\n")
                            file.write("Tiempo de ejecucion de la fase de eliminatorias asincrono: " + str(tiempos[2]) + " segundos \n")
                            file.write(str(podio_async) + "\n\n")
                            file.write("Tiempo de ejecucion de la fase de eliminatorias sincrono: " + str(tiempos[3]) + " segundos \n")
                            file.write(str(podio_sync) + "\n\n")
                elif data.decode()== "Cerrar Sesion":
                    print("Cerrando sesión")
                    break
                else:
                    #Mandar un mensaje de mensaje incorrecto
                    connex.sendall("Mensaje incorrecto".encode())
                    
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            print(f"Cerrando conexión con {clientAddres[0]}:{clientAddres[1]}")
            connex.close()









    
    



    
