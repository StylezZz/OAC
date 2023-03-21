import asyncio
import time
import random

#Para fines del problema se pondra un arreglo que guarde los ratings de cada participante
arregloRatings = []
arregloNombres = ["Magnus","Vladimir","Peter","Levon"]


#Con esto tengo los rating de cada jugador
#Para la posicion 0 es el rating de Magnus
#Para la posicion 1 es el rating de Vladimir
#Para la posicion 2 es el rating de Peter
#Para la posicion 3 es el rating de Wesley
def leerArchivo():
    idx = 0
    with open("players.csv", "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            if idx == 0:
                idx += 1
                continue
            data = line.split(";")
            arregloRatings.append(int(data[1]))

#Funcion B
async def fase_rondas_async()->str:
    puntosMagnus,puntosVladimir,puntosPeter,puntosLevon = 0,0,0,0
    idxMagnus,idxVladimir,idxPeter,idxLevon = 0,1,2,3
    for i in range(3):
        if i == 0:
            print(f"Ronda {i+1}-Dia 1")
            print(f"{arregloNombres[idxMagnus]} vs {arregloNombres[idxVladimir]}")
            if(arregloRatings[idxMagnus] > arregloRatings[idxVladimir]):
                puntosMagnus += 1
                print(f"El ganador de la partida {i+1} es Magnus")
            else:
                puntosVladimir += 1
                print(f"El ganador de la partida {i+1} es Vladimir")
            await asyncio.sleep(0.15)
            print(f"{arregloNombres[idxPeter]} vs {arregloNombres[idxLevon]}")
            if(arregloRatings[idxPeter] > arregloRatings[idxLevon]):
                puntosPeter += 1
                print(f"El ganador de la partida {i+1} es Peter")
            else:
                puntosLevon += 1
                print(f"El ganador de la partida {i+1} es Levon")
            
        elif i == 1:
            print(f"Ronda {i+1}-Dia 2")
            print(f"{arregloNombres[idxMagnus]} vs {arregloNombres[idxPeter]}")
            if(arregloRatings[idxMagnus] > arregloRatings[idxPeter]):
                puntosMagnus += 1
                print(f"El ganador de la partida {i+1} es Magnus")
            else:
                puntosPeter += 1
                print(f"El ganador de la partida {i+1} es Peter")
            await asyncio.sleep(0.15)
            print(f"{arregloNombres[idxVladimir]} vs {arregloNombres[idxLevon]}")
            if(arregloRatings[idxVladimir] > arregloRatings[idxLevon]):
                puntosVladimir += 1
                print(f"El ganador de la partida {i+1} es Vladimir")
            else:
                puntosLevon += 1
                print(f"El ganador de la partida {i+1} es Levon")
        
        else:
            print(f"Ronda {i+1}-Dia 3")
            print(f"{arregloNombres[idxMagnus]} vs {arregloNombres[idxLevon]}")
            if(arregloRatings[idxMagnus] > arregloRatings[idxLevon]):
                puntosMagnus += 1
            else:
                puntosLevon += 1
            await asyncio.sleep(0.15)
            print(f"{arregloNombres[idxVladimir]} vs {arregloNombres[idxPeter]}")
            if(arregloRatings[idxVladimir] > arregloRatings[idxPeter]):
                puntosVladimir += 1
            else:
                puntosPeter += 1
        
    diccionario = {"Magnus":puntosMagnus,"Vladimir":puntosVladimir,"Peter":puntosPeter,"Levon":puntosLevon}
    ganador = max(diccionario, key=diccionario.get)
    return ganador

#Funcion C
def fase_rondas_sync()->str:
    #Hace lo mismo pero de manera sincrona
    puntosMagnus,puntosVladimir,puntosPeter,puntosLevon = 0,0,0,0
    idxMagnus,idxVladimir,idxPeter,idxLevon = 0,1,2,3
    for i in range(3):
        if i == 0:
            print(f"Ronda {i+1}-Dia 1")
            print(f"{arregloNombres[idxMagnus]} vs {arregloNombres[idxVladimir]}")
            if(arregloRatings[idxMagnus] > arregloRatings[idxVladimir]):
                puntosMagnus += 1
                print(f"El ganador de la partida {i+1} es Magnus")
            else:
                puntosVladimir += 1
                print(f"El ganador de la partida {i+1} es Vladimir")
            time.sleep(0.15)
            print(f"{arregloNombres[idxPeter]} vs {arregloNombres[idxLevon]}")
            if(arregloRatings[idxPeter] > arregloRatings[idxLevon]):
                puntosPeter += 1
                print(f"El ganador de la partida {i+1} es Peter")
            else:
                puntosLevon += 1
                print(f"El ganador de la partida {i+1} es Levon")
            time.sleep(0.15)
        elif i == 1:
            print(f"Ronda {i+1}-Dia 2")
            print(f"{arregloNombres[idxMagnus]} vs {arregloNombres[idxPeter]}")
            if(arregloRatings[idxMagnus] > arregloRatings[idxPeter]):
                print(f"El ganador de la partida {i+1} es Magnus")
                puntosMagnus += 1
            else:
                puntosPeter += 1
                print(f"El ganador de la partida {i+1} es Peter")
            time.sleep(0.15)
            print(f"{arregloNombres[idxVladimir]} vs {arregloNombres[idxLevon]}")
            if(arregloRatings[idxVladimir] > arregloRatings[idxLevon]):
                puntosVladimir += 1
                print(f"El ganador de la partida {i+1} es Vladimir")
            else:
                puntosLevon += 1
                print(f"El ganador de la partida {i+1} es Levon")
            time.sleep(0.15)
        else:
            print(f"Ronda {i+1}-Dia 3")
            print(f"{arregloNombres[idxMagnus]} vs {arregloNombres[idxLevon]}")
            if(arregloRatings[idxMagnus] > arregloRatings[idxLevon]):
                puntosMagnus += 1
                print(f"El ganador de la partida {i+1} es Magnus")
            else:
                puntosLevon += 1
                print(f"El ganador de la partida {i+1} es Levon")
            time.sleep(0.15)
            
            if(arregloRatings[idxVladimir] > arregloRatings[idxPeter]):
                puntosVladimir += 1
                print(f"El ganador de la partida {i+1} es Vladimir")
            else:
                puntosPeter += 1
                print(f"El ganador de la partida {i+1} es Peter")
            time.sleep(0.15)
    diccionario = {"Magnus":puntosMagnus,"Vladimir":puntosVladimir,"Peter":puntosPeter,"Levon":puntosLevon}
    ganador = max(diccionario, key=diccionario.get)
    return ganador    

#Funcion D
async def fase_final_async(ganador:str)->str:
    puntosGanador,puntosCampeonVigente = 0,0
    nombreCampeonVigente = "Anand"    
    #Se jugaran 12 partidas
    for i in range(11):
        probabilidadGanador = random.randint(0,10)
        probabilidadCampeon = random.randint(0,10)
        if probabilidadGanador > probabilidadCampeon:
            puntosGanador += 1
            print(f"El ganador de la partida {i+1} es {ganador}")
        elif probabilidadGanador == probabilidadCampeon:
            puntosGanador += 0.5
            puntosCampeonVigente += 0.5
            print(f"La partida {i+1} termino en empate")
        else:
            puntosCampeonVigente += 1
            print(f"El ganador de la partida {i+1} es {nombreCampeonVigente}")
        await asyncio.sleep(0.15)

    diccionario = {ganador:puntosGanador,nombreCampeonVigente:puntosCampeonVigente}
    ganador = max(diccionario, key=diccionario.get)
    return ganador

#Funcion E
def fase_final_sync(ganador:str)->str:
    puntosGanador,puntosCampeonVigente = 0,0
    nombreCampeonVigente = "Anand"    
    #Se jugaran 12 partidas
    i = 0
    while True:
        if puntosGanador >= 6.5 or puntosCampeonVigente >= 6.5:
            break
        probabilidadGanador = random.randint(0,10)
        probabilidadCampeon = random.randint(0,10)
        if probabilidadGanador > probabilidadCampeon:
            puntosGanador += 1
            print(f"El ganador de la partida {i+1} es {ganador}")
        elif probabilidadGanador == probabilidadCampeon:
            puntosGanador += 0.5
            puntosCampeonVigente += 0.5
            print(f"La partida {i+1} termino en empate")
        else:
            puntosCampeonVigente += 1
            print(f"El ganador de la partida {i+1} es {nombreCampeonVigente}")
        i = i + 1
        time.sleep(0.15)
    diccionario = {ganador:puntosGanador,nombreCampeonVigente:puntosCampeonVigente}
    ganador = max(diccionario, key=diccionario.get)
    print(f"\n\n{diccionario}")
    return ganador


if __name__ == "__main__":
    leerArchivo()
    inicioAsync = time.time()
    ganador = asyncio.run(fase_rondas_async())
    finalAsync = time.time()
    print(f"El tiempo de ejecucion de la fase de rondas en modo asincrono es {finalAsync-inicioAsync}")
    print(f"El ganador es {ganador}")

    inicioSync = time.time()
    ganador = fase_rondas_sync()
    finalSync = time.time()
    print(f"El tiempo de ejecucion de la fase de rondas en modo sincrono es {finalSync-inicioSync}")
    print(f"El ganador es {ganador}")

    inicioAsync = time.time()
    campeon = asyncio.run(fase_final_async(ganador))
    finalAsync = time.time()
    print(f"El campeón es: {campeon}")
    print(f"El tiempo de ejecucion de la fase final en modo asincrono es {finalAsync-inicioAsync}")

    inicioSync = time.time()
    campeon = fase_final_sync(ganador)
    finalSync = time.time()
    print(f"El campeón es: {campeon}")
    print(f"El tiempo de ejecucion de la fase final en modo sincrono es {finalSync-inicioSync}")
    
    



    

