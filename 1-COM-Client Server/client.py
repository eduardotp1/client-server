# -*- coding: utf-8 -*-
 
from enlace import *
import time

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

serialName = "/dev/ttyACM4"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "COM3"  

def main():
    # Inicializa enlace
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    # Endereco da imagem a ser transmitida
    imageR = "./imgs/imageC.png"

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    # Carrega imagem
    if com.establishConnection():
        print ("Carregando imagem para transmissão :")
        print (" - {}".format(imageR))
        print("-------------------------")
        txBuffer = open(imageR, 'rb').read()
        txLen    = 3093
        print(txLen)

        # Transmite imagem
        time.sleep(0.5)
        print("Transmitindo .... {} bytes".format(txLen))
        inicio = time.time()
        com.sendData(txBuffer)

        # espera o fim da transmissão
        while(com.tx.getIsBussy()):
            pass

        fim = time.time()
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com.disable()
        print("Tempo de transmissão: " + str(fim - inicio))

if __name__ == "__main__":
    main()
