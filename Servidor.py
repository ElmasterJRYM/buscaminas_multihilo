import socket
import sys
import threading
from random import *
import numpy


def Matriz(n, m, mi):
    matriz = numpy.chararray((n, m))
    matriz[:] = 'O'
    minas = mi
    while minas != 0:
        x = randint(0, n - 1)
        y = randint(0, m - 1)
        if matriz[x][y] != 'X':
            matriz[x][y] = 'X'
            minas -= 1
    return matriz


def Vacia(n, m):
    matriz = numpy.chararray((n, m))
    matriz[:] = '*'
    return matriz

class Tablero():
    def __init__(self, di, opcion):
        self.Estado = 1
        self.Ganador = 0
        self.dificultad = di
        if self.dificultad == 1:
            self.m = 9
            self.n = 9
            self.minas = 10
            self.libres = (self.m * self.n) - self.minas
            self.abiertas = 0
            if opcion == 1:
                self.tablero = Matriz(self.n, self.m, self.minas)
            elif opcion == 0:
                self.tablero = Vacia(self.n, self.m, )
        elif self.dificultad == 2:
            self.m = 16
            self.n = 16
            self.minas = 40
            self.libres = (self.m * self.n) - self.minas
            self.abiertas = 0
            if opcion == 1:
                self.tablero = Matriz(self.n, self.m, self.minas)
            elif opcion == 0:
                self.tablero = Vacia(self.n, self.m, )

    def imprimir(self):
        print("  ", end='')
        for i in range(len(self.tablero[0])):
            print("\t", i + 1, end="")
        print()
        print()
        for i in range(len(self.tablero)):
            print(i + 1, end="")
            for j in range(len(self.tablero[i])):
                print("\t", str(self.tablero[i][j], 'utf-8'), end=' ')
            print()

    def isMina(self, x, y):

        if str(self.tablero[x - 1][y - 1], 'utf-8') == 'X':
            return 1
        else:
            return 0

    def destaparM(self, x, y):
        self.tablero[x - 1][y - 1] = 'X'

    def destapar(self, x, y):
        self.tablero[x - 1][y - 1] = 'O'

    def Juego(self):
        return self.Estado and 1

    def cEstado(self, e):
        self.Estado = e

    def getGanador(self):
        self.Ganador

    def isAbierta(self, x, y):

        if str(self.tablero[x - 1][y - 1]) == str("*"):
            return 0
        else:
            return 1

def servirPorSiempre(socketTcp, listaconexiones):
    BuscaminasF = Tablero(1, 1)
    BuscaminasD = Tablero(2, 1)
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            listaconexiones.append(client_conn)
            Dificultad = client_conn.recv(bufferSize)
            print("hola! estas conectado a", client_addr)
            print("Bienvenido, comenzaremos un nuevo juego de buscaminas")
            if int(Dificultad)==1:
                thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr, BuscaminasF])
            else:
                thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr, BuscaminasD])
            thread_read.start()
            gestion_conexiones(listaConexiones)
    except Exception as e:
        print(e)

def gestion_conexiones(listaconexiones):
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    print("hilos activos:", threading.active_count())
    print("enum", threading.enumerate())
    print("conexiones: ", len(listaconexiones))
    print(listaconexiones)


def recibir_datos(sc, addr,Buscaminas):
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(addr, cur_thread.name))
        while True:

            while Buscaminas.Estado == 1:
                Buscaminas.imprimir()
                X = sc.recv(bufferSize)
                Y = sc.recv(bufferSize)

                if Buscaminas.isMina(int(X), int(Y)):
                    Buscaminas.Estado = 0
                    Buscaminas.Ganador = 0
                    r = '1'
                    sc.send(r.encode('utf-8'))
                else:
                    r = '0'
                    sc.send(r.encode('utf-8'))
                Buscaminas.abiertas += 1
                if Buscaminas.libres == Buscaminas.abiertas:
                    Buscaminas.Estado = 0
                    Buscaminas.Ganador == 1;

            print("Juego Terminado")

            if Buscaminas.Ganador == 1:
                print("lo lograste, has ganado!!")
            else:
                print("Lo siento has perdido, mas suerte para la proxima")
            break
        sc.close()


    except Exception as e:
        print(e)
    finally:
        sc.close()


listaConexiones = []
HOST = "192.168.100.5"
PORT = 65432
bufferSize = 1024
r='0'
UDPServerSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPServerSocket.bind((HOST, PORT))
UDPServerSocket.listen(3)
print("El servidor TCP está disponible y en espera de solicitudes")

servirPorSiempre(UDPServerSocket, listaConexiones)
