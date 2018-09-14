#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Construct Struct
#from construct import *

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX

class enlace(object):
    """ This class implements methods to the interface between Enlace and Application
    """

    def __init__(self, name):
        """ Initializes the enlace class
        """
        self.fisica      = fisica(name)
        self.rx          = RX(self.fisica)
        self.tx          = TX(self.fisica)
        self.connected   = False

    def enable(self):
        """ Enable reception and transmission
        """
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        """ Disable reception and transmission
        """
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()

    ################################
    # Application  interface       #
    ################################
    def sendData(self, data):
        """ Send data over the enlace interface
        """
        dataslice=self.tx.slicedata(data)
        synch=self.synchClient()
        if synch:
            time.sleep(1)

            print("SERAO ENVIADOS {} PACOTES".format(len(dataslice)))

            for i in range(len(dataslice)):

                tipo_check = False

                while not tipo_check:
                    # Envia tipo 4
                    print("##### ENVIANDO TIPO 4 #####")

                    head = self.tx.makeHead(dataslice[i], 4, i, len(dataslice)-1)
                    self.tx.sendBuffer(dataslice[i], head)

                    # Espera tipo 5/6
                    print("##### ESPERANDO TIPO 5/6 #####")
                    data_1, check, numero, total= self.rx.getNData()
                    tipo = data_1[7]

                    if tipo == 5:
                        print("##### RECEBI TIPO 5 ######")
                        tipo_check = True
                        break

                    if tipo == 6:
                        print("##### RECEBI TIPO 6 ######")
                        self.rx.clearBuffer()

                    else:
                        print("##### NAO RECEBI TIPO 5 OU 6 OU 8######")
                        self.rx.clearBuffer()

            print("##### ENVIANDO TIPO 7 #####")
            self.sendFiller(7)
            


    def sendFiller(self, tipo, esperado=0):
        fillerData = 0
        fillerBuffer = fillerData.to_bytes(1, byteorder="big")
        if tipo == 8:
            head = self.tx.makeHead(fillerBuffer, tipo, 0, 0, esperado)
        else:
            head = self.tx.makeHead(fillerBuffer, tipo)
        self.tx.sendBuffer(fillerBuffer, head)

    def synchClient(self):
        tipo = 0
        # Envia Tipo 1
        self.sendFiller(1)
        print("##### TIPO 1 ENVIADO #####")

        # Recebe Tipo 2
        data, check, numero, total =self.rx.getNData()
        tipo=data[7]

        if tipo == 2:
            print("##### RECEBI TIPO 2 #####")
            # Envia Tipo 3
            self.sendFiller(3)
            print("Tipo 3 enviado")

            return True

        else:
            print(" ###### Não recebi tipo 2 ######")
            return False

    def synchServer(self):
        # Recebe tipo 1
        tipo = 0
        data, check, numero, total = self.rx.getNData()
        tipo=data[7]
        if tipo == 1:
            print("###### Recebi tipo 1 ######")
            # Envia tipo 2
            self.sendFiller(2)
            print("Tipo 2 Enviado")
            data, check, numero, total =self.rx.getNData()
            tipo=data[7]
            if tipo == 3:
                print("###### Recebi tipo 3 ######")
                return True
            else:
                print(" ###### Não recebi tipo 3 ######")
                return False
        else:
            print(" ###### Não recebi tipo 1 ######")
            return False







    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        print('entrou na leitura e tentara ler ' )

        dataList = []
        count = -1

        synch = self.synchServer()

        if synch:

            while True:

                tipo_check = False
                count += 1

                while  not tipo_check:
                    print("##### ESPERANDO TIPO 4 #####")
                    data, check_tamanho, numero, total = self.rx.getNData()
                    print("NUMERO = {}".format(numero))
                    print("COUNT = {}".format(count))
                    if count == numero:
                        numCheck = True
                    else:
                        numCheck = False

                    if check_tamanho and numCheck:
                        print("##### ENVIANDO TIPO 5 #####")
                        self.sendFiller(5)
                        tipo_check = True
                        break
                    else:
                        if numCheck:
                            print("##### ENVIANDO TIPO 6 #####")
                            self.sendFiller(6)
                        else:
                            print("##### ENVIANDO TIPO 8 #####")
                            self.sendFiller(8, count)

                            

                dataList.append(data)

                print("NUMERO = {}".format(numero))
                print("TOTAL = {}".format(total))

                if numero == total:
                    break
            
            print("##### ESPERANDO TIPO 7 #####")
            data_7, check_tamanho, numero, total = self.rx.getNData()
            tipo = data_7[7]

            if tipo == 7:
                print("##### RECEBI TIPO 7 #####")

            datafull = bytearray()

            print("RECEBI {} PACOTES".format(len(dataList)))

            for i in dataList:
                datafull = datafull + i


            return(datafull, len(data))
