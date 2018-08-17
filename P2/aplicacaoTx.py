print("comecou Tx")

from enlace import *
import time

serialName = "COM5"

print("porta COM aberta com sucesso")

def send(filename):


    com = enlace(serialName)
    com.enable()

    print("comunicação aberta")

    print ("gerando dados para transmissao :")

    ListTxBuffer =list()
    with open(filename, "rb") as imageFile:
        f = imageFile.read()
        txBuffer = bytearray(f)
    txLen    = len(txBuffer)

    print("tentado transmitir .... {} bytes".format(txLen))
    com.sendData(txBuffer)

    txSize = com.tx.getStatus()

    print("-------------------------")
    print("Comunicação TX encerrada")
    print("-------------------------")
    com.disable()
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))

# if __name__ == "__main__":
#     send()
