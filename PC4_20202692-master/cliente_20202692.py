import socket
import time

SOCKET_BUFFER_SIZE = 10000

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddress = ("192.168.56.1", 5000)

    print(f"Connectando a {serverAddress[0]}:{serverAddress[1]}")
    sock.connect(serverAddress)

    try:
        while True:
            mensaje = input()
            sock.sendall(mensaje.encode())
            data = sock.recv(SOCKET_BUFFER_SIZE)
            print(f"Recibido: {data.decode()}")
            if mensaje == "Cerrar Sesion":
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Cerrando conexion")
        sock.close()