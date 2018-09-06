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

# Threads
import threading

# Class
class RX(object):
    """ This class implements methods to handle the reception
        data over the p2p fox protocol
    """

    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024
        self.EOP         = 26090112

    def thread(self):
        """ RX thread, to send data in parallel with the code
        essa é a funcao executada quando o thread é chamado.
        """
        while not self.threadStop:
            if(self.threadMutex == True):
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp
                time.sleep(0.01)

    def threadStart(self):
        """ Starts RX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill RX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the RX thread to run

        This must be used when manipulating the Rx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the RX thread (after suspended)
        """
        self.threadMutex = True

    def getIsEmpty(self):
        """ Return if the reception buffer is empty
        """
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        """ Return the total number of bytes in the reception buffer
        """
        return(len(self.buffer))

    def getAllBuffer(self, len):
        """ Read ALL reception buffer and clears it
        """
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData):
        """ Remove n data from buffer
        """
        self.threadPause()
        b           = self.buffer[0:nData]
        self.buffer = self.buffer[nData:]
        self.threadResume()

        return(b)

    def getNData(self):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """
#        temPraLer = self.getBufferLen()
#        print('leu %s ' + str(temPraLer) )

        #if self.getBufferLen() < size:
            #print("ERROS!!! TERIA DE LER %s E LEU APENAS %s", (size,temPraLer))
        size = 0
        while(self.getBufferLen() != size or size == 0):

            time.sleep(0.4)

            size = self.getBufferLen()

        mensagem = self.parseBuffer(self.getBuffer(size))
        print(mensagem)
#
        return(mensagem)


    def parseBuffer(self, buffer):

        eop = self.EOP.to_bytes(12,byteorder="big")

        found = False

        if len(buffer)>24:
            for i in range(len(buffer)):

                if buffer[i:i+len(eop)] == eop:
                    start_ofEop = i
                    found = True

            if found == True:
                print("EOP encontrado no byte {}".format(start_ofEop))

                head = buffer[0:11]

                head_size = head[8:11]
                int_size = int.from_bytes(head_size, byteorder="big")

                head_type = head[7]

                if head_type == 1:

                    print("RECEBI TIPO 1")

                mensagem = buffer[12:start_ofEop]

                if int_size == len(mensagem):
                    print("TAMANHO CORRETO DE IMAGEM")
                else:
                    print("TAMANHO ERRADO DE IMAGEM")

                overhead = len(buffer)/len(mensagem)
                print("OVERHEAD = {}".format(overhead))

                return mensagem
            else:
                print("ERRO - EOP nao encontrado")




    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""
