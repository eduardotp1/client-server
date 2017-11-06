from construct import *
import binascii

def desempacota(package):
    #Desempacota e confere o tipo, retorna payload, tamanho e tipo (se e payload ou comando).
    size = int(binascii.hexlify(package[1:3]), 16) 
    type_package = package[3:4]
    if type_package == b'\x00':
        type_package = "data"
    elif type_package == b'\x10':
        type_package = "sync"
    elif type_package == b'\x11':
        type_package = "ACK"
    elif type_package == b'\x12':
        type_package = "NACK"
    payload=package[4:]
    return (payload, size, type_package)


# Class
class Pacote(object):
    def __init__(self, data, datatype):
        if datatype == "data":
            self.dataType = 0x00
        elif datatype == "sync":
            self.dataType = 0x10
        elif datatype == "ACK":
            self.dataType = 0x11
        elif datatype == "NACK":
            self.dataType = 0x12
        
        self.max_bits = 2048

        self.data = data
        if self.data == None:
            self.dataLen = 0
            self.data = bytearray([])
        else:
            self.dataLen = len(data)


        self.headSTART = 0xFF
        self.number_of_packages = ((len(self.data)//self.max_bits)+1)
        self.headStruct = Struct("start" / Int8ub, "size"  / Int16ub, "type" / Int8ub )
        self.eopSTART = bytearray([0xFF, 0xFC, 0xF4, 0xF7])


    def buildHead(self):
        #Constroi e retorna Head de acordo com as infos inicializadas
        head = self.headStruct.build(dict(start = self.headSTART, size = self.dataLen, type = self.dataType))
        return (head)

    def buildPackage(self):
        package = self.buildHead()
        package += self.data
        package += self.eopSTART
        return package

