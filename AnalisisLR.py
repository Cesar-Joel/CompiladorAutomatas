import re


def analisislr(expresion, tabsim, linea):
    expresion = preprocesadoCadena(expresion)
    if not revisionTokens(expresion, tabsim, linea):
        m = re.split(r'\s*\++\s* | \s*\-+\s* | \s*\(+\s* | \s*\)+\s*', expresion)
        for i in range(0, len(m)):
            if m[i][0] == "(":
                m[i] = m[i].split("(")[1]
            if m[i][len(m[i]) - 1] == ")":
                m[i] = m[i].split(")")[0]
        expresion = transformarExp(m, expresion)
        ACCION = [
            [("D", 5), "E", "E", "E", "E", ("D", 4), "E", "E"], #0
            ["E", ("D", 6), ("D", 7), "E", "E", "E", "E", "A"], #1
            ["E", ("R", 3), ("R", 3), ("D", 8), ("D", 9), "E", ("R", 3), ("R", 3)], #2
            ["E", ("R", 6), ("R", 6), ("R", 6), ("R", 6), "E", ("R", 6), ("R", 6)], #3
            [("D", 5), "E", "E", "E", "E", ("D", 4), "E", "E"], #4
            ["E", ("R", 8), ("R", 8), ("R", 8), ("R", 8), "E", ("R", 8), ("R", 8)], #5
            [("D", 5), "E", "E", "E", "E", ("D", 4), "E", "E"], #6
            [("D", 5), "E", "E", "E", "E", ("D", 4), "E", "E"], #7
            [("D", 5), "E", "E", "E", "E", ("D", 4), "E", "E"], #8
            [("D", 5), "E", "E", "E", "E", ("D", 4), "E", "E"], #9
            ["E", ("D", 6), ("D", 7), "E", "E", "E", ("D", 15), "E"], #10
            ["E", ("R", 1), ("R", 1), ("D", 8), ("D", 9), "E", ("R", 1), ("R", 1)], #11
            ["E", ("R", 2), ("R", 2), ("D", 8), ("D", 9), "E", ("R", 2), ("R", 2)], #12
            ["E", ("R", 4), ("R", 4), ("R", 4), ("R", 4), "E", ("R", 4), ("R", 4)], #13
            ["E", ("R", 5), ("R", 5), ("R", 5), ("R", 5), "E", ("R", 5), ("R", 5)], #14
            ["E", ("R", 7), ("R", 7), ("R", 7), ("R", 7), "E", ("R", 7), ("R", 7)]  #15
        ]
        sacarsimbolos = {1: 3, 2: 1, 3: 3, 4: 1, 5: 3, 6: 1}
        producciones = {1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2}
        IR_A = [[1, 2, 3], ["E"], ["E"], ["E"], [10, 2, 3], ["E"], ["E", 11, 3], ["E", 12, 3], ["E", "E", 13], ["E", "E", 14]]
        pila = [0]
        contador = 0
        simbolos = {"+": 1, "*": 2, "(": 3, ")": 4, "$": 5}

        while True:
            longitudExpresion = len(expresion) - 1
            if contador > longitudExpresion:
                a = "$"
            else:
                a = expresion[contador]
            x = pila[len(pila) - 1]
            y = 0
            if a in simbolos:
                y = simbolos[a]
            if ACCION[x][y] != "E" and ACCION[x][y] != "A":
                siguenteAccion = ACCION[x][y][0]
                numeroAccion = ACCION[x][y][1]
                if siguenteAccion == "D":
                    pila.append(numeroAccion)
                    contador += 1
                if siguenteAccion == "R":
                    for x in range(sacarsimbolos[numeroAccion]):
                        pila.pop()
                    t = pila[len(pila) - 1]
                    pila.append(IR_A[t][producciones[numeroAccion]])
            elif ACCION[x][y] == "A":
                print("Analisis sintáctico linea " + str(linea) + ": Correcto")
                break
            elif ACCION[x][y] == "E":
                print("Analisis sintáctico linea " + str(linea) + ": Incorrecto")
                break


def preprocesadoCadena(expresion):
    a = expresion.split("= ", -1)[1]
    a = a.split(";")[0]
    #
    return a


def revisionTokens(expresion, tabsim, linea):
    m = re.split(r'\s*\++\s* | \s*\-+\s* | \s*\(+\s* | \s*\)+\s*', expresion)
    for i in range(0, len(m)):
        if m[i][0] == "(":
            m[i] = m[i].split("(")[1]
        if m[i][len(m[i]) - 1] == ")":
            m[i] = m[i].split(")")[0]
    errores = False
    for i in m:
        existe = False
        if re.fullmatch(r'[a-zA-Z]+', i):
            for j in tabsim:
                if i == j[0]:
                    existe = True
                    errores = False
                    break
                else:
                    errores = True
        elif re.fullmatch(r'[0-9]+', i):
            existe = True
        if existe == False:
            print("Error, en linea " + str(linea) + " la variable " + i + " no existe")
            errores = True
    return errores


def transformarExp(m, exf):
    cont = 0
    for i in m:
        exf = exf.replace(i, str(cont))
        cont += 1
    exf = ''.join(exf.split())
    return exf