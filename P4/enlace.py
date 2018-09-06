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
        synch=self.synchClient()
        if synch:
            head = self.tx.makeHead(data, 4)
            self.tx.sendBuffer(data, head)

    def synchClient(self):
        tipo = 0
        # Envia Tipo 1
        fillerData = 0
        fillerBuffer = fillerData.to_bytes(1, byteorder="big")
        head = self.tx.makeHead(fillerBuffer, 1)
        self.tx.sendBuffer(fillerBuffer, head)
        print("tipo 1 Enviado")


        # Recebe Tipo 2
        data=self.rx.getNData()
        tipo=data[6:8]

        if tipo == 2:
            print("##### RECEBI TIPO 2 #####")
            # Envia Tipo 1
            fillerData = 0
            fillerBuffer = fillerData.to_bytes(1, byteorder="big")
            head = self.tx.makeHead(fillerBuffer, 3)
            self.tx.sendBuffer(fillerBuffer, head)
            print("Tipo 3 enviado")

            return True

        else:
            print(" ###### Não recebi tipo 2 ######")
            return False

    def synchServer(self):
        #recebe tipo 2
        tipo = 0
        data=self.rx.getNData()
        tipo=data[6:8]
        print(data)
        if tipo == 1:
            print("###### Recebi tipo 1 ######")
            fillerData = 0
            fillerBuffer = fillerData.to_bytes(1, byteorder="big")
            head = self.tx.makeHead(fillerBuffer, 2)
            self.tx.sendBuffer(fillerBuffer, head)
            print("Tipo 2 Enviado")
            data=self.tx.getNData()
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
        synch = self.synchServer()
        if synch:

            data = self.rx.getNData()

        return(data, len(data))
