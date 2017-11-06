# 1a implementação seguindo dicas:
#Defina os novos campos dos pacotes
self.max = 2048
self.headSTART = 0xFF
self.total = (self.dataLen//self.max) 

if self.dataLen % self.max != 0:
	self.total +=1 #Caso a divisão não de exata, um pacote a mais para os bits que sobraram

self.headStruct = Struct("start" / Int8ub, "size"  / Int16ub, "type" / Int8ub, "total" / Int8ub, "atual"/ Int8ub, "max" / Int8ub,)
self.eopSTART = bytearray([0xFF, 0xFC, 0xF4, 0xF7])

#Faça o envio e recepção desse novo formato de pacote (um único pacote com todo o payload)
#Imprima na tela do receptor (server) as informações extraídas do HEAD
totalPacotes = response[4:5]
atualPacotes = response[5:6]
tamanhoPacotes = response[6:7]
tipo = response[3:4]
print ("Tipo do pacote", tipo)
print ("Quantidade de pacotes", totalPacotes)
print ("Quantidade de bits por pacote", tamanhoPacotes)
print ("Pacote atual", atualPacotes)
#Implemente o reenvio de dados no caso de falhas :
#Reenvio em caso de ACK/NACK ou timeout:
sendData(package)
response = self.getData()
while True:
	if response[3:4] == "ACK":
	    return False
	else if response[3:4] == "NACK":
		sendData(package)
		time.sleep(1)
		response = self.getData()
		return True
	else:    
		sendData(package)
		time.sleep(2)
		response = self.getData()
		return True

#Faça a fragmentação em apenas dois pacotes (esqueça por hora o envio de no máximo 2048 bytes)
def buildPacks(self, data): #talvez seja self.total - 1 porque o i começa do  0
j = 0
Pacotes = []
while j <= 1:
	tamanho = len(self.data)/2
	inicio = j * tamanho
	j ++
	fim = (j*tamanho)-1
	fragmento = self.data[inicio : fim] #Precisa confirmar se aqui sempre tera 2048 bits ou 2047, acredito que terá 2048 pq conta com o 0, mas sei lá, né hahaha
	package = Empacota(fragmento, "data").buildPackage()
	Pacotes.add(package)
return(Pacotes)

#Falta adicionar aqui o identificador de pacotes em cada um no head


"""Verifique se o transmissor (client) está :
Fragmentando os dados corretamente
Aguardando a recepção de um ACK/NACK a cada pacote"""


"""Verifique se o receptor (server) está :
Detectando o número total de pacotes a serem recebidos
Detectando o número atual do pacote
Enviando um ACK/NACK a cada pacote"""
getData()
if response[4:5] == 2: #confirma se quantidade de pacotes é igual a esperada
	print("ok")
	if response[6:7] == len(self.data)/2: #confirma se tamanho de pacotes é igual a esperado
		print ("ok")
		if response[3:4] == b'\x00': #confirma se tipo de pacotes é igual a esperado
			print ("ok")
			if response[5:6] == 0:
				print("ok")
else:
	print ("Quantidade errada de pacotes")
	else:
		print ("Tamanho errado de pacote")
		else:
			print ("Tipo errado de pacote")
			else:
				print ("Identificador de pacote errado")
				