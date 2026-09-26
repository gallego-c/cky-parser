# Helper functions

# ---------------------------------------------------------------------------------------- #

# Grammar loading function
# Load a grammar from a file and return a dictionary of rules and words
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
                        
                        
                # A blank line starts a new grammar block; save the data read so far
                if linea == "" or linea == " ":
                    if reglas and palabras:
                        gramaticas[f"G{n}"] = {
                            "reglas": reglas,
                            "palabras": palabras
                        }
                        n += 1
                        reglas = {}
                        palabras = []
            

    # Save the last block if the input does not end with a blank line
    if reglas and palabras:
        gramaticas[f"G{n}"] = {
            "reglas": reglas,
            "palabras": palabras
        }

    return gramaticas

# ---------------------------------------------------------------------------------------- #

# Check whether a grammar is in Chomsky normal form (CNF)
def es_cnf(gramatica):
    simbolo_inicial = list(gramatica.keys())[0]
    no_terminales = set(gramatica.keys())
    terminales = set()

    
    # Scan the grammar to identify possible terminal symbols
    for reglas in gramatica.values():
        for produccion in reglas:
            for simbolo in produccion:
                if simbolo == simbolo_inicial:
                    return False
                if simbolo not in no_terminales :
                    terminales.add(simbolo)

    # Check whether each production satisfies the CNF rules
    for _, reglas in gramatica.items():
        for produccion in reglas:
            
            if len(produccion) == 1:
                # Case A -> a
                if produccion[0] not in terminales:
                    return False
                    
            elif len(produccion) == 2:
                # Case A -> B C
                if produccion[0] in terminales or produccion[1] in terminales:
                    return False
                    
            else:
                # Production with more than two symbols, e.g. A -> BCD
                return False
                
    
     
    return True    
    
# ---------------------------------------------------------------------------------------- #

# Implement CKY to check whether a string belongs to a grammar in CNF
def cky(gramatica, palabra):
    n = len(palabra)
    tabla = [[set() for _ in range(n)] for _ in range(n)]

    # Build an inverse dictionary: RHS -> LHS
    inversa = {}
    for lhs, producciones in gramatica.items():
        for rhs in producciones:
            clave = tuple(rhs)
            inversa.setdefault(clave, []).append(lhs)

    # Fill the diagonal (length 1): A -> a
    for i, simbolo in enumerate(palabra):
        if (simbolo,) in inversa:
            tabla[i][i].update(inversa[(simbolo,)])

    # Fill the remaining table cells
    for longitud in range(2, n + 1):  # Substring length
        for i in range(n - longitud + 1):
            j = i + longitud - 1
            for k in range(i, j):
                izquierda = tabla[i][k]
                derecha = tabla[k + 1][j]
                for B in izquierda:
                    for C in derecha:
                        if (B, C) in inversa:
                            tabla[i][j].update(inversa[(B, C)])
    
    # Check whether the start symbol S generates the entire string
    return 'S' in tabla[0][n - 1]
