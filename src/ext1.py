# Helper functions for extension 1

# ---------------------------------------------------------------------------------------- #

# Convert a grammar to Chomsky normal form (CNF)
def convertir_cnf(gramatica):

    simbolo_inicial = list(gramatica.keys())[0]

    # Nonterminals: dictionary keys
    no_terminales = set(gramatica.keys())
    terminales = set()

    # Scan all rules to identify terminals
    for reglas in gramatica.values():
        for produccion in reglas:
            for simbolo in produccion:
                if simbolo not in no_terminales and simbolo != 'epsilon':
                    terminales.add(simbolo)

    nueva_gramatica = {}
    contador = 0


    # Step 1: Introduce a new start symbol if needed
    if any(simbolo_inicial in prod for reglas in gramatica.values() for prod in reglas):
        nueva_gramatica['S0'] = [[simbolo_inicial]]
        simbolo_inicial = 'S0'

    # Copy the original rules
    for no_terminal, reglas in gramatica.items():
        nueva_gramatica[no_terminal] = reglas.copy()


    # Step 2: Eliminate epsilon productions
    vacios = set()
    for nt, reglas in nueva_gramatica.items():
        for regla in reglas:
            if regla == ['epsilon']:
                vacios.add(nt)

    for nt in vacios:
        nueva_gramatica[nt] = [r for r in nueva_gramatica[nt] if r != ['epsilon']]
        for nt2, reglas in nueva_gramatica.items():
            nuevas = []
            for regla in reglas:
                if nt in regla:
                    nueva = [s for s in regla if s != nt]
                    if nueva and nueva != regla and nueva not in reglas:
                        nuevas.append(nueva)
            nueva_gramatica[nt2].extend(nuevas)


    # Step 3: Eliminate unit productions
    for nt in list(nueva_gramatica):
        nuevas = []
        for regla in nueva_gramatica[nt]:
            if len(regla) == 1 and regla[0] in nueva_gramatica and regla[0] != nt:
                nuevas.extend([r for r in nueva_gramatica[regla[0]] if r not in nueva_gramatica[nt]])
        nueva_gramatica[nt].extend(nuevas)  


    # Step 4: Split long productions
    for nt in list(nueva_gramatica):
        nuevas = []
        for regla in nueva_gramatica[nt]:
            while len(regla) > 2:
                nuevo = f"X{contador}"
                contador += 1
                nueva_gramatica[nuevo] = [[regla[0], regla[1]]]
                regla = [nuevo] + regla[2:]
            nuevas.append(regla)
        nueva_gramatica[nt] = nuevas


    # Step 5: Isolate terminals in productions containing multiple symbols
    reemplazos = {}
    for nt in list(nueva_gramatica):
        for _, regla in enumerate(nueva_gramatica[nt]):
            if len(regla) == 2:
                for j in range(2):
                    simbolo = regla[j]
                    if simbolo in terminales:
                        if simbolo not in reemplazos:
                            nuevo = f"T{contador}"
                            contador += 1
                            nueva_gramatica[nuevo] = [[simbolo]]
                            reemplazos[simbolo] = nuevo
                        regla[j] = reemplazos[simbolo]

    return nueva_gramatica