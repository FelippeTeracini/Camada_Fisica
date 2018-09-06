print("comecou Rx")

from enlace import *
import time

serialName = "COM5"

print("porta COM aberta com sucesso")

def receive():
    com = enlace(serialName)
    com.enable()

    print ("Recebendo dados .... ")
    bytesSeremLidos=com.rx.getBufferLen()

    rxBuffer, nRx = com.getData()

    print ("Lido              {} bytes ".format(nRx))

    with open("received_img.png", "wb") as imageFile2:
        f_image = imageFile2.write(rxBuffer)

    print("-------------------------")
    print("Comunicação RX encerrada")
    print("-------------------------")
    com.disable()

if __name__ == "__main__":
    receive()
