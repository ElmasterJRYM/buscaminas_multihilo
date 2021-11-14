from time import time
import socket
import numpy
import random
class operaciones:
    def creaMatriz(n, m, mi):
        matriz = numpyp.chararray((n, m))
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

class Tablero:
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
                self.tablero = operaciones.creaMatriz(self.n, self.m, self.minas)
            elif opcion == 0:
                self.tablero = operaciones.Vacia(self.n, self.m, )
        elif self.dificultad == 2:
            self.m = 16
            self.n = 16
            self.minas = 40
            self.libres = (self.m * self.n) - self.minas
            self.abiertas = 0
            if opcion == 1:
                self.tablero = operaciones.creaMatriz(self.n, self.m, self.minas)
            elif opcion == 0:
                self.tablero = operaciones.Vacia(self.n, self.m, )

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

HOST = "192.168.100.5"
PORT = 65432
bufferSize = 1024
TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPClientSocket.connect((HOST, PORT))
print("Conectado al Servidor bienvenido al juego de buscaminas")

Dificultad=input ("\n1.Facil\n2.Dificil.\n\nIngresa la dificultad: ")
TCPClientSocket.send(Dificultad.encode('utf-8'))
Buscaminas=Tablero(int(Dificultad),0)
tiempo_inicial = time()
print("Por favor espera, el juego esta a punto de comensar\n\n")
while Buscaminas.Estado==1:
          print()
          print()
          Buscaminas.imprimir()
          XY = input("\nIngresa las cordenadas de la casilla que quieres destapar separadas por un espacio: (X Y):  ")
          X, Y = XY.split(' ')
          TCPClientSocket.send(X.encode('utf-8'))
          TCPClientSocket.send(Y.encode('utf-8'))
          Respuesta = TCPClientSocket.recv(bufferSize)
          if int(Respuesta) == 1:
                  Buscaminas.Estado = 0
                  Buscaminas.destaparM(int(XY[0]), int(XY[2]))
                  Buscaminas.Ganador == 0;
          elif int(Respuesta) == 0:
                  Buscaminas.destapar(int(XY[0]), int(XY[2]))
                  Buscaminas.abiertas += 1
                  if Buscaminas.libres == Buscaminas.abiertas:
                      Buscaminas.Estado = 0
                      Buscaminas.destaparM(int(XY[0]), int(XY[2]))
                      Buscaminas.Ganador == 1



tiempo_final = time()
print("El juego ha terminado")
Buscaminas.imprimir()
if Buscaminas.Ganador==1:
    print("Felicitaciones, ganaste!!")
else:
    print("Has perdido, suerte para la proxima! :c ")
tiempo_ejecucion = tiempo_final - tiempo_inicial
print ("El tiempo de juego: ",tiempo_ejecucion)
TCPClientSocket.close()
