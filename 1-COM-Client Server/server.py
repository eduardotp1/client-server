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
    if com.waitConnection():
        response = com.getData()
        rxBuffer, nRx, real_nRx, package_type = response
        inicio=time.time()


        
        lost_b=nRx - real_nRx
        fim=time.time()
        print ("Lido              {} bytes ".format(nRx))

        # Salva imagem recebida em arquivo
        print("-------------------------")
        print ("Salvando dados no arquivo :")
        print (" - {}".format(imageW))
        f = open(imageW, 'wb')
        f.write(rxBuffer)

        # Fecha arquivo de imagem
        f.close()

        print("Tempo de recepção: {}".format(fim - inicio))

    

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com.disable()
        return "Received"

    else:
        return "Error"
        f.close
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com.disable()

if __name__ == "__main__":
    main()
