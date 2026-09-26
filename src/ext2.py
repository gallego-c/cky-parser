# Helper functions for extension 2

from collections import defaultdict

# ---------------------------------------------------------------------------------------- #

# Load probabilistic grammars from a file
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
                        
                        # Extract the probability enclosed in square brackets
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
                            produccion = ['epsilon']  # Always represent epsilon as 'epsilon'
                        else:
                            produccion = alt_sin_prob.split() if ' ' in alt_sin_prob else list(alt_sin_prob)
                        reglas.setdefault(l_iz, []).append((produccion, probabilidad))
           
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

# Implement probabilistic CKY to compute the best derivation probability for a string

def cky_probabilistico(gramatica, palabra):
    # Convert the word to a list if it is a string
    if isinstance(palabra, str):
        palabra = list(palabra)
    
    # Special case: empty string
    if not palabra:
        return 0.0
    
    n = len(palabra)
    
    # CKY table: tabla[i][j] = dictionary {nonterminal: maximum probability}
    tabla = [[{} for _ in range(n)] for _ in range(n)]
    
    # Build inverse production indexes
    inv_bin = defaultdict(list)  # (B, C) -> list of (A, p)
    inv_uni = defaultdict(list)  # (a,) -> list of (A, p)
    
    for A, producciones in gramatica.items():
        for rhs, p in producciones:
            # Convert the list to a tuple for use as a dictionary key
            rhs_tuple = tuple(rhs)
            if len(rhs) == 1:
                inv_uni[rhs_tuple].append((A, p))
            elif len(rhs) == 2:
                inv_bin[rhs_tuple].append((A, p))
            else:
                # CKY requires a CNF grammar (productions with one or two symbols)
                raise ValueError(f"Producción {A} -> {rhs} no está en CNF")
    
    # Fill the diagonal (substrings of length 1)
    for i in range(n):
        terminal = palabra[i]
        for A, p in inv_uni.get((terminal,), []):
            # Keep the maximum probability if an entry for A already exists
            tabla[i][i][A] = max(tabla[i][i].get(A, 0), p)
    
    # Fill the remaining table cells (substring lengths from 2 to n)
    for longitud in range(2, n + 1):
        for i in range(n - longitud + 1):
            j = i + longitud - 1
            cell = tabla[i][j]
            
            # Try every possible split point
            for k in range(i, j):
                left_cell = tabla[i][k]
                right_cell = tabla[k + 1][j]
                
                # Combine all nonterminals from the two subcells
                for B, prob_B in left_cell.items():
                    for C, prob_C in right_cell.items():

                        # Look up productions A -> B C
                        for A, prob_A in inv_bin.get((B, C), []):
                            prob_total = prob_A * prob_B * prob_C
                            
                            # Update the cell if a higher probability is found
                            if prob_total > cell.get(A, 0):
                                cell[A] = prob_total
    
    # Return the probability for 'S' (or 0 if absent)
    return tabla[0][n - 1].get('S', 0.0)


