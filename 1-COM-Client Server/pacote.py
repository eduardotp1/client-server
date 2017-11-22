from construct import *
import binascii


class Pacote (object):
    
    # Define o tamanho do HEAD e do EOP
    def __init__(self, data, datatype):
        if datatype == "data":
            self.dataType = 0x00
        elif datatype == "sync":
            self.dataType = 0x10
        elif datatype == "ACK":
            self.dataType = 0x11
        elif datatype == "NACK":
            self.dataType = 0x12
        
        self.data = data
        if self.data == None:
            self.dataLen = 0
            self.data = bytearray([])
        else:
            self.dataLen = len(data)
        
        self.head  = 0xD7
        self.eop = bytearray([0xaf, 0xfc, 0xa4, 0xe7])
        self.headStruct = Struct("start" / Int8ub, "size"  / Int16ub, "type" / Int8ub )
                            
        
    def buildHead(self):
        head = self.headStruct.build(dict(start = self.head,size  = self.dataLen, type = self.dataType))              
        return(head)

    def empacota(self):
        package = self.buildHead()
        package += self.data
        package += self.eop
        print(binascii.hexlify(package))
        return package


# # Desempacota os dados
def desempacota(package):
    size = binascii.hexlify(package[1:3])
    print(package[3])
    print("zoide")
    type_package = package[3]

    if type_package == b'\x00':
        type_package = "data"
    elif type_package == b'\x10':
        type_package = "sync"
    elif type_package == b'\x11':
        type_package = "ACK"
    elif type_package == b'\x12':
        type_package = "NACK"
    payload = package[4:] 
    return (payload,size,type_package)