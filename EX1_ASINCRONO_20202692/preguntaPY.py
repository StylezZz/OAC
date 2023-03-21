import random
import numpy as np
import ctypes
import time
import statistics
import matplotlib.pyplot as plt

def producto1(arreglo,N,tope):
    menorQue , mayorQue = 0, 0
    for i in range(N):
        if arreglo[i]<tope:
            menorQue+=1
        else:
            mayorQue+=1
    
    return mayorQue*menorQue

def ctypesC():
    lib = ctypes.CDLL('./pregunta.so')
    lib.producto1.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.float32),
        ctypes.c_int,ctypes.c_float
    ]
    lib.producto1.restype = ctypes.c_int

    return lib.producto1

def ctypesASM():
    lib = ctypes.CDLL('./pregunta.so')
    lib.productoASM.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.float32),
        ctypes.c_int,ctypes.c_float
    ]
    lib.productoASM.restype = ctypes.c_int

    return lib.productoASM


if __name__ == '__main__':
    arreglo = np.random.rand(100).astype(np.float32)
    print("Python:")
    print(producto1(arreglo,len(arreglo),0.5))

    libC = ctypesC()
    print("C:")
    print(libC(arreglo,len(arreglo),0.5))

    libASM = ctypesASM()
    print("ASM:")
    print(libASM(arreglo,len(arreglo),0.5))

    #Probar los tiempos de ejecucion y sacar el SpeedUp
    L = [2 ** i for i in range(7,12)]
    tPythonFinal = []
    tCFinal = []
    tASMFinal = []

    speedUp_Python_C = []
    speedUp_Python_ASM = []

    for N in L:
        arreglo= np.random.rand(N).astype(np.float32)
        listPython = []
        listC = []
        listASM = []
        iteraciones = 100

        for it in range(iteraciones):
            tic1 = time.time()
            producto1(arreglo,len(arreglo),0.5)
            toc1 = time.time()
            listPython.append(toc1-tic1)

            tic2 = time.time()
            libC(arreglo,len(arreglo),0.5)
            toc2 = time.time()
            listC.append(toc2-tic2)

            tic3 = time.time()
            libASM(arreglo,len(arreglo),0.5)
            toc3 = time.time()
            listASM.append(toc3-tic3)

        tPythonFinal.append(statistics.mean(listPython))
        tCFinal.append(statistics.mean(listC))
        tASMFinal.append(statistics.mean(listASM))
        speedUp_Python_C.append(tPythonFinal[-1]/tCFinal[-1])
        speedUp_Python_ASM.append(tPythonFinal[-1]/tASMFinal[-1])


plt.plot(list(L),speedUp_Python_C,label="SpeedUp Python/C")
plt.plot(list(L),speedUp_Python_ASM,label="SpeedUp Python/ASM")
plt.xlabel("Tamaño de N")
plt.ylabel("Tiempo de ejecución")
plt.legend()
plt.savefig("SpeedUp.png")




