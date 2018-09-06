print("comecou Tx")

from enlace import *
import time

serialName = "/dev/tty.usbmodem1461"

print("porta COM aberta com sucesso")

def send(filename="sent_image.png"):


    com = enlace(serialName)
    com.enable()

    print("comunicação aberta")

    print ("gerando dados para transmissao :")

    ListTxBuffer =list()
    with open(filename, "rb") as imageFile:
        f = imageFile.read()
        txBuffer = bytearray(f)
    txLen    = len(txBuffer)

    tempo_teorico = str((txLen*10)/(com.fisica.baudrate))
    print("Tempo teorico: " + tempo_teorico + " segundos")

    print("tentado transmitir .... {} bytes".format(txLen))
    com.sendData(txBuffer)

    txSize = com.tx.getStatus()




    print("-------------------------")
    print("Comunicação TX encerrada")
    print("-------------------------")
    com.disable()

if __name__ == "__main__":
     send()
