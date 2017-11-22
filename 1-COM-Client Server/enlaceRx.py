# -*- coding: utf-8 -*-
import time
import binascii
# Threads
import threading

# Class
class RX(object):
    """ This class implements methods to handle the reception
        data over the p2p fox protocol
    """

    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024
        self.pay = False

    def thread(self):
        """ RX thread, to send data in parallel with the code
        """
        while not self.threadStop:
            if(self.threadMutex == True):
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp
                print(binascii.hexlify(self.buffer),"enlaceRx,linha 31")
                time.sleep(0.001)

    def threadStart(self):
        """ Starts RX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill RX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the RX thread to run
        This must be used when manipulating the Rx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the RX thread (after suspended)
        """
        self.threadMutex = True

    def getIsEmpty(self):
        """ Return if the reception buffer is empty
        """
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        """ Return the total number of bytes in the reception buffer
        """
        return(len(self.buffer))

    def getAllBuffer(self, len):
        """ Read ALL reception buffer and clears it
        """
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData):
        """ Remove n data from buffer
        """
        self.threadPause()
        b           = self.buffer[0:nData]
        self.buffer = self.buffer[nData:]
        self.threadResume()
        return(b)

    def getNData(self, size):
        """ Read N bytes of data from the reception buffer
        This function blocks until the number of bytes is received
        """
        while(self.getBufferLen() < size):
            time.sleep(0.05)

        return(self.getBuffer(size))


    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""


    def getHead(self):
        while(self.pay ==False):
            eop = self.buffer.find(b'\xaf, \xfc, \xa4, \xe7')
            if (eop == -1):
                print("enlaceRx,107", eop)
                self.threadPause()
                headpayload = self.buffer[:eop]
                print("HEADPAYLOAD,enlaceRx,linha 109", headpayload)
                self.buffer = self.buffer[eop+4:]
                self.threadResume()
                return headpayload
