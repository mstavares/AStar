import sys

class No:
    def __init__(self, posicao, custo = 0):
        self.posicao = posicao
        self.custo = custo

    def get_posicao(self):
        return self.posicao

    def get_custo(self):
        return self.custo

    def atualiza_custo(self, goal):
        self.custo += 1 + calcula_heuristica(self, goal)

def insere_objetos_na_matriz(matriz, posicao, objeto):
    matriz[posicao[0]][posicao[1]] = objeto

def devolve_o_melhor_no(lista):
    melhor = lista[0]
    for x in lista:
        if melhor.get_custo() > x.get_custo():
            melhor = x
    return lista.index(melhor)



def calcula_heuristica(current, goal):
    return abs(goal.get_posicao()[0] - current.get_posicao()[0]) + abs(goal.get_posicao()[1] - current.get_posicao()[1])

def is_goal(current, goal):
    if current.get_posicao() == goal.get_posicao():
        return True
    else:
        return False

def calcula_custo(q, goal):
    [x.atualiza_custo(goal) for x in q]

def calcula_expancao(current, obstaculos):
    expansao = [No([current.get_posicao()[0] + 1, current.get_posicao()[1]]),
            No([current.get_posicao()[0] - 1, current.get_posicao()[1]]),
            No([current.get_posicao()[0], current.get_posicao()[1] + 1]),
            No([current.get_posicao()[0], current.get_posicao()[1] - 1])]

    return [x for x in expansao if x.get_posicao() not in obstaculos]

def imprime_o_caminho(caminho, matriz):
    caminho.pop(0), caminho.pop(-1)
    for no in caminho:
        insere_objetos_na_matriz(matriz, no.get_posicao(), "x")
    imprime_a_matriz(matriz)

def imprime_a_matriz(matriz):
    for i in matriz:
        print " ".join(i)
    print"\n"

def a_star(inicio, goal, obstaculos, matriz):
    caminho = []
    q = [inicio]
    i = 0

    while len(q) > 0:
        h = q.pop(devolve_o_melhor_no(q))
        caminho.append(h)
        print h.get_posicao()
        r = q
        if is_goal(h, goal):
            print "encontrei em %d iteracoes" % i
            imprime_o_caminho(caminho, matriz)
            break
        else:
            q = calcula_expancao(h, obstaculos)
            calcula_custo(q, goal)
            q.extend(r)
            i += 1

# inicializa espaço com os dados fornecidos pelo ficheiro
def inicializa_espaco(dim, obstaculos, inicio, goal):
    matriz = [ [ "." for i in range(dim) ] for j in range(dim) ]

    for obstaculo in obstaculos:
        insere_objetos_na_matriz(matriz, obstaculo, "1")
    insere_objetos_na_matriz(matriz, inicio.get_posicao(), "S")
    insere_objetos_na_matriz(matriz, goal.get_posicao(), "G")
    imprime_a_matriz(matriz)
    return matriz

# modularizar esta funcao
def ler_ficheiro(ficheiro):
    try:
        file = open(ficheiro, "r")
        ficheiro = file.read().splitlines()

        # dimensao do espaco
        dimensao = int(ficheiro[0])

        # obstaculos (em otimização)
        linha_obstaculos = ficheiro[1].replace(" ", "").split(";")
        obstaculos = []
        for obs in linha_obstaculos:
            x, y = map(int, obs.strip('()').split(','))
            obstaculos.append([x, y])

        # initial state
        x, y = map(int, ficheiro[2].strip('()').split(','))
        inicio = No([x, y])

        # goal state
        x, y = map(int, ficheiro[3].strip('()').split(','))
        goal = No([x, y])

        # inicializa espaco com dimensao, obstaculos, initial e goal state
        matriz = inicializa_espaco(dimensao, obstaculos, inicio, goal)

        a_star(inicio, goal, obstaculos, matriz)
    except IOError:
        print "Erro, ficheiro nao encontrado"
    finally:
        file.close()
        print "Ficheiro lido com sucesso"

def main(argv):
    # teste ao argumento do programa
    if(len(argv) == 2):
        ler_ficheiro(argv[1])
    else:
        print "O programa necessita de receber o ficheiro por argumento."

### START ###

main(sys.argv)