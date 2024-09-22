def main():
    
    gananciaMaximaActual = 0
    tareasGanananciaMaximaActual = []
    
    tareas = [ (1, 'T1', []), (2, 'T2', []), (3, 'T3', [3]) ]
    ganancias = []
    ganancias.append([1, 10, 10, 10])
    ganancias.append([2, 10, 10, 10])
    ganancias.append([3, 10, 10, 10])
    
    
def calcularMaximaGanancia(nroSemana, tareasRestantes, tareasRealizadas, gananciaPrevia, ganancias):
    global tareasGanananciaMaximaActual
    
    if not tareasRestantes:
        return 0

    tareasPosiblesSemanaActual = tareasRestantes

    while tareasPosiblesSemanaActual:
        gananciaActual = gananciaPrevia

        tareaARealizar = buscarTareaQueMeConviene(tareasPosiblesSemanaActual, tareasRealizadas, ganancias)
        tareasPosiblesSemanaActual.remove(tareaARealizar)

        for id in tareaARealizar[2]:
            if not tareasRealizadas[id]:
                continue

        gananciaActual += calcularGanancia(tareaARealizar[0], nroSemana, ganancias)
        gananciaSupuesta = funcionCosto()

        if gananciaActual + gananciaSupuesta < gananciaMaximaActual:
            return 0

        gananciaActual += calcularMaximaGanancia(
            nroSemana + 1,
            tareasRestantes - tareaARealizar,
            tareasRealizadas + tareaARealizar,
            gananciaActual,
            ganancias
        )

        if gananciaMaximaActual < gananciaActual:
            gananciaMaximaActual = gananciaActual
            tareasGanananciaMaximaActual = tareasRealizadas + tareaARealizar


def calcularGanancia(idTarea, nroSemana, ganancias):
    return ganancias[idTarea][nroSemana]
    
if __name__ == "__main__":
    main()
