# -*- coding: utf-8 -*-
 
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
        print("ENVIANDO DATA")
        data = Pacote(data, "data").empacota()
        self.tx.sendBuffer(data)
        print("***ENVIANDO DATA***")

    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        package = self.rx.getHeadPayload()
        print(binascii.hexlify(package),"getData","linha 57")
        data = desempacota(package)
        print("***RECEBENDO DATA***")
        return(data[0], data[1],(len(data[0])),data[2])

    def sendACK(self):
        package = Pacote(None,"ACK").empacota()
        print("***ENVIANDO ACK***")
        self.tx.sendBuffer(package)
    
    def sendNACK(self):
        package = Pacote(None,"NACK").empacota()
        print("***ENVIANDO NACK***")
        self.tx.sendBuffer(package)
    
    def sendSync(self):
        package = Pacote(None,"sync").empacota()
        self.tx.sendBuffer(package)
        print("***ENVIANDO SYNC***")

    def waitConnection(self):
        print("Preparing to receive image")
        while self.connected ==  False:
            response = self.getData()
            print("Waiting sync...")
            if response[3] == "sync":
                print("Sync received")
                self.sendSync()
                print("***ENVIOU SYNC***")
                time.sleep(3)
                self.sendACK()
                time.sleep(3)
                print("ACK SENT")
                response = self.getData()
                time.sleep(3)
                print("Waiting ACK..")
                if response[3] == "ACK" or "sync":
                    print("***RECEBEU ACK OU SYNC***")
                    print("Ready to receive package")
                    return True
            else:
                print("***NÃO RECEBEU SYNC INICIAL***")
                return False

    def establishConnection(self):
        print("Preparing to send image")
        timeout = False
        print("Sending sync...")
        comeco = time.time()

        while self.connected ==  False:
            if timeout:
                timeout=False
                comeco = time.time()
                print("--Waiting sync...")
                if self.rx.getIsEmpty() == False:
                    self.sendSync()
                    time.sleep(2)
                    print("***ENVIOU SYNC***")
                    response = self.getData()
                    if response[3] == "sync":
                        print("Sync received")
                        response = self.getData()
                        print("Waiting ACK..")
                        if response[3] == "ACK":
                            print("ACK received")
                            time.sleep(3)
                            self.sendACK()
                            print("***ENVIOU ACK***")
                            print("Connection established")
                            return True
                    else:
                        print("***NÃO RECEBEU SYNC INICIAL***")
                        return False      
            else:
                if ((time.time() - comeco) > 6):
                    print ("Passou 6 s")
                    self.sendSync()
                    print("***ENVIOU SYNC timeout***")
                    timeout = True
                    