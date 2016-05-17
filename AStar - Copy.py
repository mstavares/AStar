def inicializa_espaco(dim):
    matriz = [ [ "0" for i in range(dim) ] for j in range(dim) ]
    matriz[0][1] = "1"
    for i in matriz:
        print " ".join(i)

inicializa_espaco(5)