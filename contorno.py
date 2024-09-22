import sys
ARCHIVO_PARTES = sys.argv[1]

def main():

    # una parte
    # listaPartes = [(1, 10, 3)]

    # dos partes disjuntas
    # listaPartes = [(1, 10, 3), (4, 15, 6)]

    # dos partes unidas
    # listaPartes = [(1, 10, 4), (3, 15, 6)]

    # dos partes unidas en un punto
    # listaPartes = [(1, 10, 3), (3, 5, 6)]

    # dos partes iguales
    # listaPartes = [(1, 10, 3), (1, 10, 3)]

    # partes que ocupan lo mismo
    # listaPartes = [(1, 20, 3), (1, 20, 3), (1, 50, 3)]

    # partes disjuntas
    # listaPartes = [(1, 10, 3), (4, 15, 6), (7, 20, 9), (10, 20, 11)]

    # partes que ocupan lo mismo + una disjunta
    #listaPartes = [(3, 20, 5), (1, 20, 2), (1, 20, 2),
     #              (3, 20, 5), (3, 20, 5), (2, 15, 4)]

    """
     listaPartes = [(3, 20, 5), (1, 20, 2), (1, 20, 3),
                   (4, 20, 6), (5, 20, 8), (2, 15, 4),
                   (1, 20, 2), (1, 20, 8), (0, 20, 7)] 
    """

    lista_partes = leer_archivo_partes(ARCHIVO_PARTES)
    # enunciado
    # listaPartes = [(1, 11, 5), (2, 6, 7), (3, 13, 9),
    #                (12, 7, 16), (14, 3, 25), (19, 18, 22)]

    print("Contorno: ", contorno(lista_partes))

# ======================= FUNCION RECURSIVA =======================


def contorno(listaPartes):
    return generarContornoAPartirDePartes(listaPartes, 0, len(listaPartes))


def generarContornoAPartirDePartes(listaPartes, inicio, fin):

    if fin - inicio == 1:
        return construirUnContorno(listaPartes[inicio])

    medio = (inicio + fin) // 2
    contorno1 = generarContornoAPartirDePartes(listaPartes, inicio, medio)
    contorno2 = generarContornoAPartirDePartes(listaPartes, medio, fin)

    return mergeContornos(contorno1, contorno2)

# ======================= FUNCIONES AUXILIARES =======================


def construirUnContorno(parte):

    contorno = []
    (x1, y, x2) = parte

    contorno.append((x1, y))
    contorno.append((x2, 0))

    return contorno


def mergeContornos(contorno1, contorno2):

    contorno = []
    lenContorno = 0
    idxContorno1 = 0
    idxContorno2 = 0

    contornoId = idContornoConMenorCoordenadaX(
        contorno1,
        idxContorno1,
        contorno2,
        idxContorno2
    )
    if contornoId == 1:
        menorCoordenadaActual = contorno1[idxContorno1]
        idxContorno1 += 1
    else:
        menorCoordenadaActual = contorno2[idxContorno2]
        idxContorno2 += 1

    (x, _) = menorCoordenadaActual

    while (idxContorno1 < len(contorno1) or idxContorno2 < len(contorno2)):

        contornoId = idContornoConMenorCoordenadaX(
            contorno1,
            idxContorno1,
            contorno2,
            idxContorno2
        )
        if contornoId == 1:
            menorCoordenadaActual = contorno1[idxContorno1]
            idxContorno1 += 1
        else:
            menorCoordenadaActual = contorno2[idxContorno2]
            idxContorno2 += 1

        x1 = x
        x2 = menorCoordenadaActual[0]
        (x, _) = menorCoordenadaActual

        intervalo = (x1, x2)

        if (intervalo[0] == intervalo[1]):
            continue

        y = alturaMaximaEnIntervalo(
            contorno1,
            idxContorno1,
            contorno2,
            idxContorno2,
            intervalo
        )

        if lenContorno == 0:
            contorno.append((x1, y))
            lenContorno += 1
        elif contorno[lenContorno - 1][1] != y:
            contorno.append((x1, y))
            lenContorno += 1

    contorno.append((x2, 0))
    return contorno


def idContornoConMenorCoordenadaX(
    contorno1,
    idxContorno1,
    contorno2,
    idxContorno2
):
    if len(contorno1) <= idxContorno1:
        return 2
    if len(contorno2) <= idxContorno2:
        return 1

    if contorno1[idxContorno1][0] <= contorno2[idxContorno2][0]:
        return 1
    else:
        return 2


def alturaMaximaEnIntervalo(
        contorno1,
        idxContorno1,
        contorno2,
        idxContorno2,
        intervalo
):
    y1 = alturaDeContorno(contorno1, idxContorno1, intervalo)
    y2 = alturaDeContorno(contorno2, idxContorno2, intervalo)

    return y1 if (y1 > y2) else y2


def alturaDeContorno(contorno, idxContorno, intervalo):

    # considero al intervalo cerrado a la izquierda y abierto a la derecha
    # [x1, x2)
    (x1, _) = intervalo

    # para saber la altura del contorno, tengo que saber que un
    # intervalo puede haber sido generado por:
    # - una coordenada de cada contorno
    # - dos coordenadas del mismo contorno

    # caso 1: una coordenada de cada contorno
    idxAuxiliar = idxContorno - 1
    if idxAuxiliar < 0:
        return 0
    (x, y) = contorno[idxAuxiliar]
    if x <= x1:
        return y

    # caso 2: dos coordenadas del mismo contorno
    idxAuxiliar = idxContorno - 2
    if idxAuxiliar < 0:
        return 0
    (_, y) = contorno[idxAuxiliar]
    return y

def leer_archivo_partes(archivo_partes):
    lista_partes = []

    with open(archivo_partes, 'r') as archivo:
        for linea in archivo:
            izquierda, altura, derecha = map(int, linea.strip().split(','))
            lista_partes.append((izquierda, altura, derecha))

    return lista_partes

if __name__ == "__main__":
    main()
