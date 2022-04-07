import csv

#Variáveis Globais
tuplas_de_transicao = []
tuplas_de_estados = []
contador = 1

class Estado:
    valor = ""
    inicial = False
    final = False
    transicoes = []
    def __init__(self,valor:str,transicoes):
        self.valor = valor
        self.transicoes = transicoes
        if(valor.find(">") != -1):
            self.inicial = True
        if(valor.find("*") != -1):
            self.final = True
        for i in self.transicoes:
            i = i.replace('{',"")
            i = i.replace('}',"")

class DFA:
    #Lista de Estados
    estados = []
    #Estado Atual - Começa recebendo o estado inicial
    estado_atual = Estado("",[])
    #Cadeia de caracteres a ser lida
    texto = []
    #Linguagem do DFA
    linguagem = []
    aceitacao = False
    #Índice da Linguagem
    indice = 0

    def split(word):
        return [char for char in word]


    def __init__(self, linguagem, estados, estado_inicial:Estado, texto):
        self.linguagem = linguagem
        self.estados = estados
        self.estado_atual = estado_inicial
        # Conversões necessárias para uma lista de caracteres
        self.texto = texto
        texto_t = str(texto[0])
        texto_t = list(texto_t)
        # Tratando do caso específico se for lido apenas String vazia
        if(texto==""):
            if(self.estado_atual.final):
                self.aceitacao = True
        # Le cada elemento do texto
        for element in texto_t:
            # Verifica se o caracter existe na nossa linguagem e retorne o seu índice
            try:
                self.indice = linguagem.index(element)
            # Caso não exista estado de aceitação é falso
            except:
                self.aceitacao = False
            # Verificar na lista de estados se existe 1 estado que seja igual a transição no índice do nosso estado atual
            for estado in estados:
                # Se exister esse é o nosso novo estado atual
                if(estado.valor == self.estado_atual.transicoes[self.indice]):
                    self.estado_atual = estado
                    break
                else:
                    self.aceitacao = False
        # Após ler toda a String verificar se o nosso estado atual é estado final
        if(self.estado_atual.final):
            self.aceitacao = True

class NFAEstado:
    valor = ""
    inicial = False
    final = False
    transicoes = []
    index = 0
    def __init__(self,valor:str,transicoes):
        self.valor = valor
        self.transicoes = transicoes
        if(valor.find(">") != -1):
            self.inicial = True
        if(valor.find("*") != -1):
            self.final = True
        for i in range(len(self.transicoes)):
            self.transicoes[self.index] = self.transicoes[self.index].replace('{',"")
            self.transicoes[self.index] = self.transicoes[self.index].replace('}',"")
            self.index += 1

class NFA:
    # Lista de Estados
    estados = []
    # Estado Inicial
    estado_inicial = 0
    # Linguagem do NFA
    linguagem = []

    def __init__(self, linguagem, estados):
        self.linguagem = linguagem
        self.estados = estados

# Função Principal do simulador de Autômato Finito Determinístico
def main():
    index = 0
    # Estado inicial do meu DFA
    estado_inicial = 0
    # Lista de Estados
    estados = []
    # Leitura de arquivo .tsv dos estados e linguagem do DFA
    with open("entrada/entradaDFA.tsv") as file:
        tsv_file = csv.reader(file, delimiter="\t")
        
        for line in tsv_file:
            if(index==0):
                linguagem = line
                linguagem.remove("")
                
            else:
                transicoes = []
                if(index == 1):
                    # Recebe o valor do estado inicial
                    estado_inicial = line[0]
                    # Separa suas transições
                    transicoes = line
                    transicoes.pop(0)
                    # Cria um objeto estado
                    aux = Estado(estado_inicial, transicoes)
                    # O adiciona a lista de estados do nosso DFA
                    estados.append(aux)
                    # Define como o nosso estado inicial
                    estado_inicial = aux
                else:
                    # Separa o valor do estado
                    aux = line[0]
                    line.pop(0)
                    # Separa suas transições e cria um objeto estado
                    aux2 = Estado(aux, line)
                    # O adiciona a lista de estados do nosso DFA
                    estados.append(aux2)
            index = index + 1

    # Leitura de arquivo .tsv das Strings
    with open("entrada/stringsDFA.tsv") as file:
        tsv_file = csv.reader(file, delimiter="\t")
        for line in tsv_file: 
            dfa = DFA(linguagem,estados,estado_inicial,line)
            # Escrita do arquivo .tsv de Saída           
            with open("saida/saidaDFA.tsv",'a') as f2:
                f2.write(str(dfa.aceitacao)+"\n")

#Função Principal do algoritmo de covnersão de Autômato Finito Não-Determinístico
def main2():
    index = 0
    # Estado inicial do meu NFA
    estado_inicial = 0
    # Lista de Estados
    estados = []
    # Lista de Tuplas de Transição
    tuplas_de_transicao = []
    # Lista de Tuplas de Estados
    tuplas_de_estados = []
    #Contador auxiliar para os novos estados encontrados
    contador = 0
    # Lista de Estados ainda não visitados
    list_nmarcada = []
    # Lista de Estados visitados
    list_marcada = []

    # Leitura de arquivo .tsv dos estados e linguagem do NFA
    with open("entrada/entradaNFA.tsv") as file:
        tsv_file = csv.reader(file, delimiter="\t")
        
        for line in tsv_file:
            if(index==0):
                linguagem = line
                linguagem.remove("")
                
            else:
                transicoes = []
                if(index == 1):
                    # Recebe o valor do estado inicial
                    estado_inicial = line[0]
                    # Separa suas transições
                    transicoes = line
                    transicoes.pop(0)
                    # Cria um objeto estado
                    aux = NFAEstado(estado_inicial, transicoes)
                    # O adiciona a lista de estados do nosso NFA
                    estados.append(aux)
                    # Define como o nosso estado inicial
                    estado_inicial = aux
                    
                else:
                    # Separa o valor do estado
                    aux = line[0]
                    line.pop(0)
                    # Separa suas transições e cria um objeto estado
                    aux2 = NFAEstado(aux, line)
                    # O adiciona a lista de estados do nosso NFA
                    estados.append(aux2)
                    
            index += 1
    
    
    #Inicialmente ε-closure(q0) é o único estado em Dstates, e não está marcado;
    list_nmarcada.append(estado_inicial.valor)
    while(len(list_nmarcada) != 0):
        #Indice da Linguagem
        index = 0
        #Se o nosso estado já foi marcado
        isChecked = False
        #Marca T
        ##A = {>q0}
        #B = {>q0,q1}
        #testa o primeiro e adiciona e outra lista a transição resultante
        #testa até o final e adiciona cada transição. se essa lista não era existente ela é um novo estado.
        #	{}
        #C = {>q0,q1,q2,*q3}
        #MARCANDO Q0
        print("Lista não marcada") 
        print(list_nmarcada)
        print("")
        
        t = list_nmarcada.pop(0)
        t = t.split(",")
        if not t in list_marcada:
            list_marcada.append(t)
        print("Valor de T")
        print(t)
        print("Tamanho do T")        
        print(len(t))
        print("")
        if(len(t)==1):
            tuplas_de_estados.append(tuple((contador,t[0])))
            contador += 1
        
        if(len(t)==1):
            print("TESTE 1")
            for x in estados:
                if(x.valor in t):
                    print("Valor de X")
                    print(x.valor)
                    for y in linguagem:
                        print("Valor de Y")
                        print(y)
                        for z in list_marcada:
                            print("Valor de Z")
                            print(z)
                            if(x.transicoes[index] == z):
                                
                                tuplas_de_transicao.append(tuple((t[0],y,z)))
                                print(x.transicoes[index]+" ja foi marcado")
                                isChecked = True
                        if(isChecked == False):
                        #Adicionar a lista como não marcada
                        #['>q0', 'q1'] -> A
                        # MAS TEM Q SER ENTENDIDO PELO PROGRAMA Q TODA VEZ Q ['>q0', 'q1'] -> A
                            print(x.transicoes[index]+" ainda n foi marcado")
                            tuplas_de_estados.append(tuple((contador,x.transicoes[index])))
                            contador += 1
                            tuplas_de_transicao.append(tuple((t[0],y,x.transicoes[index])))
                            list_nmarcada.append(x.transicoes[index])
                        index += 1
            
            print("Lista Marcada")
            print(list_marcada)                        
            print("Tupla de Estados")
            print(tuplas_de_estados)
            print("")
        else:
            print("TESTE 2")
            print("Valor de T")
            print(t)
            w = []
            tupla_t = []
            if(len(t)!=1):
                for w in t:
                    index = 0
                    print("Valor de W")
                    print(w)
                    for x in estados:
                        if(x.valor == w):
                            for y in linguagem:
                                print("Valor de Y")
                                print(y)
                                print("Valor da Transição")
                                print(x.transicoes[index])
                                tupla_t.append(tuple((y,x.transicoes[index])))
                                index +=1
                print("Tupla Temporária")
                print(tupla_t)
            isChecked = False
            print("Lista Marcada")
            print(list_marcada)
            print("Tuplas de Estados")
            print(tuplas_de_estados)
            print("Tuplas de Transicao")
            print(tuplas_de_transicao)
            tupla_t2 = []
            print("Valor de T- Teste A")
            print(t)
            print("Tamanho do T")
            print(len(t))
            while(len(t)!=len(tupla_t2)):
                print("Tupla T")
                print(tupla_t)
                for x in tupla_t:
                    print("Valor de X")
                    print(x)
                    index = 0
                    for y in tupla_t:
                        print("Valor de Y")
                        print(y)
                        if(x != y):
                            if(x[0]==y[0]):
                                s = x[1]+","+y[1]
                                print("Valor de S")
                                print(s)
                                s2 = y[1]+","+x[1]
                                if s2 in tupla_t2:
                                    pass
                                else:
                                    for z in tupla_t2:
                                        #Tentando eliminar uniões desnecessárias fazendo 1 acontecer de cada vez
                                        print("Valor de Z")
                                        print(z)
                                    tupla_t2.append(s)
                                    print("Valor de Tupla T2")
                                    print(tupla_t2)
                                    break
                        index += 1
            print("Tupla Temporária 2")
            print(tupla_t2)
            print("Lista Marcada - Antes do Loop")
            print(list_marcada)
            index = 0
            for x in tupla_t2:
                for z in list_marcada:
                    print("Comparação X com Z")
                    print(x)
                    print(z)
                    if(x == z):
                        #Adicionar tupla de transicao
                        tuplas_de_transicao.append(tuple((t,linguagem[index],z)))
                        print(x+" ja foi marcado")
                        isChecked = True
                    if(isChecked == False):
                        print(x+" ainda n foi marcado")
                        print("Valor de x")
                        print(x)
                        print("Tipo do X")
                        print(type(x))
                        print("Lista não Marcada - Antiga")
                        print(list_marcada)
                        list_nmarcada.append(x)
                        print("Lista não Marcada - Nova")
                        print(list_marcada)
                        tuplas_de_estados.append(tuple((contador,x)))
                        contador += 1
                        tuplas_de_transicao.append(tuple((t,linguagem[index],x)))
                index += 1



if __name__ == "__main__":
    
    print("Digite 1 caso deseje iniciar o simulador de Autômato Finito Determinístico")
    print("Digite 2 caso deseje iniciar o algoritmo de conversão de Autômato Finito Não-Determinístico")
    
    input = int(input())
    if(input==1):
        main()
    if(input==2):
        main2()
    else:
        print("Valor inválido -- Finalizando Programa")
