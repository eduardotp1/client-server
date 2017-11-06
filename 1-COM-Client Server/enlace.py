#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Prof. Rafael Corsi
#  Abril/2017
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Construct Struct
from construct import *

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX
from pacote import *

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
        package = Pacote(data, "data").buildPackage()
        self.tx.sendBuffer(package)

    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        package = self.rx.getHeadPayload()
        print(package)
        data = desempacota(package)
        return(data[0], data[1],(len(data[0])), data[2])

    def sendAck(self):
        #Envia os ACKs para autorizar inicio da conexão ou confirmar recebimentoss
        package = Pacote(None, "ACK").buildPackage()
        self.tx.sendBuffer(package)

    def sendNack(self):
        #Avisa que pacote chegou corrompido
        package = Pacote(None, "NACK").buildPackage()
        self.tx.sendBuffer(package)

    def sendSync(self):
        #Para estabelecer conexão
        package = Pacote(None, "sync").buildPackage()
        self.tx.sendBuffer(package)

    def waitConnection(self): #Papel do Server
        #print("connected", connected)
        #Fica conferindo recebimento do sync e se recebe, confirma enviando ack. Depois envia o sync e confirma se recebeu ack de confirmação.
        while self.connected ==  False:
            print("Loop waitconnection")
            response = self.getData()
            time.sleep(1)
            print("Waiting sync...")
            print("response", response)
            if response[3] == "sync":
                print("Sync received")
                self.sendSync()
                time.sleep(0.5)
                self.sendAck()
                time.sleep(0.5)
                print("ACK SENT")
                response = self.getData()
                if response[3] == "ACK":
                    print("Ready to receive package")
                    return True
                else:
                    time.sleep(0.5)
                    self.sendNack
                    return False
            else:
                print("falhou")
                time.sleep(1)
                self.sendNack()
                return False

        
    def establishConnection(self): #Papel do Client
        timeout = False
        print("waiting Sync...")
        begin = time.time()
        #Envia o Sync para iniciar e pega a resposta. Se tiver Ack (confirmação de recebimento sync), procura pelo recebimento de sync e envia ack. 
        while self.connected ==  False:
            if self.rx.getIsEmpty() == False:
                #parei de fazer aqui
                time.sleep(0.5)
                self.sendSync()
                time.sleep(1)
                response = self.getData()
                print("Waiting sync...")
                if response[3] == "sync":
                    print("Sync received")
                    response = self.getData()
                    if response[3] == "ACK":
                        print("ACK received")
                        time.sleep(0.5)
                        self.sendAck()
                        return True
                    else:
                        return False
                else:
                    return False                    
                   

    def verifyPackage(self, data):
        package = Pacote(data,"data").buildPackage()
        sizePack = len(package)
        expected = len(self.getData())
        if sizePack == expected:
            self.sendAck()
            return True
        else:
            self.sendNack()
            return False
    