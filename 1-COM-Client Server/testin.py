#Reformulação do head do pacote (em empacota):
#Inicializar quantidade de pacotes necessário
self.max = 2048
self.headSTART = 0xFF
self.total = ((self.dataLen//self.max)+1) 

self.headStruct = Struct("start" / Int8ub, "size"  / Int16ub, "type" / Int8ub, "total" / Int8ub, "atual"/ Int8ub, "max" / Int8ub,)
self.eopSTART = bytearray([0xFF, 0xFC, 0xF4, 0xF7])

#Criando fragmentos de payloads para serem empacotados, sempre com 2048 bits no máx.
def buildPacks(self, data): #talvez seja self.total - 1 porque o i começa do  0
j = 0
Pacotes = []
while j <= self.total:
	inicio = j*self.max
	j ++
	fim = (j*self.max)-1
	fragmento = self.data[inicio : fim] #Precisa confirmar se aqui sempre tera 2048 bits ou 2047, acredito que terá 2048 pq conta com o 0, mas sei lá, né hahaha
	package = Empacota(fragmento, "data").buildPackage()
	Pacotes.add(package)
return (Pacotes)

#Falta adicionar aqui o identificador de pacotes em cada um no head

	#enviar pacotes
	def sendPacks(self, Pacotes):
		i = 0
		while i <= self.total: #talvez seja self.total - 1 porque o i começa do  0
			atual = Pacotes[i]
			self.sendAtual(atual)
			i ++

	#implementação do nosso desempacotar, pois aqui apenas vai adicionando o pacote x ao pacote x+1...., na ordem, mas não faz tratamento de identificar se é data, ack, etc
	#Dado que o fragmento já vira sem eop, por conta da getHeadPayLoad
	#Dado que o total de pacotes é na posicao [4:5] e do pacote atual é na posicao [5:6]
	def desempacotaFragmento():
		headpayload = getHeadPayLoad()
		total = headpayload[4:5] #pegando valor total
		contador = 0
		while contador <= total:
			headpayload = getHeadPayLoad() #encontra pacote no buffer e entrega sem eop
			atual = headpayload[5:6]  #pega o identificador do fragmento atual
				if atual == contador:#confirma pelo identificador se esse fragmento de payload é realmente o próximo fragmento que precisa ser adicionado
				pay = headpayload.getData() #tira o head
				payload += pay 
				contador ++
			else:
				pass #caso não for o fragmento que queremos, refaz o loop pegando outro fragmento



	#função sendAtual
	