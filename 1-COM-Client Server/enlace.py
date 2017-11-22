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
        data = Pacote(data, "data").empacota()
        self.tx.sendBuffer(data)

    def getData(self, size):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        package = self.rx.getHead()
        print(package, "enlace,57")
        data = desempacota(package)
        return(data[0], data[1],(len(data[0])),data[2])

    def sendACK(self):
        package = Pacote(None,"ACK").empacota()
        self.tx.sendBuffer(package)
    
    def sendNACK(self):
        package = Pacote(None,"NACK").empacota()
        self.tx.sendBuffer(package)
    
    def sendSync(self):
        package = Pacote(None,"sync").empacota()
        self.tx.sendBuffer(package)



    def waitConnection(self):
        print("Preparing to receive image")
        while self.connected ==  False:
            response = self.getData(self)
            print("Waiting sync...")
            if response[3] == "sync":
                print("Sync received")
                self.sendSync()
                time.sleep(0.5)
                self.sendACK()
                print("ACK SENT")
                response = self.getData(self)
                if response[3] == "ACK":
                    print("Ready to receive package")
                    return True
            else:
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
                    response = self.getData(self)
                    if response[3] == "sync":
                        print("Sync received")
                        response = self.getData(self)
                        if response[3] == "ACK":
                            print("ACK received")
                            time.sleep(0.5)
                            self.sendACK()
                            print("Connection established")
                            return True
                    else:
                        return False      
            else:
                if ((time.time() - comeco) > 5):
                    print ("Passou 5 s")
                    self.sendSync()
                    timeout = True
                    