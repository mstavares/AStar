class no:
    def __init__(self, posicao, custo = 0):
        self.posicao = posicao
        self.custo = custo

    def get_posicao(self):
        return self.posicao

    def get_custo(self):
        return self.custo

    def atualiza_custo(self, goal):
        self.custo += 1 + calcula_heuristica(self, goal)
        print self.posicao
        print self.custo

def devolve_a_posicao(lista):
    return [i for i, x in enumerate(lista) if x == devolve_o_melhor_no(lista)][0]

def insere_objetos_na_matriz(matriz, posicao, objeto):
    linha = posicao[0]
    coluna = posicao[1]
    matriz[linha][coluna] = objeto

def devolve_o_melhor_no(lista):
    melhor = None
    for x in lista:
        if(melhor is None):
            melhor = x
        else:
            if(melhor.get_custo() < x.get_custo()):
                continue
            else:
                melhor = x
    return melhor

def inicializa_espaco(dim, obstaculos, inicio, goal):
    matriz = [ [ "0" for i in range(dim) ] for j in range(dim) ]
    # inicializar espaço numa só função
    # desafio: inicializar espaço numa só linha de código
    for x in obstaculos:
        insere_objetos_na_matriz(matriz, x.get_posicao(), "1")
    insere_objetos_na_matriz(matriz, inicio.get_posicao(), "S")
    insere_objetos_na_matriz(matriz, goal.get_posicao(), "G")

    for i in matriz:
        print " ".join(i)
    print"\n"
    return matriz

def calcula_heuristica(current, goal):
    return abs(goal.get_posicao()[0] - current.get_posicao()[0]) + abs(goal.get_posicao()[1] - current.get_posicao()[1])

def is_goal(current, goal):
    if(current.get_posicao() == goal.get_posicao()):
        return True
    else:
        return False

def calcula_custo(q, goal):
    for x in q:
        x.atualiza_custo(goal)

def calcula_expancao(current):
    return  [no([current.get_posicao()[0] + 1, current.get_posicao()[1]]), \
            no([current.get_posicao()[0] - 1, current.get_posicao()[1]]), \
            no([current.get_posicao()[0], current.get_posicao()[1] + 1]), \
            no([current.get_posicao()[0], current.get_posicao()[1] - 1])]

def algoritmo(inicio, goal):
    q = [inicio]
    i = 0

    while(len(q) > 0):
        h = q.pop(devolve_a_posicao(q))
        r = q
        if(is_goal(h, goal)):
            print "encontrei em %d iteracoes" %i
            break
        else:
            q = calcula_expancao(h)
            calcula_custo(q, goal)
            q.extend(r)
            i += 1

# modularizar esta função
def ler_ficheiro():
    try:
        file = open("espaco.txt", "r")      
        espaco = file.read().splitlines()
        # dimensao do espaço
        dimensao = int(espaco[0])

        # obstaculos (reduzir linhas de código para isto)
        obstaculos = []
        linha_obstaculos = espaco[1].replace(" ", "").split(";")
        for x in linha_obstaculos:
            obstaculos.append(no([int(x[1]), int(x[-2])]))

        # initial state
        inicio = no([int(espaco[2][1]), int(espaco[2][-2])])
        # goal state
        goal = no([int(espaco[3][1]), int(espaco[3][-2])])

        # inicializa espaço com dimensao, obstaculos, initial e goal state
        inicializa_espaco(dimensao, obstaculos, inicio, goal)

        algoritmo(inicio, goal)
    except IOError:
        print "Erro, ficheiro não encontrado"
    else:
        print "Ficheiro lido com sucesso"

def main():
    # cenas do main
    ler_ficheiro()

### START ###

main()