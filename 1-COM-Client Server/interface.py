import matplotlib
matplotlib.use('TkAgg')

from Tkinter import *
import Tkinter as tk
import server
import client

class Janela_Principal():

    def __init__(self):

        self.window = tk.Tk()
        self.window.geometry("210x200")
        self.window.configure(background = 'white')
        self.window.resizable(False, False)

        # Geometria da pagina
        self.window.rowconfigure(0, minsize = 30)
        self.window.rowconfigure(1, minsize = 10)
        self.window.rowconfigure(2, minsize = 10)
        self.window.columnconfigure(0, minsize = 35)
        self.window.columnconfigure(1, minsize = 35)



        #Botoes
        self.button_treinar = tk.Button(self.window, text = "Receber", height = 3, width = 30)
        self.button_treinar.grid(row = 1, columnspan = 1)
        self.button_treinar.configure(command = self.receive)

        self.button_Reconhecimento = tk.Button(self.window, text = "Enviar", height = 3, width = 30)
        self.button_Reconhecimento.grid(row   = 2, columnspan = 1)
        self.button_Reconhecimento.configure(command = self.send)

    #Loop do codigo
    def iniciar(self):
        self.window.mainloop()

    #Acoes dos botoes
    def receive(self):
        server.main()

    def send(self):
        client.main()

#Loop do codigo
app = Janela_Principal()
app.iniciar()
