from tkinter import *   
from random import randint
import threading as th
import pygame as pg
import time


class InterFaceGrafica():
    formato = 0 #o formato da matriz ex: 3x3, 4x4, 5x5 e etc
    Criado_matriz = False #para nao fica criando matriz toda hora
    Movimentos = 0 #ondem sera guardados as contagem de movimentos das peças

    def __init__(self):
        self.MainGui()
        

    def Tocar_Som(self , file, temp=None):
        #carregando o arquivo MP3
        '''
        Explicando esse 'fr' basicamente, o 'f' é o formata e o 'r' é a famosa string bruta 
        '''
        pg.mixer.music.load(file)
        #Play no audio
        pg.mixer.music.play()
        #tempo
        if temp != None:
            time.sleep(temp)


    def MainGui(self): #janela Principal
        def Play():
            #destruindo janela atual
            Botao_Jogar.destroy()

            #partido para outra janela
            self.EsolheDificuldade_GUI()

        #pegando todos os modulos do modulo Mixer do pygame, para reproduzir musicas
        pg.mixer.init()

        self.janela = Tk()
        #imagens
        image_play = PhotoImage(file=r'Puzzle\sistema\imagem\jogar.png') #<a href="https://br.freepik.com/search">Ícone de riajulislam</a>
        self.image_relogio = PhotoImage(file=r'Puzzle\sistema\imagem\conometro.png')
        #imagem do botao jogar novemente
        self.image_Loop = PhotoImage(file=r'Puzzle\sistema\imagem\JogarNovamente.png')#<a href="https://br.freepik.com/search">Ícone de Pixel perfect</a>
        #imsge da seta para direita
        self.image_setaRight = PhotoImage(file=r'Puzzle\sistema\imagem\Proximo.png')#<a href="https://br.freepik.com/search#uuid=953e0ab6-e724-454a-8963-b5341eb42461">Ícone de Fathema Khanom</a>

        self.janela.geometry('700x500')
        self.janela.config(bg='#F28705')
        self.janela.iconphoto = image_play
        self.janela.resizable(width=False , height=False)

        Botao_Jogar = Button(self.janela , image = image_play , relief='flat' , bg='#F28705' , command=Play)
        Botao_Jogar.pack(expand=True)
        
        self.janela.mainloop()

    
    def EsolheDificuldade_GUI(self):# ondem o usuario vai escolhar o formato, ou seja o dificuldade

        def Jogar():
            #Destruindo janela atual
            frame_destaque.destroy()
            frame_titulo.destroy()
            
            titulo.destroy()

            botao_3x.destroy()
            botao_4x.destroy()
            botao_5x.destroy()
            self.janela.update()

            self.jogandoGui()
            self.janela.update()
            


        def x5():
            self.formato = 5 # o formato da matriz 
            Jogar()


        def x4():
            self.formato = 4 # o formato da matriz
            Jogar()


        def x3():
            self.formato = 3 # o formato da matriz
            Jogar()

        #meio: x = 210
        '''
        Dificuldade: 3x3 , 4x4 e 5x5
        '''
        #frames
        #frames que vai destaca as dificuldade
        frame_destaque = Frame(self.janela , width=800 , height=300 , bg='#ad5f00')
        frame_destaque.place(x=0 , y=100)

        #frame titulo
        frame_titulo = Frame(self.janela , width=800  , height=100 ,bg='#F2BE22')
        frame_titulo.place(x=0 , y=0)

        #titulo
        titulotext = 'Escolha o Formato'
        titulo = Label(self.janela , width = len(titulotext)+2 , font='arial 40 bold' ,text=titulotext ,bg='#F2BE22')
        titulo.pack(pady=15)
        
        fonte_botao = 'arial 25 bold' #fonte dos botoes

        #Formato 3x3
        botao_3x = Button(self.janela, text='3x3' , width=14 , font=fonte_botao , relief='flat' ,bg='#35AC55' , command=x3)
        botao_3x.place(x=210 , y=130)

        #Formato 4x4
        botao_4x = Button(self.janela , width=14 , height=1 , font=fonte_botao , relief='flat' ,bg='#FDBE02' , text='4x4' , command=x4)
        botao_4x.place(x=210 , y=220)

        #Formato 5x5
        botao_5x = Button(self.janela , width=14 ,height=1 ,font=fonte_botao ,bg='#EB4436' ,relief='flat' , text='5x5' , command=x5)
        botao_5x.place(x=210 , y=310)


    def jogandoGui(self):
        
        #frame do tempo
        self.frame_tempo = Frame(self.janela , width=800 , height=100 ,bg='#1473E6')
        self.frame_tempo.place(y=0 , x=0)

        #relogio
        self.relogio_image = Label(self.janela , image=self.image_relogio , relief='flat' , bg='#1473E6')
        self.relogio_image.place(x=10 , y=10)

        #Contagem de movimentos
        self.label_MoviCont = Label(self.janela , width=len('Move:')+4 , text='Move:' , relief='flat' , bg='#1473E6' ,justify=CENTER , font='arial 35 bold')
        self.label_MoviCont.place(x=370 , y= 25)

        #label temporizador
        self.label_tempo = Label(self.janela , width=len('00:00') , font='Time 50 bold' ,text='00:00', bg='#1473E6' , fg='white' , relief='flat' , justify='left')
        self.label_tempo.place(x=100 , y=10)

        self.frame = Frame(self.janela , width=600 , height=800 , bg='#c27416')
        self.frame.place(x=50 , y=100)

        thread_contagem = th.Thread(target=self.Contagem)
        thread_contagem.start()

        #Declarando ondem vai fica o resultado
        if self.formato == 3:
            #eixo y do label
            self.EixoYLabel = 190
            #eixo y do frame
            self.EixoYFrame = 160
        elif self.formato == 4:
            #eixo y label
            self.EixoYLabel = 230
            #y do frame
            self.EixoYFrame = 200
        
        elif self.formato == 5:
            #eixo y do label
            self.EixoYLabel = 280
            #eixo y do frame
            self.EixoYFrame = 250
            

        self.Create_Table(formato=self.formato)
        self.Puzzle()


    def Estatisticas_EndGame(self , resultado , ContTempo=False): #a interface grafica ondem o usuario vai ver as informações sobre a jogadas
        def Destruir_GuiPlay():
            self.label_MoviCont.destroy()
            self.frame_tempo.destroy()    
            self.relogio_image.destroy()
            self.label_tempo.destroy()
            self.frame.destroy()
            self.Frame_res.destroy()
            self.Label_res.destroy()
            
            #Destruindo a Matriz
            for v in self.blocos.values():
                v.destroy()
            #atualizando janela
            self.janela.update()


        def Dificuldade(): #formata a dificuldade para exbição
            if self.formato == 3:
                return '3x3 Fácil'
            elif self.formato == 4:
                return '4x4 Medio'
            elif self.formato == 5:     
                return '5x5 Difícil'
            

        def Formata_Tempo(min ,seg): #Formatando tempo
            if min > 9 and seg > 9:
                return f'{min}:{seg}'
            elif min <= 9 and seg <= 9:
                return f'0{min}:0{seg}'
            elif min > 9 and seg <= 9:
                return f'{min}:0{seg}'
            elif min <= 9 and seg > 9:
                return f'0{min}:{seg}'
            

        def Destruir_Janela():#Destruir essa janela
            #destruindo esta janela
            #botoes
            self.JogarNovamente.destroy()
            self.VoltaMenu.destroy()
            #frames
            self.frame_DestaqueRes.destroy()
            self.frame_InfoEnd.destroy()
            #labels
            self.label_NameInfo.destroy()
            self.label_ResEnd.destroy()
            self.Pecas_Movi.destroy()
            self.TempoGasto.destroy()
            self.Dificuldade_Jogada.destroy()


        def Joga_Novamente():
            #destruindo janela atual
            Destruir_Janela()
            #joga Novamente
            self.Criado_matriz = False # para criar uma nova matriz
            self.jogandoGui()


        def Volta_Menu():
            #destruindo janela atual
            Destruir_Janela()
            #Voltando pro menu da dificuldade
            self.Criado_matriz = False # para criar uma nova matriz
            self.EsolheDificuldade_GUI()

        
        Destruir_GuiPlay() #destruindo janela anterior.
        if resultado == 'Vitoria':
            ResFinal = 'Vitoria'
            ContTempo=True
        else:
            ResFinal = 'Derrota'

        if ContTempo:
            tempo = Formata_Tempo(min=self.tempo_Gasto//60 , seg=self.tempo_Gasto%60)
        else:
            tempo = 'Esgostado'

        self.Movimentos = 0 #resetando a contagem dos movimentos
        #config janela
        self.janela.geometry('700x540')

        #Frame que dara destaque ao label que exbirar o resultado
        self.frame_DestaqueRes = Frame(self.janela , width=800 , height=130 ,bg='#5C0201')
        self.frame_DestaqueRes.pack()

        #Label que exbirar o resultado
        self.label_ResEnd = Label(self.janela , width=7 ,text=ResFinal ,font='arial 70 bold' , bg='#5C0201' ,fg='white' , relief='flat' , justify=CENTER)
        self.label_ResEnd.place(x=150 , y=10)

        #frame ondem ficara as estatisticas
        self.frame_InfoEnd = Frame(self.janela , width=550 , height=430 , bg='#e6b633')
        self.frame_InfoEnd.pack()

        #Label com nome 'Estatistiicas'
        self.label_NameInfo = Label(self.janela , width=len('estatisticas') ,text='Estatisticas', font='arial 40 bold' ,relief='flat' , fg='white' , bg='#e6b633',justify=CENTER)
        self.label_NameInfo.place(x=150 , y=140)

        #Estatisticas
        #Peças movidas
        self.Pecas_Movi = Label(self.janela , width=len('Blocos Movidos: 000') ,text=f'Blocos Movidos: {self.Movimentos}', font='arial 30 bold' , relief='flat' , justify='right' , anchor='nw', bg='#e6b633' )
        self.Pecas_Movi.place(x=130, y=240)

        #Tempo Gasto
        self.TempoGasto = Label(self.janela , width=len('Tempo Gasto: 00:00')+2 , text=f'Tempo Gasto: {tempo}' , font='arial 30 bold' , relief='flat', justify='right' , anchor='nw', bg='#e6b633' )
        self.TempoGasto.place(x=130 , y=300)
        
        #Dificuldade
        dificuldade = Dificuldade()
        self.Dificuldade_Jogada = Label(self.janela , width=20 , text=f'Diculdade: {dificuldade}' ,font='arial 30 bold' , relief='flat' ,anchor='nw' , justify='right' , bg='#e6b633')
        self.Dificuldade_Jogada.place(x=130 , y=360)

        #Jogar Novamente
        self.JogarNovamente = Button(self.janela , image=self.image_Loop , bg='#e6b633' ,relief='flat' ,command=Joga_Novamente)
        self.JogarNovamente.place(x=160 , y=420)

        #Volta pro Menu de escolha
        self.VoltaMenu = Button(self.janela , image=self.image_setaRight ,relief='flat' ,bg='#e6b633' , command=Volta_Menu)
        self.VoltaMenu.place(x=440 , y=420)


    def Contagem(self):
        def Desabilitar_Pecas():
            for pecas in self.blocos.values():
                pecas['state'] = 'disabled'

        def Tempo_Esgotando():#vai fica mudando a cor do time
            thread_SomTicTac = th.Thread(target=lambda: self.Tocar_Som(file=r'sistema\audios\tic-tac.mp3' ,temp=30))
            thread_SomTicTac.start() #tocando o efeito sonoro de 30s pra termina. em um thread
            try:    
                Vermelho = True # a variavel se o fg do label_tempo vai fica vermelho sinalizando que o tempo esta esgotando
                for cont in range(60):
                    if Vermelho: #se vermelho for True(verdadeiro)
                        self.label_tempo['fg'] = '#C90202' #fg do label sera vermalho
                        Vermelho=False # Vermelho passara se False(Falso)
                    else: #senao 
                        self.label_tempo['fg'] = 'white' #label voltaram se da cor branco
                        Vermelho=True #Agora vermelho passara se True(Verdadeiro)
                    time.sleep(0.5) #meio segundo
                    self.label_tempo.update() #Atualizando label
            except Exception:
                pass

        self.parada_win = False #se for true pq o usuario ganhou
        resultado = None #ondem vou guardar o resultado
        self.tempo_Gasto = 0 #vai guarda o tempo que o usuario demorou ao cumprir o puzzle

        if self.formato == 3: #se o formato escolhido for 3 sera 180s de tempo par ao usuario. tenta ganhar o puzzle
            tempo = 180  
        elif self.formato == 4: # se for o 4 sera 240s
            tempo = 240
        elif self.formato == 5: # se for o 5 sera 300s
            tempo = 300

        while True:
            if tempo == 30 :
                thread_atencao = th.Thread(target=Tempo_Esgotando)
                thread_atencao.start()

            if self.parada_win:
                Desabilitar_Pecas() #desabilitar peças do puzzle
                thread_SomFim = th.Thread(target=lambda: self.Tocar_Som(file=r'sistema\audios\fimRelogio.mp3'))
                thread_SomFim.start() #acabou, efeito sonoro de relogio esgotado
                resultado='Vitoria' # vai guardar o resultado Vitoria
                for v in self.blocos.values():
                    v['state'] = 'disabled'
                time.sleep(2)
                break
                
            tempo-=1
            self.tempo_Gasto+=1
            if tempo == 0:
                Desabilitar_Pecas() #desabilitando todas as peças
                thread_SomFim = th.Thread(target=lambda: self.Tocar_Som(file=r'sistema\audios\fimRelogio.mp3'))
                thread_SomFim.start() #acabou, efeito sonoro de relogio esgotado
                resultado = 'Derrota' # vai guardar a str derrota.
                self.label_tempo['text'] = '00:00'   
                """
                Mostrar se o usuario ganhou ou nao
                Aqui mostrar que o usuario perdeu, os sao separado porque:
                Ambos serao disparado por diferente codicoes, aqui dispara quando o time for 0, na caso o usuario perdeu
                ja do Wins, entao na linha 386-390
                """            
                self.Frame_res = Frame(self.janela , width=800 , height=180 , bg='#5C0201')
                self.Frame_res.place(x=0, y=self.EixoYFrame)

                self.Label_res = Label(self.janela , width=11 , height=1 ,font='arial 70 bold' , relief='flat' ,bg='#5C0201' ,fg='white' , text='Você Perdeu')
                self.Label_res.place(x=30 , y=self.EixoYLabel)
                time.sleep(2)
                break

            minutos = tempo // 60
            segundos = tempo % 60

            if minutos > 9 and segundos > 9:
                self.label_tempo['text'] = f'{minutos}:{segundos}'
            elif minutos <= 9 and segundos <= 9:
                self.label_tempo['text'] = f'0{minutos}:0{segundos}'
            elif minutos <= 9 and segundos > 9:
                self.label_tempo['text'] = f'0{minutos}:{segundos}'
            elif minutos > 9 and segundos <= 9:
                self.label_tempo['text'] = f'{minutos}:0{segundos}'
            
            time.sleep(1)
            self.label_tempo.update()

        self.Estatisticas_EndGame(resultado=resultado)


    def Create_Table(self , formato):#ondem ira criar as tabela do puzzle
        def Matriz():
            matriz=[] #ondem vai fica os numeros sorteados
            numeros = list(range(1,(formato*formato))) #criando uma lista dos numeros
            repetido = False #parar verificar os numeros se é repetido ou nao
            while True: #loop
                if len(numeros) == 0: #se numeros for == 0> porque eu gerei a lista com -1 de acordo com range(), entao o ultimo sera o espaço vazio
                    matriz.append(' ') #add o espaço vazio no final
                    return matriz #retornando a matriz
                
                sorteio = randint(0 , len(numeros)-1)  #sorteado o indice

                if len(matriz) == 0: #se a matriz estive com 0 valores dentro dele. Add o primeiro valor
                    matriz.append(numeros[sorteio]) #add o valor sorteado de acordo com indice
                    del numeros[sorteio] #deletando o valor sorteado para nao se sorteado novamente
                else: 
                    for v in matriz: # um for para verificar cada valor.
                        if v == sorteio: #se for igual
                            repitido = True # repetido sim
                            break #quebrar o loop
                    if not repetido: #se nao estive repetido
                        matriz.append(numeros[sorteio]) # add o valor sorteado
                        del numeros[sorteio] #deleta o valor soteado pra nao ter repetição
                    elif repitido: #se estiver repetido
                        repetido = False

        if not self.Criado_matriz:
            self.Criado_matriz = True #para garantir somente uma matriz sorteada
            self.matriz = Matriz()

        self.blocos = {} #ondem vou guardar os blocos
        #'700x500'
        if not self.parada_win:
            if formato == 3:
                #x=+100 , y=+90
                #configuração
                x = 125 # ondem começar a matriz 
                y = 140 # ondem fica o eixo Y da matriz

                coluna2 = coluna3 = False #isso aqui é para garantir que o X seja subtraido uma vez.
                for c in range(formato*formato):
                    valor = self.matriz[c] #pegando o valor de acordo com indices

                    if c in (3, 4, 5) and not coluna2: # se c estive com indice que entao na coluna 2
                        coluna2 = True # pra garantir que essa codição nao seja atendida
                        x-=270 # começo do eixo X
                        y+=90 # botando a coluna pra baixo Eixo Y
                    
                    elif c in (6,7,8) and not coluna3: # se c estive com indice que entao na coluna 3    
                        coluna3 = True # pra garantir que essa codição nao seja atendida mais.
                        x-=270 # voltando pro começo do eixo X
                        y+=90 #botando a coluna pra baixo

                    x+=90
                    self.bloco = Button(self.janela ,width=10, height=5 , relief="flat" , text=valor ,state="disabled" ,font='bold', command=lambda v=valor: self.Mudar_Posicoes(v))
                    self.bloco.place(x=x , y=y)
                    self.blocos[f'bloco{c}'] = self.bloco

            elif formato == 4:
                #configuração
                self.janela.geometry('700x550')
                x = 80
                y = 140

                coluna2 = coluna3= coluna4 = False
                for c in range(formato*formato):
                    valor = self.matriz[c]

                    if c in (4,5,6,7) and not coluna2:
                        x-=360
                        y+=90
                        coluna2 = True

                    elif c in (8,9,10,11) and not coluna3:
                        x-=360
                        y+=90
                        coluna3 = True

                    elif c in (12,13,14,15) and not coluna4:
                        x-=360
                        y+=90
                        coluna4 = True

                    x+=90
                    self.bloco = Button(self.janela , width=10 , height=5 , font='bold' , relief='flat', text=valor , command=lambda v=valor: self.Mudar_Posicoes(v) ,state='disabled')
                    self.bloco.place(x=x , y=y)
                    self.blocos[f'bloco{c}'] = self.bloco

            elif formato == 5:
                #x=90 y=+90
                #-450
                #configuração
                self.janela.geometry('700x630')
                x = 30 
                y = 130

                coluna2 = coluna3 = coluna4 = coluna5 = False
                for c in range(formato*formato):
                    valor = self.matriz[c]

                    if c in (5,6,7,8,9) and not coluna2:
                        x-=450
                        y+=90
                        coluna2 = True

                    elif c in (10,11,12,13,14) and not coluna3:
                        x-=450
                        y+=90
                        coluna3 = True

                    elif c in (15,16,17,18,19) and not coluna4:
                        x-=450
                        y+=90
                        coluna4 = True

                    elif c in (20,22,23,24,25) and not coluna5:
                        x-=450
                        y+=90
                        coluna5 = True

                    x+=90
                    self.bloco = Button(self.janela , width=10 , height=5 , font='bold', text=valor , state='disabled' , command=lambda v=valor: self.Mudar_Posicoes(v))
                    self.bloco.place(x=x , y=y)
                    self.blocos[f'bloco{c}'] = self.bloco


    def Mudar_Posicoes(self,inputvalor): #o responsavel que irar mudar a matriz, e vair trabalhar diretamente com o metedo Pezzle
        def Verificação_Vitoria(matriz): #funcao pra verificar se o usuario ganhou ou nao.
            #podemos o usar o a sintax ==.
            Corret_Ondem = list(range(1 ,self.formato*self.formato))
            Corret_Ondem.append(' ')
            for index, valor in enumerate(matriz):
                if valor != Corret_Ondem[index]:
                    break
                if index+1 == len(Corret_Ondem):
                    return True
            return False


        self.Movimentos +=1 #Uma peça movida
        self.label_MoviCont['text'] = f'Move: {self.Movimentos}'

        valor_info = None
        vazio_info = None

        for v in self.matriz.values():#pegando as informações do valor clicado
            if v['valor'] == inputvalor:
                valor_info = v #pegando as seguintes informações 'valor' e indice
                break

        for v in self.matriz.values(): #pegando as informações do bloco vazio
            if v['valor'] == ' ':
                vazio_info = v #pegando as seguintes informações 'valor' e 'indice'
                break
        matrizTemp = []

        for v in self.matriz.values(): # vou contruir uma nova matriz, so qr ja formatado, ja feita a troca, vou retorna um a lista pq so irei faze-lo como dicionario para fazer a conta la no metedo 'Puzzle';
            #condicao para fazer a troca
            if v['valor'] == valor_info['valor']: # se o valor for = ao bloco vazio
                matrizTemp.append(vazio_info['valor']) #add o valor que o usuario selecionou
            elif v['valor'] == vazio_info['valor']: # se o valor = ao bloco que o usuario acarbou de selecionar
                matrizTemp.append(valor_info['valor']) #add o espaço vazio
            else: #senao apenas add o valor na matriz tempo
                matrizTemp.append(v['valor'])

        self.matriz = matrizTemp
        if Verificação_Vitoria(self.matriz): #verificando se o usuario ganhou ou nao
            for v in  self.blocos.values():
                    v['state'] = 'disabled'
            #Destruindo a Matriz
            for v in self.blocos.values():
                v.destroy()
            self.Create_Table(self.formato) #criando uma nova tabela ja atualizada
            '''
            Mostrar o Resultado se ganhou ou nao
            Aqui é separado porque ambos sao disparado por diferente condicoes:
            linha da funcoes ondem sera disparada o label com game over
            181-186
            '''

            self.Frame_res = Frame(self.janela , width=800 , height=180 , bg='#5C0201')
            self.Frame_res.place(x=0, y=self.EixoYFrame)

            self.Label_res = Label(self.janela , width=11 , height=1 ,font='arial 70 bold' , relief='flat' ,bg='#5C0201' ,fg='white' , text='Você Ganhou')
            self.Label_res.place(x=30 , y=self.EixoYLabel)
            self.parada_win = True #Usuario ganhou

        else:
            #Destruindo a Matriz
            for pecas in self.blocos.values():
                pecas.destroy()
            self.Create_Table(self.formato) #criando uma nova tabela ja atualizada
            self.Puzzle() #Verificar Posicoes, a parte logica.
            self.janela.update() #Atualizar janela


    def Puzzle(self): #a parte logica do game
        def FormataLista(lista):#passando lista pra dicionario
            #passando a lista 'self.matriz' para um dicionario
            matriz = {}# o dicionario
            i = 1
            j = 0
            PassaLinha = 0 #sera o responavel por mudar o valor de do 'i' ou seja a linha da matriz
            for ind, v in enumerate(lista):#sendo direto essa formatação, vai criar um indice de uma matriz e vai criar uma lista de dois valores, com indice do valor, ex: A12 = valor=x , indice=3, a localização do valor. isso tudo a parti do espaço vazio.
                j+=1 #1+ coluna
                matriz[f'{i}{j}'] = {'valor': v , #o valor do indice.
                                    'index': ind} #o indice. fodase
                PassaLinha+=1
                if PassaLinha == self.formato:
                    i+=1 #1+ linha
                    PassaLinha = 0
                    j = 0              
            return matriz
        

        def cima(col , lin):
            i = lin
            j = col
            if (i-1) > 0:
                i-=1
                for c , v in self.matriz.items():
                    if c == f'{i}{j}':
                        return v
            else:
                return None
        

        def abaixo(col , lin):
            i = lin
            j = col
            if (i+1) <= self.formato:
                i+=1
                for c , v in self.matriz.items():
                    if c == f'{i}{j}':
                        return v
            else:
                return None
            

        def esquerda(col , lin):
            i = lin
            j = col
            if (j-1) > 0:
                j-=1 
                for c , v in self.matriz.items():
                    if c == f'{i}{j}':
                        return v
            else:
                return None 


        def direita(col , lin):
            i = lin
            j = col
            if (j+1) <= self.formato:
                j+=1
                for c , v in self.matriz.items():
                    if c == f'{i}{j}':
                        return v
            else:
                return None


        def Procurar_Vazio(matriz):
            for c , v in matriz.items():
                if v['valor'] == ' ':
                    i = int(c[0])
                    j = int(c[1])
                    return [i ,j]
                

        self.matriz = FormataLista(lista=self.matriz) #guardando o retorno do metedo(funcao) na variavel 'matriz'

        posicao = Procurar_Vazio(matriz=self.matriz)                        
        #procurar o vazio
        i = posicao[0] #o i
        j = posicao[1] #i j
        #as direções que sera liberadas pra clicas
        Direita = direita(lin=i , col=j)
        Esquerda = esquerda(lin=i , col=j)
        Cima = cima(lin=i , col=j)
        Abaixo = abaixo(lin=i , col=j)
        
        try:    
            if Direita != None:
                blocotemp = self.blocos[f'bloco{Direita['index']}']
                blocotemp['state'] = 'normal'
            if Esquerda != None:
                blocotemp = self.blocos[f'bloco{Esquerda['index']}']
                blocotemp['state'] = 'normal'
            if Cima != None:
                blocotemp = self.blocos[f'bloco{Cima['index']}']
                blocotemp['state'] = 'normal'
            if Abaixo != None:
                print
                blocotemp = self.blocos[f'bloco{Abaixo['index']}']
                blocotemp['state'] = 'normal'
        except Exception.__class__ as error:
            print(f'error: {error}')
            
        self.janela.update()


if __name__ == '__main__':
    InterFaceGrafica()