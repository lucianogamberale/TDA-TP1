import sys

ARCHIVO_TAREAS = sys.argv[1]
ARCHIVO_GANANCIAS = sys.argv[2]

tareas = []
ganancias = []

estadoTareas = []
mejoresGananciasPorSemana = []

gananciaMaxima = 0
ordenTareasGananciaMaxima = []


def main():
    
    leerArchivoTareas(ARCHIVO_TAREAS)
    leerArchivoGanancias(ARCHIVO_GANANCIAS)
    
    proyecto()

# ======================= FUNCION PPAL =======================

def proyecto():
    
    inicializarMejoresGananciasPorSemana()
    inicializarEstadoTareas()
    
    nroSemana = 0
    gananciaPrevia = 0
    ordenTareasRealizadas = []   
    
    calcularMaximaGanancia(nroSemana, gananciaPrevia, ordenTareasRealizadas)
    
    print("Ganancia máxima: ", gananciaMaxima)
    print("Orden de tareas: ", ordenTareasGananciaMaxima)
    

# ======================= LECTURA ARCHIVOS =======================    

def leerArchivoTareas(nombreArchivo):
    global tareas

    with open(nombreArchivo, 'r') as file:
        for line in file:
            partes = line.strip().split(',') 
            idTarea = int(partes[0])          
            nombreTarea = partes[1].strip() 
            
            if len(partes) > 2:           
                listaTareasPrevias = [int(x) for x in partes[2:]] 
            else:
                listaTareasPrevias = []

            tarea = (idTarea, nombreTarea, listaTareasPrevias)  
            tareas.append(tarea)  

    return tareas


def leerArchivoGanancias(nombreArchivo):
    global ganancias

    with open(nombreArchivo, 'r') as file:
        for line in file:
            numeros = [int(x) for x in line.strip().split(',')]
            ganancias.append(numeros)

    return ganancias


# ======================= INICIALIZAR =======================

def inicializarEstadoTareas():
    global tareas
    global estadoTareas
    
    for _ in tareas:
        estadoTareas.append(False)


def inicializarMejoresGananciasPorSemana():
    global ganancias
    global mejoresGananciasPorSemana
        
    for i in range(1, len(ganancias) + 1):
        gananciaMaxima = 0
        for j in range(0, len(ganancias)):
            if gananciaMaxima < ganancias[j][i]:
                gananciaMaxima = ganancias[j][i]
        mejoresGananciasPorSemana.append(gananciaMaxima)


# ======================= BACKTRACKING =======================

# funcion backtracking
def calcularMaximaGanancia(nroSemana, gananciaPrevia, ordenTareasRealizadas):
    global tareas
    
    global gananciaMaxima
    global ordenTareasGananciaMaxima
        
    # estadosDescendientes
    tareasNoRealizadas = obtenerTareasNoRealizadas()
    
    # descendientes
    tareasNoRealizadasAExplorar = []
    for idTarea in tareasNoRealizadas:
        # propiedad de corte
        if todasTareasPreviasRealizadas(idTarea):
            # funcion costo
            gananciaEstimada = calcularMaximaGananciaPosible(nroSemana, idTarea, gananciaPrevia)
            tareasNoRealizadasAExplorar.append((idTarea, gananciaEstimada, False))
    
    cantidadTareasExploradas = 0
    # mientras existan estados descendientes no explorados
    while cantidadTareasExploradas < len(tareasNoRealizadasAExplorar):
        
        # estadoProximo con mayor fc
        idxDescendiente = buscarIdxTareaNoRealizadaConMayorFc(tareasNoRealizadasAExplorar)
        cantidadTareasExploradas +=1
        
        # marco al descendiente como visitado
        (idTarea, gananciaEstimada, _) = tareasNoRealizadasAExplorar[idxDescendiente]
        tareasNoRealizadasAExplorar[idxDescendiente] = (idTarea, gananciaEstimada, True)
        
        marcarTareaComoRealizada(idTarea, ordenTareasRealizadas)
        
        # si fc es de estadoProximo es mayor a la mejor solucion obtenida
        if gananciaMaxima < gananciaEstimada:
            # si es solucion
            if (len(tareas) == len(ordenTareasRealizadas)) and (gananciaMaxima < gananciaEstimada):
                gananciaMaxima = gananciaEstimada
                ordenTareasGananciaMaxima = ordenTareasRealizadas.copy()
            
            gananciaTarea = calcularGananciaTarea(nroSemana, idTarea)
            calcularMaximaGanancia(
                nroSemana + 1,
                gananciaPrevia + gananciaTarea,
                ordenTareasRealizadas
            )
            
        marcarTareaComoNoRealizada(idTarea, ordenTareasRealizadas)


# ======================= ESTADOS DESCENDIENTES =======================

def obtenerTareasNoRealizadas():
    global tareas
    global estadoTareas
    
    tareasNoRealizadas = []
    
    for tarea in tareas:
        idTarea = tarea[0]
        if not estadoTareas[idTarea - 1]:
            tareasNoRealizadas.append(idTarea)
    
    return tareasNoRealizadas


# ======================= PROPIEDAD CORTE =======================

def todasTareasPreviasRealizadas(idTarea):
    global tareas
    global estadoTareas
    
    tareasPrevias = tareas[idTarea - 1][2]
    
    if len(tareasPrevias) == 0:
        return True
        
    for tarea in tareasPrevias:
        if not estadoTareas[tarea - 1]:
            return False
        
    return True


# ======================= FUNCION COSTO =======================

def calcularMaximaGananciaPosible(nroSemana, idTarea, gananciaPrevia):
    
    gananciaActual = gananciaPrevia
    gananciaActual += calcularGananciaTarea(nroSemana, idTarea)
    gananciaProyectada = calcularProyeccionMaximaGananciaPosible(nroSemana)
    
    return gananciaActual + gananciaProyectada


def calcularGananciaTarea(nroSemana, idTarea):
    global ganancias
    
    return ganancias[idTarea - 1][nroSemana + 1]


def calcularProyeccionMaximaGananciaPosible(nroSemana):
    global mejoresGananciasPorSemana
    
    gananciaOptima = 0
    
    for i in range(nroSemana + 1, len(mejoresGananciasPorSemana)):
        gananciaOptima += mejoresGananciasPorSemana[i]
    
    return gananciaOptima    
   
   
# ======================= ESTADO PROXIMO =======================

def buscarIdxTareaNoRealizadaConMayorFc(tareasNoRealizadasAExplorar):
    idxMaxFc = -1
    maxFc = 0
    
    for i in range(0, len(tareasNoRealizadasAExplorar)):
        (_, fc, visitado) = tareasNoRealizadasAExplorar[i]
        if visitado:
            continue
        if (not visitado) and maxFc < fc:
            idxMaxFc = i
    
    return idxMaxFc


# ======================= AUXILIARES =======================

def marcarTareaComoRealizada(idTarea, ordenTareasRealizadas):
    global estadoTareas

    estadoTareas[idTarea - 1] = True
    ordenTareasRealizadas.append(idTarea)
    
    
def marcarTareaComoNoRealizada(idTarea, ordenTareasRealizadas):
    global estadoTareas
    
    estadoTareas[idTarea - 1] = False
    ordenTareasRealizadas.pop()


if __name__ == "__main__":
    main()
