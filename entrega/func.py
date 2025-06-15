# Funciones auxiliares

# ---------------------------------------------------------------------------------------- #

# Funcion de lectura de gramaticas
# Carga una gramatica desde un archivo y devuelve un diccionario con las reglas y palabras
def cargar_gramatica(ruta_archivo):
    gramaticas={}
    reglas = {}
    palabras = []
    n = 1

    with open(ruta_archivo) as f:
        for linea in f:
            if linea:
                linea = linea.strip()


                if '->' in linea:
                    l_iz, l_der = linea.split('->')
                    l_iz = l_iz.strip()
                    alternativas = l_der.split('|')

                    for alt in alternativas:
                        alt = alt.strip()
                        if alt not in ['epsilon', 'ε']:
                            produccion = alt.split() if ' ' in alt else list(alt)
                            reglas.setdefault(l_iz, []).append(produccion)

                            
                if linea != "":
                    palabras.append(linea)
                        
                        
                #si hay \n es q hay nueva gramatica, y se guarda lo que hemos leido
                if linea == "" or linea == " ":
                    if reglas and palabras:
                        gramaticas[f"G{n}"] = {
                            "reglas": reglas,
                            "palabras": palabras
                        }
                        n += 1
                        reglas = {}
                        palabras = []
            

    # Si input no acaba en /n añadir lo ultimo leido               
    if reglas and palabras:
        gramaticas[f"G{n}"] = {
            "reglas": reglas,
            "palabras": palabras
        }

    return gramaticas

# ---------------------------------------------------------------------------------------- #

# Función que comprueba si una gramática está en forma normal de Chomsky (CNF)
def es_cnf(gramatica):
    simbolo_inicial = list(gramatica.keys())[0]
    no_terminales = set(gramatica.keys())
    terminales = set()

    
    # Recorremos toda la gramática para ver qué símbolos podrían ser terminales
    for reglas in gramatica.values():
        for produccion in reglas:
            for simbolo in produccion:
                if simbolo == simbolo_inicial:
                    return False
                if simbolo not in no_terminales :
                    terminales.add(simbolo)

    # Ahora comprobamos si cada producción cumple las reglas de la CNF
    for _, reglas in gramatica.items():
        for produccion in reglas:
            
            if len(produccion) == 1:
                # Caso A -> a
                if produccion[0] not in terminales:
                    return False
                    
            elif len(produccion) == 2:
                # Caso A -> B C
                if produccion[0] in terminales or produccion[1] in terminales:
                    return False
                    
            else:
                # Producción con más de 2 símbolos ej A-> BCD
                return False
                
    
     
    return True    
    
# ---------------------------------------------------------------------------------------- #

# Funcion que implementa el algoritmo CKY para verificar si una cadena pertenece a una gramática en CNF
def cky(gramatica, palabra):
    n = len(palabra)
    tabla = [[set() for _ in range(n)] for _ in range(n)]

    # Crear un diccionario inverso: RHS -> LHS
    inversa = {}
    for lhs, producciones in gramatica.items():
        for rhs in producciones:
            clave = tuple(rhs)
            inversa.setdefault(clave, []).append(lhs)

    # Rellenar la diagonal (longitud 1): A -> a
    for i, simbolo in enumerate(palabra):
        if (simbolo,) in inversa:
            tabla[i][i].update(inversa[(simbolo,)])

    # Rellenar el resto de la tabla
    for longitud in range(2, n + 1):  # tamaño del fragmento
        for i in range(n - longitud + 1):
            j = i + longitud - 1
            for k in range(i, j):
                izquierda = tabla[i][k]
                derecha = tabla[k + 1][j]
                for B in izquierda:
                    for C in derecha:
                        if (B, C) in inversa:
                            tabla[i][j].update(inversa[(B, C)])
    
    # Verificamos si el símbolo inicial S genera toda la cadena
    return 'S' in tabla[0][n - 1]
