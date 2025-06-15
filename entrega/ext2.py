
# Funciones auxiliares para la extensión 1

from collections import defaultdict

# ---------------------------------------------------------------------------------------- #

# Funcion que carga las gramaticas probabilísticas desde un archivo
def cargar_gramatica2(ruta_archivo):
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
                        
                        # Extraer probabilidad entre corchetes
                        if '[' in alt and ']' in alt:
                            prob_str = alt[alt.rfind('[') + 1:alt.rfind(']')].strip()
                            try:
                                probabilidad = float(prob_str)
                            except ValueError:
                                probabilidad = 1.0
                            alt_sin_prob = alt[:alt.rfind('[')].strip()
                        else:
                            probabilidad = 1.0
                            alt_sin_prob = alt

                        if alt_sin_prob in ['epsilon', 'ε']:
                            produccion = ['epsilon']  # Representamos epsilon siempre como 'epsilon'
                        else:
                            produccion = alt_sin_prob.split() if ' ' in alt_sin_prob else list(alt_sin_prob)
                        reglas.setdefault(l_iz, []).append((produccion, probabilidad))
           
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

# Funcion que implementa el algoritmo CKY probabilístico para verificar si una cadena pertenece a una gramática y su probabilidad

def cky_probabilistico(gramatica, palabra):
    # Convertir palabra a lista si es string
    if isinstance(palabra, str):
        palabra = list(palabra)
    
    # Caso especial: palabra vacía
    if not palabra:
        return 0.0
    
    n = len(palabra)
    
    # Tabla CKY: tabla[i][j] = dict {NoTerminal: prob_max}
    tabla = [[{} for _ in range(n)] for _ in range(n)]
    
    # Construir índices inversos de producciones
    inv_bin = defaultdict(list)  # (B,C) -> lista de (A, p)
    inv_uni = defaultdict(list)  # (a,) -> lista de (A, p)
    
    for A, producciones in gramatica.items():
        for rhs, p in producciones:
            # Convertir lista a tupla para usar como clave en diccionario
            rhs_tuple = tuple(rhs)
            if len(rhs) == 1:
                inv_uni[rhs_tuple].append((A, p))
            elif len(rhs) == 2:
                inv_bin[rhs_tuple].append((A, p))
            else:
                # CKY sólo funciona con gramáticas en CNF (prod. de 1 o 2 símbolos)
                raise ValueError(f"Producción {A} -> {rhs} no está en CNF")
    
    # Llenar diagonal (subcadenas de longitud 1)
    for i in range(n):
        terminal = palabra[i]
        for A, p in inv_uni.get((terminal,), []):
            # Maximizar probabilidad si ya existe entrada para A
            tabla[i][i][A] = max(tabla[i][i].get(A, 0), p)
    
    # Llenar resto de la tabla (subcadenas de longitud 2 a n)
    for longitud in range(2, n + 1):
        for i in range(n - longitud + 1):
            j = i + longitud - 1
            cell = tabla[i][j]
            
            # Probar todos los puntos de división posibles
            for k in range(i, j):
                left_cell = tabla[i][k]
                right_cell = tabla[k + 1][j]
                
                # Combinar todos los no-terminales de las subceldas
                for B, prob_B in left_cell.items():
                    for C, prob_C in right_cell.items():

                        # Buscar producciones A -> B C
                        for A, prob_A in inv_bin.get((B, C), []):
                            prob_total = prob_A * prob_B * prob_C
                            
                            # Actualizar si encontramos mejor probabilidad
                            if prob_total > cell.get(A, 0):
                                cell[A] = prob_total
    
    # Devolver probabilidad de 'S' (o 0 si no aparece)
    return tabla[0][n - 1].get('S', 0.0)


