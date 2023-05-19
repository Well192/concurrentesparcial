import threading
import math
import random
import re
import socket
import threading

sumaarray = [0] * 40

class TCPClient50:
    def __init__(self, ip, listener):
        self.servermsj = None
        self.SERVERIP = ip
        self.SERVERPORT = 4444
        self.mMessageListener = listener
        self.mRun = False
        self.out = None
        self.incoming = None

    def sendMessage(self, message):
        if self.out is not None:
            self.out.write(message + '\n')
            self.out.flush()

    def stopClient(self):
        self.mRun = False

    def run(self):
        self.mRun = True
        try:
            serverAddr = socket.gethostbyname(self.SERVERIP)
            print("TCP Client - C: Conectando...")
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((serverAddr, self.SERVERPORT))
            try:
                self.out = clientSocket.makefile('w')
                print("TCP Client - C: Sent.")
                print("TCP Client - C: Done.")
                self.incoming = clientSocket.makefile('r')
                while self.mRun:
                    self.servermsj = self.incoming.readline()
                    if self.servermsj is not None and self.mMessageListener is not None:
                        self.mMessageListener(self.servermsj)
                    self.servermsj = None
            except Exception as e:
                print("TCP - S: Error", e)
            finally:
                clientSocket.close()
        except Exception as e:
            print("TCP - C: Error", e)

class Cliente50:
    def __init__(self):
        
        self.mTcpClient = None
        self.sc = None

    def main(self):
        objcli = Cliente50()
        objcli.iniciar()

    def iniciar(self):
        def run():
            def message_received(message):
                self.ClienteRecibe(message)

            self.mTcpClient = TCPClient50("127.0.0.1", message_received)
            self.mTcpClient.run()

        thread = threading.Thread(target=run)
        thread.start()

        salir = "n"
        self.sc = input()
        print("Cliente bandera 01")
        while salir != "s":
            salir = self.sc.nextLine()
            self.ClienteEnvia(salir)
        print("Cliente bandera 02")

    def ClienteRecibe(self, llego):
        print("CLINTE50 El mensaje::" + llego)
        if "evalua" in llego:
            arrayString = llego.split()
            polinomio = arrayString[1]
            a = int(arrayString[2])
            b = int(arrayString[3])
            cantidad = int(arrayString[4])
            rango = int(arrayString[5])
            print("El polinomio: " + polinomio + ", el min:" + str(a) + " el max:" + str(b) + ", " + str(cantidad))
            self.procesar(polinomio, a, b, cantidad, rango)

    def ClienteEnvia(self, envia):
        if self.mTcpClient is not None:
            self.mTcpClient.sendMessage(envia)

    def funcion(self, fin):
        suma = 0
        for j in range(fin + 1):
            suma += math.sin(j * random.random())
        return suma

    def procesar(self, polinomio, a, b, cantidad, rango):
        numIntervalos = int(((b - a) * cantidad) / rango)

        H = 6  

        dx = rango / cantidad

        limite = numIntervalos // H

        todos = [None] * 40
        for i in range(H - 1):
            todos[i] = tarea0101((i * dx * limite + a), ((i * dx * limite) + (dx * limite) + a), i, dx, polinomio)
            todos[i].start()

        todos[H - 1] = tarea0101(((dx * limite * (H - 1)) + a), b, H - 1, dx, polinomio)
        todos[H - 1].start()
        for i in range(H):
            todos[i].join()

        sumatotal = 0.0
        for i in range(H):
            
            sumatotal += sumaarray[i]

        self.ClienteEnvia("rpta " + str(sumatotal * dx))

class tarea0101(threading.Thread):
    def __init__(self, min_, max_, id_, dx, polinomio_):
        threading.Thread.__init__(self)
        self.max = max_
        self.min = min_
        self.id = id_
        self.dx = dx
        self.polinomio = polinomio_

    def run(self):
        suma = 0.0

        i = self.min
        while i < self.max:
            polinomio = Polinomio(self.polinomio, i)
            suma += polinomio.imprimirCoeficientes()
            i += self.dx
        sumaarray[self.id] = suma
        print(" min:" + str(self.min) + " max:" + str(self.max) + " id:" + str(self.id) + " suma:" + str(suma))
        
        # envio 7x^1+8x^2 5 10 200

# Clase Polinomio
class Polinomio:
    def __init__(self, polinomio, numero):
        self.coeficientes = []
        self.x = numero

        # Dividir el polinomio en términos individuales
        terminos = re.split(r'\s*\+\s*|\s*\-\s*', polinomio)

        # Determinar el grado máximo del polinomio
        gradoMaximo = 0
        for termino in terminos:
            grado = self.obtenerGrado(termino)
            gradoMaximo = max(grado, gradoMaximo)

        # Inicializar el arreglo de coeficientes
        self.coeficientes = [0.0] * (gradoMaximo + 1)

        # Asignar los coeficientes en el arreglo
        for termino in terminos:
            coeficiente = self.obtenerCoeficiente(termino)
            grado = self.obtenerGrado(termino)
            self.coeficientes[grado] = coeficiente

    def imprimirCoeficientes(self):
        resultado = 0.0
        for i in range(len(self.coeficientes)):
            resultado += self.coeficientes[i] * (self.x ** i)
        return resultado

    def obtenerCoeficiente(self, termino):
        coeficienteStr = termino.split('x')[0]
        if coeficienteStr == '':
            return 1.0
        elif coeficienteStr == '-':
            return -1.0
        else:
            return float(coeficienteStr)

    def obtenerGrado(self, termino):
        if '^' in termino:
            gradoStr = termino.split('^')[1]
            return int(gradoStr)
        elif 'x' in termino:
            return 1
        else:
            return 0

# Ejecutar el programa
cliente = Cliente50()
cliente.main()
