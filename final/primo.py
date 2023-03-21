import math
import multiprocessing as mp
import time
import matplotlib.pyplot as plt

def esPrimo(n: int) -> bool:
    primo = True
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            primo = False
            break
    return primo


def esPrimoParalelo(n:int, inicio:int,fin:int)->bool:
    if n < 2:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    
    for i in range(inicio, fin, 2):
        if n % i == 0:
            return False
    
    return True


def poolProcesos(n:int, inicio:int, fin:int)->bool:
    pool = mp.Pool(processes=2)
    resultado = pool.starmap(esPrimoParalelo, [(n, inicio, fin)])
    pool.close()
    return resultado[0]


def poolProcesosV2(n:int, inicio:int,fin:int,numProcesos:int)->bool:
    pool = mp.Pool(processes=numProcesos)
    resultado = pool.starmap(esPrimoParalelo, [(n,inicio,inicio + i + fin) for i in range(numProcesos)])
    pool.close()
    return resultado[0]

if __name__ == '__main__':
    n = 2345678911111111
    print("Parte A)")
    inicioA = time.time()
    print(esPrimo(n))
    finA = time.time()
    print(f"Tiempo de ejecución: {finA- inicioA}")

    print(50*'=')

    print("Parte B)")
    inicio = time.time()
    print(poolProcesos(n, 2, int(math.sqrt(n)) + 1))
    fin = time.time()
    print(f"Tiempo de ejecución: {fin - inicio}")

    #Usar asserts para verificar que el resultado es correcto
    assert esPrimo(n) == poolProcesos(n, 2, int(math.sqrt(n)) + 1)

    
    speedUp = (finA - inicioA) / (fin - inicio)
    print(f"SpeedUp: {speedUp}")

    print(50*'=') 

    print("Parte C)")
    tiemposEjecucion = []
    procesos = [2, 4, 8, 16]

    for i in procesos:
        inicio = time.time()
        poolProcesosV2(n, 2, int(math.sqrt(n)) + 1, i)
        fin = time.time()
        tiemposEjecucion.append(fin - inicio)

    plt.plot(procesos, tiemposEjecucion)
    plt.xlabel("Procesos")
    plt.ylabel("Tiempo de ejecución")
    plt.savefig("tiemposEjecucion.png")

    print("¿Aumentar el número de procesos hace que disminuya el tiempo de ejecución, o no necesariamente?")
    print("No necesariamente, ya que el tiempo de ejecución depende de la cantidad de procesos que se usen, pero también de la cantidad de datos que se procesen, ya que si se procesan muchos datos, el tiempo de ejecución aumenta, pero si se procesan pocos datos, el tiempo de ejecución disminuye.")
    print("Y como vemos en el gráfico mientras haya más procesos el tiempo de ejecución aumenta, pero cuando hay pocos procesos el tiempo de ejecución disminuye.")

