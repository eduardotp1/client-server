# -*- coding: utf-8 -*-
 
from enlace import *
import time
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "COM0"                   # Windows(variacao de)

def main():
    # Inicializa enlace
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

# Endereco da imagem a ser transmitida
    # imageR = "./imgs/imageE.png"

    # Endereco da imagem a ser salva
    imageW = "./imgs/recebida.png"

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    #txLen = 3093

    # Faz a recepção dos dados
    print ("Recebendo dados .... ")
    #rxBuffer, nRx = com.getData(txLen)
    temp1,tx = com.getData(1)
    inicio=time.time()
    temp2, nRx = com.getData(3092)

    rxBuffer = temp1 + temp2

    fim=time.time()
    # log
    print ("Lido              {} bytes ".format(nRx))

    # Salva imagem recebida em arquivo
    print("-------------------------")
    print ("Salvando dados no arquivo :")
    print (" - {}".format(imageW))
    f = open(imageW, 'wb')
    f.write(rxBuffer)


    print("Tempo de recepção: {}".format(fim - inicio))

    # Fecha arquivo de imagem
    f.close()

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

if __name__ == "__main__":
    main()
