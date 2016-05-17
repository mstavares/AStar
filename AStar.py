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

def inicializa_espaco(dim):
    matriz = [ [ "0" for i in range(dim) ] for j in range(dim) ]
    for i in matriz:
        print " ".join(i)
    print"\n"
    return matriz

def teste(matriz, obstaculos, inicio, goal):
    for x in obstaculos:
        insere_objetos_na_matriz(matriz, x.get_posicao(), "1")
    insere_objetos_na_matriz(matriz, inicio.get_posicao(), "S")
    insere_objetos_na_matriz(matriz, goal.get_posicao(), "G")
    for i in matriz:
        print " ".join(i)


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


# temos de fazer um try catch finally para a leitura do ficheiro
# o ficheiro tem de ser passado ao main por parametro


matriz = inicializa_espaco(6)
file = open("espaco.txt", "r")
espaco = file.read().splitlines()


dimensao = int(espaco[0])
obstaculos = []

linha_obstaculos = espaco[1].replace(" ", "").split(";")
for x in linha_obstaculos:
    obstaculos.append(no([int(x[1]), int(x[-2])]))

inicio = no([int(espaco[2][1]), int(espaco[2][-2])])
goal = no([int(espaco[3][1]), int(espaco[3][-2])])

teste(matriz, obstaculos, inicio, goal)
algoritmo(inicio, goal)