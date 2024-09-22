tareas = []
ganancias = []

mejoresGananciasPorSemana = []

gananciaMaximaActual = 0
tareasGanananciaMaximaActual = []

def main():
    
    global tareas
    global ganancias
    
    global mejoresGananciasPorSemana
        
    # leo las ganancias
    ganancias = []
    # ganancias.append([1, 10])
    ganancias.append([1, 10, 1, 1])
    ganancias.append([2, 1, 20, 1])
    ganancias.append([3, 50, 1, 1])
    
    # leo las tareas
    # tareas = [ (1, 'T1', []) ]
    tareas = [ (1, 'T1', []), (2, 'T2', []), (3, 'T3', [2]) ]
    
    # hay que calcularlo bien después
    # mejoresGananciasPorSemana = [10]
    mejoresGananciasPorSemana = [50, 20, 1]
    
    # cada posición simboliza si una tarea fue realizada
    estadoTareas = []
    for _ in tareas:
        estadoTareas.append(False)
    
    calcularMaximaGanancia(0, estadoTareas, [], 0)
    
    print("====================================")
    print("Ganancia máxima: ", gananciaMaximaActual)
    print("Tareas realizadas: ", tareasGanananciaMaximaActual)


# ======================= BACKTRACKING =======================

# backtracking
def calcularMaximaGanancia(nroSemana, estadoTareas, tareasRealizadas, gananciaActual):
    global tareas
    
    global gananciaMaximaActual
    global tareasGanananciaMaximaActual
    
    
    # estadosDescendientes
    estadosDescendientes = obtenerTareasNoRealizadas(estadoTareas)
    
    # descendientes
    descendientes = []
    for idTarea in estadosDescendientes:
        # propiedad de corte
        if todasTareasPreviasRealizadas(tareas[idTarea - 1], estadoTareas):
            # funcion costo
            ganancia = funcionCosto(nroSemana, idTarea, gananciaActual)
            descendientes.append((idTarea, ganancia, False))
    
    descendientesExplorados = 0
    # mientras existan estados descendientes no explorados
    while descendientesExplorados < len(descendientes):
        
        # estadoProximo con mayor fc
        idxDescendiente = buscarIdDescendienteConMayorFc(descendientes)
        descendientesExplorados +=1
        
        # marco al descendiente como visitado
        (idTarea, ganancia, _) = descendientes[idxDescendiente]
        descendientes[idxDescendiente] = (idTarea, ganancia, True)
        
        print("Semana: ", nroSemana, ". Tarea: ", idTarea)

        # marco la tarea como realizada
        estadoTareas[idTarea - 1] = True
        tareasRealizadas.append(idTarea)
        
        # si fc es de estadoProximo es mayor a la mejor solucion obtenida
        if gananciaMaximaActual < ganancia:
            # si es solucion
            if (len(tareas) == len(tareasRealizadas)) and (gananciaMaximaActual < ganancia):
                print("Actualizo solución")
                print("Tareas realizadas: ", tareasRealizadas)
                print("Ganancia: ", ganancia)
                gananciaMaximaActual = ganancia
                tareasGanananciaMaximaActual = tareasRealizadas.copy()
            
            calcularMaximaGanancia(nroSemana + 1, estadoTareas, tareasRealizadas, gananciaActual)
            
        # desmarco la tarea como realizada
        estadoTareas[idTarea - 1] = False
        # ver una forma optima de hacer esto
        tareasRealizadas.pop()
            
            
def buscarIdDescendienteConMayorFc(descendientes):
    idDescendienteConMayorFc = 0
    maxFc = descendientes[0][1]
    
    for i in range(1, len(descendientes)):
        (tarea, fc, visitado) = descendientes[i]
        if visitado:
            continue
        if (not visitado) and maxFc < fc:
            idDescendienteConMayorFc = i
    
    return idDescendienteConMayorFc

# ======================= ESTADOS DESCENDIENTES =======================

def obtenerTareasNoRealizadas(estadoTareas):
    global tareas
    
    tareasNoRealizadas = []
    
    for tarea in tareas:
        idTarea = tarea[0]
        if not estadoTareas[idTarea - 1]:
            tareasNoRealizadas.append(idTarea)
    
    return tareasNoRealizadas

# ======================= PROPIEDAD CORTE =======================

def todasTareasPreviasRealizadas(tarea, estadoTareas):
    
    tareasPrevias = tarea[2]
    
    if len(tareasPrevias) == 0:
        return True
        
    for tarea in tareasPrevias:
        if not estadoTareas[tarea - 1]:
            return False
        
    return True

# ======================= FUNCION COSTO =======================

def funcionCosto(nroSemana, idTarea, gananciaActual):
    
    gananciaActual += calcularGananciaTarea(nroSemana, idTarea)
    proyeccionGananciaOptima = calcularOptimaGanancia(nroSemana)
    
    return gananciaActual + proyeccionGananciaOptima

def calcularGananciaTarea(nroSemana, idTarea):
    global ganancias
    
    return ganancias[idTarea - 1][nroSemana + 1]

def calcularOptimaGanancia(nroSemana):
    global mejoresGananciasPorSemana
    
    gananciaOptima = 0
    
    for i in range(nroSemana + 1, len(mejoresGananciasPorSemana)):
        gananciaOptima += mejoresGananciasPorSemana[i]
    
    return gananciaOptima    
    
if __name__ == "__main__":
    main()
