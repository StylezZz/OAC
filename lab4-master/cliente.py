import socket
import time

SOCKET_BUFFER = 1024

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddress = ("192.168.56.1", 5000)

    print(f"Conectando a {serverAddress[0]}:{serverAddress[1]}")

    sock.connect(serverAddress)

    #El cliente debe enviar un mensaje al servidor
    try:
        while True:
            mensaje = input()
            sock.sendall(mensaje.encode())
            data = sock.recv(SOCKET_BUFFER)
            print(f"Recibido: {data.decode()}")
            #Si el mensaje es Cerrar sesion se cierra la conexión
            if mensaje == "Cerrar Sesion":
                break
    except Exception as e:
        print(f"Exception {e}")
    finally:
        print("Cerrando conexión")
        sock.close()