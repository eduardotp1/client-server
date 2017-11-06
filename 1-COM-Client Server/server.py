#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Prof. Rafael Corsi
#  Abril/2017
#  Aplicação
####################################################

from enlace import *
import time

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

serialName = "/dev/ttyACM1"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "COM3"                   # Windows(variacao de)

def main():
    # Inicializa enlace
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()


    # Endereco da imagem a ser salva
    imageW = "./imgs/recebida.png"

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

     # espera o fim da transmissão
    while(com.tx.getIsBussy()):
        pass
        
    # Atualiza dados da transmissão
    txSize = com.tx.getStatus()


    # Faz a recepção dos dados
    print ("Recebendo dados .... ")
    #rxBuffer, nRx = com.getData(txLen)
    #temp1,tx = com.getData(1)
    if com.waitConnection():
        time.sleep(0.5)
        response = com.getData()
        rxBuffer, nRx, real_nRx, package_type = response
        begin=time.time()
       


        end=time.time()
        lost_bytes = nRx-real_nRx
        while lost_bytes !=0:
            com.sendNack()
            time.sleep(1)
        # log
        print ("Lido              {} bytes ".format(nRx))
        print ("Perdidos            {} bytes ".format(lost_bytes))
        # Salva imagem recebida em arquivo
        print("-------------------------")
        print ("Salvando dados no arquivo :")
        print (" - {}".format(imageW))
        f = open(imageW, 'wb')
        f.write(rxBuffer)
        # Fecha arquivo de imagem
        f.close()

        print("Tempo de recepção: {}".format(end - begin))

        # Fecha arquivo de imagem
        f.close()

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com.disable()
        return "File Received"
    else:
        return "Error"
        f.close()
        com.disable()

        print("Tempo de recepção: {}".format(end - begin))

        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com.disable()